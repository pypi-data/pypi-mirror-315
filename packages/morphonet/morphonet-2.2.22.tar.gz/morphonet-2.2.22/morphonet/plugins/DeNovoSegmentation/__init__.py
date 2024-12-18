# -*- coding: latin-1 -*-
defaultPlugins=[]

from .StardistPredict import StardistPredict
defaultPlugins.append(StardistPredict())

from .StardistTrain import StardistTrain
defaultPlugins.append(StardistTrain())

from .CellposePredict import CellposePredict
defaultPlugins.append(CellposePredict())

from .CellPoseTrain import CellposeTrain
defaultPlugins.append(CellposeTrain())

from .Mars import Mars
defaultPlugins.append(Mars())

from .Binarize import Binarize
defaultPlugins.append(Binarize())

from .BinBox import BinBox
defaultPlugins.append(BinBox())

from .BinCha import BinCha
defaultPlugins.append(BinCha())
