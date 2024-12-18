# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ..functions import read_time_points, donwsample
from ...tools import printv
from os.path import isfile, basename, abspath, dirname
from tqdm import tqdm
import numpy as np
import os

#Adapated from the https://github.com/stardist/stardist/blob/c6c261081c6f9717fa9f5c47720ad2d5a9153224/examples/3D/2_training.ipynb

def random_fliprot(img, mask, axis=None):
    if axis is None:
        axis = tuple(range(mask.ndim))
    axis = tuple(axis)

    assert img.ndim >= mask.ndim
    perm = tuple(np.random.permutation(axis))
    transpose_axis = np.arange(mask.ndim)
    for a, p in zip(axis, perm):
        transpose_axis[a] = p
    transpose_axis = tuple(transpose_axis)
    img = img.transpose(transpose_axis + tuple(range(mask.ndim, img.ndim)))
    mask = mask.transpose(transpose_axis)
    for ax in axis:
        if np.random.rand() > 0.5:
            img = np.flip(img, axis=ax)
            mask = np.flip(mask, axis=ax)
    return img, mask


def random_intensity_change(img):
    img = img * np.random.uniform(0.6, 2) + np.random.uniform(-0.2, 0.2)
    return img


def augmenter(x, y):
    """Augmentation of a single input/label image pair.
    x is an input image
    y is the corresponding ground-truth label image
    """
    # Note that we only use fliprots along axis=(1,2), i.e. the yx axis
    # as 3D microscopy acquisitions are usually not axially symmetric
    x, y = random_fliprot(x, y, axis=(1, 2))
    x = random_intensity_change(x)
    return x, y

def get_ratio(shape,max_r=128):
    ratio=2
    while ratio < shape:
        ratio *= 2
    ratio = int(ratio / 2)
    if ratio > max_r: ratio = max_r  # Max Size
    return ratio

