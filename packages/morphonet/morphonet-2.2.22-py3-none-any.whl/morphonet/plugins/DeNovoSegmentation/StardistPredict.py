# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
from ..functions import read_time_points
from ...tools import printv, read_file
from os.path import isfile, abspath, basename, dirname, join


class StardistPredict(MorphoPlugin):
    """ This plugin uses an intensity image of the nucleus from a local dataset at a specific time point, to compute a
    segmentation of the nucleus, using the 3D Stardist deep learning algorithm.

    \n
    This plugin requires intensity image(s), and is applied on the whole image.

    Parameters
    ----------
    downsampling : int, default :2
        The resolution reduction applied to each axis of the input image before performing segmentation, 1 meaning that
        no reduction is applied. Increasing the reduction factor may reduce segmentation quality
    nms_thresh : float, default :0.3
        Non-max suppression threshold in Stardist
    nuclei_channel: int, default :0
        The desired channel to run stardist on
    prob_thresh: float, default :0.707933
        Mask probability threshold in Stardist
    time_points : string, default: current
        The time range for stardist
    use_tiles: bool, default :True
        Should divide the process in tiles, recommended for big images
    Pretrained_model: string
        the model filename (ex : weights_best.h5) used for the prediction (Default 3D model )
        if the thrshod file isavialble in the folder nms_thresh and prob_thresh will be direcly extract from it

    Reference
    ---------
        Uwe Schmidt, Martin Weigert, Coleman Broaddus, and Gene Myers. Cell Detection with Star-convex Polygons.
        International Conference on Medical Image Computing and Computer-Assisted Intervention (MICCAI), Granada, Spain,
        September 2018.
        https://github.com/stardist/stardist

    """

    def __init__(self):  # PLUGIN DEFINITION
        MorphoPlugin.__init__(self)
        self.set_icon_name("StardistPredict.png")
        self.set_image_name("StardistPredict.png")
        self.set_name("Startdist Predict : Perform nuclei segmentation on intensity images ")
        self.add_inputfield("Nuclei Channel", default=0)
        self.add_inputfield("downsampling", default=2)
        self.add_inputfield("nms_thresh", default=0.3)
        self.add_inputfield("prob_thresh", default=0.707933)
        self.add_inputfield("time points", default="current")
        self.add_dropdown("use tiles ?", ["Yes","No"])
        self.add_filepicker("Pretrained model", default=None, Optional=True)
        self.set_parent("De Novo Segmentation")


    def process(self, t, dataset, objects):  # PLUGIN EXECUTION
        if not self.start(t, dataset, objects, objects_require=False):
            return None

        exec("import tensorflow")

        import numpy as np
        from csbdeep.utils import normalize
        from stardist.models import StarDist3D
        from skimage.transform import resize


        #import tensorflow as tf
        #print(" Devices ? "+str(tf.config.list_physical_devices('GPU')))
        #which = "GPU" if len(tf.config.list_physical_devices('GPU')) >= 1 else "CPU"
        which="CPU"
        printv("Stardist  will run on " + which,1)

        nuclei_channel = int(self.get_inputfield("Nuclei Channel"))
        downsampling = int(self.get_inputfield("downsampling"))
        nms_thresh = float(self.get_inputfield("nms_thresh"))
        prob_thresh = float(self.get_inputfield("prob_thresh"))
        use_tiles=self.get_dropdown("use tiles ?")=="Yes"
        times = read_time_points(self.get_inputfield("time points"), t)
        pretrained_model = self.get_filepicker("Pretrained model")

        cancel=True
        printv("load the stardist 3D model", 0)
        if pretrained_model != "" and isfile(pretrained_model):
            pretrained_model=abspath(pretrained_model)
            #weights=basename(pretrained_model)
            pretrained_model=dirname(pretrained_model)
            name=basename(pretrained_model)
            basedir=dirname(pretrained_model)
            printv(f"load the pretrained model {name} from {basedir} ", 0)
            model=StarDist3D(None, name=name, basedir=basedir)

            #Check if threshold file exist
            thresholds_file=join(basedir,name,"thresholds.json")
            if isfile(thresholds_file):
                txt=read_file(thresholds_file)
                txt=txt[1:-1].split(",")
                prob_thresh=float(txt[0].split(":")[1])
                nms_thresh=float(txt[1].split(":")[1])
                printv(f"found prob_thresh={prob_thresh} and nms_thresh={nms_thresh} ",1)
        else:
            printv("load the 3D demo model ", 0)
            model = StarDist3D.from_pretrained('3D_demo')


        for t in times:
            rawdata = dataset.get_raw(t,nuclei_channel)
            if rawdata is None:
                printv("please specify the rawdata at "+str(t),0)
            else:
                init_shape = rawdata.shape
                if downsampling>1:
                    rawdata=rawdata[::downsampling,::downsampling,::downsampling]

                printv("normalize the rawdata at "+str(t),0)
                rawdata = normalize(rawdata)
                rawdata=np.swapaxes(rawdata,0,2) #ZXY

                printv("predict at "+str(t)+" with nms_thresh="+str(nms_thresh)+' and prob_thresh='+str(prob_thresh),0)
                if use_tiles:
                    n_tiles = model._guess_n_tiles(rawdata)
                    printv("with tiles "+str(n_tiles),1)
                    data, _ = model.predict_instances(rawdata, nms_thresh=nms_thresh, prob_thresh=prob_thresh,n_tiles=n_tiles)
                else:
                    data, _ = model.predict_instances(rawdata,nms_thresh =nms_thresh,prob_thresh =prob_thresh)

                data = np.swapaxes(data, 0, 2)  # ZXY
                nb_cells = len(np.unique(data))
                if nb_cells == 1:  # Only background...
                    printv("did not find any cells", 0)
                else:
                    printv("found " + str(nb_cells) + " cells  at " + str(t), 0)
                    if downsampling > 1: data = resize(data, init_shape, preserve_range=True, order=0)
                    dataset.set_seg(t, data,channel=nuclei_channel,cells_updated=None)
                    cancel = False

        self.restart(cancel=cancel)