class StardistTrain(MorphoPlugin):
    """
    This plugin allows users to train their own Stardist model on their own 3D datasets.
    Using the 3D intensity image with the corresponding segmentation, you can train your own Stardist model on several time points.
    Then the model can be used with the StardistPredict plugin to perform nuclei prediction on 3D intensity images.
    \n
    This plugin requires intensity image(s), and is applied on the whole image.

    Parameters
    ----------
    downsampling : int, default :2
        The resolution reduction applied to each axis of the input image before performing segmentation, 1 meaning that
        no reduction is applied. Increasing the reduction factor may reduce segmentation quality
    nuclei_intensity_channel: int, default :0
        The desired channel to run stardist on
    epochs : int, default :20
        Number of epochs to train the model
    batch_size: int, default :2
        size of the batch size (increase learning process, but can create memory errors)
    time_points : string, default: current
        The time range to train your model
     model_filename: string
        full filename path to save the model

    Reference
    ---------
        Uwe Schmidt, Martin Weigert, Coleman Broaddus, and Gene Myers. Cell Detection with Star-convex Polygons.
        International Conference on Medical Image Computing and Computer-Assisted Intervention (MICCAI), Granada, Spain,
        September 2018.
        https://github.com/stardist/stardist

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("StardistTrain.png")
        self.set_image_name("StardistTrain.png")
        self.set_name("Startdist Train : Train the Stardist model for nuclei segmentation on your own data ")
        self.add_inputfield("Nuclei Intensity Channel", default=0)
        self.add_inputfield("downsampling", default=2)
        self.add_inputfield("time points", default="current")
        self.add_inputfield("epochs", default=20)
        self.add_inputfield("batch size", default=2)
        self.add_filesaver("model filename")
        self.set_parent("De Novo Segmentation")


    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        import numpy as np
        from csbdeep.utils import normalize

        from stardist import fill_label_holes, calculate_extents, gputools_available
        from stardist import Rays_GoldenSpiral
        from stardist.models import Config3D, StarDist3D

        # Use OpenCL-based computations for data generator during training (requires 'gputools')
        use_gpu = False and gputools_available()
        s_GPU="G" if use_gpu else "C"
        printv(f"Stardist will run on {s_GPU}PU ",1)

        nuclei_channel = int(self.get_inputfield("Nuclei Intensity Channel"))
        downsampling = int(self.get_inputfield("downsampling"))
        epochs = int(self.get_inputfield("epochs"))
        train_batch_size = int(self.get_inputfield("batch size"))
        model_filename = self.get_filesaver("model filename")
        times = read_time_points(self.get_inputfield("time points"), t)

        cancel=True

        #Collect all the data
        train_data=[]
        train_labels=[]
        nb_cells=0
        data_shape=None
        for t in times:
            rawdata = dataset.get_raw(t, nuclei_channel)
            data = dataset.get_seg(t, nuclei_channel)
            if rawdata is None or data is None:
                if rawdata is None : printv("please specify the rawdata at "+str(t),0)
                if data is None: printv("please specify the segmented data at " + str(t), 0)
            else:
                if downsampling>1:  rawdata, data = donwsample(rawdata, data, downsampling)
                if dataset.background != 0: data[ data == dataset.background] = 0  # We do it after the rescaling to go faster
                cells = np.unique(data)
                if len(cells) > 1:
                    train_data.append(np.swapaxes(rawdata,0,2))
                    train_labels.append(np.swapaxes(data,0,2))
                    printv(f"add {len(cells)} objects at {t}",1)
                    nb_cells+= len(cells)
                    data_shape=data.shape

        if len(train_data)==0 or nb_cells==0:
            printv("ERROR Cannot Train with not images or no cells",0)
        else:
            printv(f"{nb_cells} objects added at {t}", 1)
            printv(f"Start Train Stardist on {len(train_data)} 3D images",0)

            #NORMALIZE DATA
            axis_norm = (0, 1, 2) # normalize channels independently
            train_data = [normalize(x, 1, 99.8, axis=axis_norm) for x in tqdm(train_data)]
            train_labels = [fill_label_holes(y) for y in tqdm(train_labels)]

            #MODEL CONFIGURATION
            #print(Config3D.__doc__)
            extents = calculate_extents(train_labels)
            anisotropy = tuple(np.max(extents) / extents)
            printv('empirical anisotropy of labeled objects = %s' % str(anisotropy),1)

            n_rays = 96 # 96 is a good default choice (see 1_data.ipynb)
            printv(f" data shape is {data_shape}",2)
            n_channel=0
            ratio=get_ratio(data_shape[0])
            ratio_z = get_ratio(data_shape[2])

            train_patch_size=(ratio_z,ratio,ratio)
            printv(f" train patch size is {train_patch_size}", 1)

            # Predict on subsampled grid for increased efficiency and larger field of view
            grid = tuple(1 if a > 1.5 else 2 for a in anisotropy)

            # Use rays on a Fibonacci lattice adjusted for measured anisotropy of the training data
            rays = Rays_GoldenSpiral(n_rays, anisotropy=anisotropy)

            conf = Config3D(
                rays=rays,
                grid=grid,
                anisotropy=anisotropy,
                use_gpu=use_gpu,
                n_channel_in=n_channel,
                train_patch_size=train_patch_size,  # adjust for your data below (make patch size as large as possible)
                train_batch_size=train_batch_size,
                train_epochs=epochs,
            )
            printv(conf,1)
            if use_gpu:
                from csbdeep.utils.tf import limit_gpu_memory
                # adjust as necessary: limit GPU memory to be used by TensorFlow to leave some to OpenCL-based computations
                limit_gpu_memory(0.8)

            if model_filename.endswith('.h5'): #Existing model:
                model_filename = abspath(model_filename)
                pretrained_model = dirname(model_filename)
                name = basename(pretrained_model)
                basedir = dirname(pretrained_model)
                printv(f"load the pretrained model {name} from {basedir} ", 0)
                model = StarDist3D(conf, name=name, basedir=basedir)
            else:
                model = StarDist3D(conf, name=basename(model_filename), basedir=os.path.dirname(os.path.abspath(model_filename)))

            median_size = calculate_extents(train_labels, np.median)
            fov = np.array(model._axes_tile_overlap('ZYX'))
            printv(f"median object size:      {median_size}",1)
            printv(f"network field of view :  {fov}",2)
            if any(median_size > fov):
                printv("WARNING: median object size larger than field of view of the neural network.",1)


            #Define Validation Data
            x, y = augmenter(train_data[0], train_labels[0])

            #Launch the training
            model.train(train_data, train_labels, validation_data=([x], [y]), augmenter=augmenter)

            model.optimize_thresholds(train_data,train_labels)

        self.restart(cancel=cancel)
