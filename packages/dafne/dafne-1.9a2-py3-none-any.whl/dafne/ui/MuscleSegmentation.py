#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gc

#  Copyright (c) 2021 Dafne-Imaging Team
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
from ..config import GlobalConfig, load_config
load_config()

import tensorflow as tf

if GlobalConfig['USE_GPU_FOR'] == 'SAM Refinement':
    # force CPU for tensorflow
    tf.config.set_visible_devices([], 'GPU')
elif GlobalConfig['USE_GPU_FOR'] == 'Both (careful!)':
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            tf.config.experimental.set_virtual_device_configuration(
                gpus[0],
                [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=GlobalConfig['TENSORFLOW_MEMORY_ALLOCATION']*1000)])
        except RuntimeError as e:
            # Virtual devices must be set before GPUs have been initialized
            print(e)

import matplotlib
from dafne_dl.common.biascorrection import biascorrection_image
from matplotlib.patches import Rectangle
from voxel import NiftiWriter
from scipy.interpolate import interp1d
from skimage.morphology import area_opening, area_closing

from .WhatsNew import NewsChecker, WhatsNewDialog
from dicomUtils.misc import realign_medical_volume, dosma_volume_from_path, reorient_data_ui, \
    get_nifti_orientation
from . import GenericInputDialog
from ..utils.mask_to_spline import mask_average, mask_to_trivial_splines, masks_splines_to_splines_masks
from ..utils.pySplineInterp import SplineInterpROIClass
from ..utils.resource_utils import get_resource_path
from ..utils.sam_mask_refine import enhance_mask

matplotlib.use("Qt5Agg")

import os, time, math, sys

from .ToolboxWindow import ToolboxWindow
from dicomUtils.ui.pyDicomView import ImageShow
from ..utils.mask_utils import save_npy_masks, save_npz_masks, save_dicom_masks, save_nifti_masks, \
    save_single_dicom_dataset, save_single_nifti
from dafne_dl.misc import calc_dice_score
import matplotlib.pyplot as plt
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import shutil
from datetime import datetime
from ..utils.ROIManager import ROIManager
from .. import utils
sys.modules['utils'] = utils # to make pickle work

import numpy as np
import scipy.ndimage as ndimage
from scipy.ndimage.morphology import binary_dilation, binary_erosion
from ..utils import compressed_pickle as pickle
import os.path
from collections import deque
import functools
import csv

from ..utils.ThreadHelpers import separate_thread_decorator

from .BrushPatches import SquareBrush, PixelatedCircleBrush
from .ContourPainter import ContourPainter
import traceback

from dafne_dl.LocalModelProvider import LocalModelProvider
from dafne_dl.RemoteModelProvider import RemoteModelProvider
from dafne_dl.MixedModelProvider import MixedModelProvider

from ..utils.RegistrationManager import RegistrationManager

import requests

try:
    import SimpleITK as sitk # this requires simpleelastix!
except:
    sitk = None

try:
    import radiomics
except:
    radiomics = None

import subprocess

if os.name == 'posix':
    def checkCapsLock():
        return (int(subprocess.check_output('xset q | grep LED', shell=True)[65]) & 1) == 1
elif os.name == 'nt':
    import ctypes

    hllDll = ctypes.WinDLL("User32.dll")


    def checkCapsLock():
        return ((hllDll.GetKeyState(0x14) & 1) == 1)
else:
    def checkCapsLock():
        return False

try:
    QString("")
except:
    def QString(s):
        return s


INTENSITY_AWARE_THRESHOLD = 0.5
ACTIONS_TO_REMOVE = 'Subplots', 'Customize', 'Save'

def make_excepthook(muscle_segmentation_instance):
    def excepthook(exctype, value, traceback):
        muscle_segmentation_instance.alert(f"An error occurred. Please check the logs in {os.path.dirname(GlobalConfig['ERROR_LOG_FILE'])} for more information. The current ROIs will be saved.")
        muscle_segmentation_instance.saveROIPickle()
        muscle_segmentation_instance.close_slot()
        return sys.__excepthook__(exctype, value, traceback)
    return excepthook

def makeMaskLayerColormap(color):
    return matplotlib.colors.ListedColormap(np.array([
        [0, 0, 0, 0],
        [*color[:3],1]]))


def snapshotSaver(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self.saveSnapshot()
        func(self, *args, **kwargs)

    return wrapper


class MuscleSegmentation(ImageShow, QObject):

    undo_possible = pyqtSignal(bool)
    redo_possible = pyqtSignal(bool)
    splash_signal = pyqtSignal(bool, int, int, str)
    reblit_signal = pyqtSignal()
    redraw_signal = pyqtSignal()
    reduce_brush_size = pyqtSignal()
    increase_brush_size = pyqtSignal()
    alert_signal = pyqtSignal(str, str)
    undo_signal = pyqtSignal()
    redo_signal = pyqtSignal()

    mask_changed = pyqtSignal(list, np.ndarray)
    mask_slice_changed = pyqtSignal(int, np.ndarray)
    volume_loaded_signal = pyqtSignal(list, np.ndarray)

    def __init__(self, *args, **kwargs):
        self.suppressRedraw = False
        ImageShow.__init__(self, *args, **kwargs)
        QObject.__init__(self)

        self.shortcuts = {
            'z': self.undo_signal.emit,
            'y': self.redo_signal.emit,
            'g': self.gotoImageDialog
        }

        self.news_checker = NewsChecker()
        self.news_checker.news_ready.connect(self.show_news)
        self.news_checker.check_news()


        self.fig.canvas.mpl_connect('close_event', self.closeCB)
        # self.instructions = "Shift+click: add point, Shift+dblclick: optimize/simplify, Ctrl+click: remove point, Ctrl+dblclick: delete ROI, n: propagate fw, b: propagate back"

        if 'Elastix' in dir(sitk):
            self.registration_available = True
        else:
            print("Elastix is not available")
            self.registration_available = False

        self.app = None

        self.setupToolbar()

        main_window = self.fig.canvas.parent()
        main_window.setWindowTitle("Dafne Main Window")
        with get_resource_path('dafne_logo.png') as logo_path:
            main_window.setWindowIcon(QIcon(logo_path))

        self.roiManager = None

        self.wacom = False

        self.saveDicom = False

        self.model_provider = None
        self.dl_classifier = None
        self.dl_segmenters = {}
        self.model_details = {}

        # self.fig.canvas.setCursor(Qt.BlankCursor)

        # self.setCmap('viridis')
        self.extraOutputParams = []

        self.registrationManager = None

        self.hideRois = False
        self.editMode = ToolboxWindow.EDITMODE_MASK
        self.resetInternalState()

        self.fig.canvas.mpl_connect('resize_event', self.resizeCB)
        self.reblit_signal.connect(self.do_reblit)
        self.redraw_signal.connect(self.do_redraw)
        self.undo_signal.connect(self.undo)
        self.redo_signal.connect(self.redo)

        self.separate_thread_running = False

        toolbar = self.fig.canvas.toolbar
        actions = toolbar.actions()
        for action in actions:
            if action.text() in ACTIONS_TO_REMOVE:
                toolbar.removeAction(action)


        # disable keymapping from matplotlib - avoid pan and zoom
        for key in list(plt.rcParams):
            if 'keymap' in key and 'zoom' not in key and 'pan' not in key:
                plt.rcParams[key] = []
        sys.excepthook = make_excepthook(self)

    @pyqtSlot(list, str)
    def show_news(self, news, index_address):
        d = WhatsNewDialog(news, index_address)
        d.exec()

    def get_app(self):
        if not self.app:
            self.app = QApplication.instance()
        return self.app


    def resizeCB(self, event):
        self.resetBlitBg()
        self.redraw()

    def resetBlitBg(self):
        self.blitBg = None


    @pyqtSlot()
    def resetModelProvider(self):
        available_models = None
        filter_classes = False
        self.model_details = {}
        if GlobalConfig['MODEL_PROVIDER'] == 'Local':
            model_provider = LocalModelProvider(GlobalConfig['MODEL_PATH'], GlobalConfig['TEMP_UPLOAD_DIR'])
            available_models = model_provider.available_models()
        else:
            if GlobalConfig['MODEL_PROVIDER'] == 'Remote':
                ProviderClass = RemoteModelProvider
            else:
                ProviderClass = MixedModelProvider
                print('Using mixed model provider')
            url = GlobalConfig['SERVER_URL']
            if not url.endswith('/'):
                url += '/'
            model_provider = ProviderClass(GlobalConfig['MODEL_PATH'], url, GlobalConfig['API_KEY'], GlobalConfig['TEMP_UPLOAD_DIR'])
            fallback = False
            try:
                available_models = model_provider.available_models()
                filter_classes = True
            except PermissionError:
                self.alert("Error in using Remote Model. Please check your API key. Falling back to Local")
                fallback = True
            except requests.exceptions.ConnectionError:
                self.alert("Remote server unavailable. Falling back to Local")
                fallback = True
            except requests.exceptions.InvalidURL:
                self.alert("Invalid URL. Falling back to Local")
                fallback = True
            else:
                if available_models is None:
                    self.alert("Error in using Remote Model Loading. Falling back to Local")
                    fallback = True

            if fallback:
                GlobalConfig['MODEL_PROVIDER'] = 'Local'
                model_provider = LocalModelProvider(GlobalConfig['MODEL_PATH'], GlobalConfig['TEMP_UPLOAD_DIR'])
                filter_classes = False
                available_models = model_provider.available_models()

        try:
            local_model_list = self.model_provider.get_local_models()
        except AttributeError:
            local_model_list = []

        GlobalConfig['ENABLED_MODELS'].extend(local_model_list)
        self.setModelProvider(model_provider)

        print(available_models)
        self.setAvailableClasses(available_models, filter_classes)

    @pyqtSlot()
    def configChanged(self):
        self.scroll_debounce_time = float(GlobalConfig['MOUSE_SCROLL_DEBOUNCE_TIME'])/1000.0
        self.resetInterface()
        self.resetModelProvider()

    def resetInterface(self):
        self.blitBg = None
        self.blitXlim = None
        self.blitYlim = None
        try:
            self.brush_patch.remove()
        except:
            pass

        self.brush_patch = None

        try:
            self.removeMasks()
        except:
            pass

        try:
            self.removeSubregion()
        except:
            pass

        self.maskImPlot = None
        self.maskOtherImPlot = None
        self.activeMask = None
        self.otherMask = None
        self.region_rectangle = None

        self.roiColor = GlobalConfig['ROI_COLOR']
        self.roiOther = GlobalConfig['ROI_OTHER_COLOR']
        self.roiSame = GlobalConfig['ROI_SAME_COLOR']
        self.interpolation = GlobalConfig['INTERPOLATION']
        try:
            self.imPlot.set_interpolation(self.interpolation)
        except:
            pass

        self.setCmap(GlobalConfig['COLORMAP'])

        self.mask_layer_colormap = makeMaskLayerColormap(self.roiColor)
        self.mask_layer_other_colormap = makeMaskLayerColormap(self.roiOther)

        try:
            self.removeContours()
        except:
            pass

        self.activeRoiPainter = ContourPainter(self.roiColor, GlobalConfig['ROI_CIRCLE_SIZE'])
        self.sameRoiPainter = ContourPainter(self.roiSame, 0.1)
        self.otherRoiPainter = ContourPainter(self.roiOther, 0.1)

        try:
            self.updateContourPainters()
        except:
            pass

        self.redraw()

    def resetInternalState(self):
        self.imList = []
        self.resolution = [1, 1, 1]
        self.curImage = 0
        self.classifications = []
        self.lastsave = datetime.now()

        self.roiChanged = {}
        self.history = deque(maxlen=GlobalConfig['HISTORY_LENGTH'])
        self.historyHead = None
        self.currentHistoryPoint = 0

        self.registrationManager = None

        self.resetModelProvider()
        self.resetInterface()
        self.slicesUsedForTraining = set()

        self.roiManager = None

        self.currentPoint = None
        self.translateDelta = None
        self.rotationDelta = None
        self.scroll_debounce_time = float(GlobalConfig['MOUSE_SCROLL_DEBOUNCE_TIME'])/1000.0
        self.threshold_mask = None


    #############################################################################################
    ###
    ### Toolbar interaction
    ###
    ##############################################################################################

    def setupToolbar(self):
        self.toolbox_window = ToolboxWindow(self, activate_registration=self.registration_available, activate_radiomics= (radiomics is not None))
        self.toolbox_window.show()

        self.toolbox_window.editmode_changed.connect(self.changeEditMode)

        self.toolbox_window.roi_added.connect(self.addRoi)
        self.toolbox_window.subroi_added.connect(self.addSubRoi)

        self.toolbox_window.roi_deleted.connect(self.removeRoi)
        self.toolbox_window.subroi_deleted.connect(self.removeSubRoi)

        self.toolbox_window.roi_changed.connect(self.changeRoi)

        self.toolbox_window.roi_clear.connect(self.clearCurrentROI)

        self.toolbox_window.do_autosegment.connect(self.doSegmentationMultislice)

        self.toolbox_window.classification_changed.connect(self.changeClassification)
        self.toolbox_window.classification_change_all.connect(self.changeAllClassifications)

        self.toolbox_window.undo.connect(self.undo)
        self.toolbox_window.redo.connect(self.redo)
        self.undo_possible.connect(self.toolbox_window.undo_enable)
        self.redo_possible.connect(self.toolbox_window.redo_enable)

        self.toolbox_window.contour_simplify.connect(self.simplify)
        self.toolbox_window.contour_optimize.connect(self.optimize)

        self.toolbox_window.calculate_transforms.connect(self.calcTransforms)
        self.toolbox_window.contour_propagate_fw.connect(self.propagate)
        self.toolbox_window.contour_propagate_bw.connect(self.propagateBack)

        self.toolbox_window.interpolate_mask.connect(self.interpolate)
        self.toolbox_window.interpolate_block.connect(self.interpolate_block)

        self.toolbox_window.roi_import.connect(self.loadROIPickle)
        self.toolbox_window.roi_export.connect(self.saveROIPickle)
        self.toolbox_window.data_open.connect(self.loadDirectory)
        self.toolbox_window.data_save_as_nifti.connect(self.save_data_as_reoriented_nifti)
        self.toolbox_window.data_reorient.connect(self.reorient_data)
        self.toolbox_window.masks_export.connect(self.saveResults)
        self.toolbox_window.bundle_export.connect(self.saveBundle)

        self.toolbox_window.roi_copy.connect(self.copyRoi)
        self.toolbox_window.roi_combine.connect(self.combineRoi)
        self.toolbox_window.roi_multi_combine.connect(self.combineMultiRoi)
        self.toolbox_window.roi_remove_overlap.connect(self.roiRemoveOverlap)

        self.toolbox_window.statistics_calc.connect(self.saveStats)
        self.toolbox_window.statistics_calc_slicewise.connect(self.saveStats_singleslice)
        self.toolbox_window.radiomics_calc.connect(self.saveRadiomics)

        self.toolbox_window.incremental_learn.connect(self.incrementalLearnStandalone)

        self.toolbox_window.mask_import.connect(self.loadMask)

        self.splash_signal.connect(self.toolbox_window.set_splash)
        self.interface_disabled = False
        self.splash_signal.connect(self.disableInterface)

        self.toolbox_window.mask_grow.connect(self.maskGrow)
        self.toolbox_window.mask_shrink.connect(self.maskShrink)
        self.toolbox_window.mask_fill_holes.connect(self.maskFillHoles)
        self.toolbox_window.mask_despeckle.connect(self.maskDespeckle)
        self.toolbox_window.mask_auto_threshold.connect(self.maskAutoThreshold)
        self.toolbox_window.sam_autorefine.connect(self.samAutoRefine)

        self.toolbox_window.config_changed.connect(self.configChanged)
        self.toolbox_window.data_upload.connect(self.uploadData)

        self.toolbox_window.model_import.connect(self.importModel)

        self.reduce_brush_size.connect(self.toolbox_window.reduce_brush_size)
        self.increase_brush_size.connect(self.toolbox_window.increase_brush_size)
        self.toolbox_window.brush_changed.connect(self.updateBrush)

        self.alert_signal.connect(self.toolbox_window.alert)
        self.toolbox_window.quit.connect(self.close_slot)

        self.toolbox_window.reblit.connect(self.do_reblit)
        self.toolbox_window.redraw.connect(self.do_redraw)

        self.toolbox_window.delete_subregion.connect(self.delete_current_subregion)
        self.toolbox_window.delete_all_subregions.connect(self.delete_all_subregions)
        self.toolbox_window.copy_all_subregions.connect(self.copy_all_subregions)

        self.toolbox_window.show_3D_viewer_signal.connect(self.emit_mask_changed)
        self.mask_changed.connect(self.toolbox_window.viewer3D.set_spacing_and_data)
        self.mask_slice_changed.connect(self.toolbox_window.viewer3D.set_slice)
        self.volume_loaded_signal.connect(self.toolbox_window.viewer3D.set_spacing_and_anatomy)

    def setSplash(self, is_splash, current_value = 0, maximum_value = 1, text= ""):
        self.splash_signal.emit(is_splash, current_value, maximum_value, text)

    #dis/enable interface callbacks
    @pyqtSlot(bool, int, int, str)
    def disableInterface(self, disable, unused1, unused2, txt):
        if self.interface_disabled == disable: return
        self.interface_disabled = disable
        if disable:
            self.disconnectSignals()
        else:
            self.connectSignals()

    @pyqtSlot(str)
    def changeEditMode(self, mode):
        print("Changing edit mode")
        self.setSplash(True, 0, 1)
        self.editMode = mode
        roi_name = self.getCurrentROIName()
        if roi_name:
            self.updateRoiList()
            self.toolbox_window.set_current_roi(roi_name)
            if mode == ToolboxWindow.EDITMODE_MASK:
                self.removeContours()
                self.updateMasksFromROIs()
            else:
                self.removeMasks()
                self.updateContourPainters()
            self.redraw()
        self.setSplash(False, 1, 1)

    def setState(self, state):
        self.state = state

    def getState(self):
        if self.toolbox_window.valid_roi(): return 'MUSCLE'
        return 'INACTIVE'

    def updateRoiList(self):
        if not self.roiManager: return
        roiDict = {}
        imageN = int(self.curImage)
        for roiName in self.roiManager.get_roi_names():
            if self.editMode == ToolboxWindow.EDITMODE_MASK:
                if not self.roiManager.contains(roiName, imageN):
                    self.roiManager.add_mask(roiName, imageN)
                n_subrois = 1
            else:
                if not self.roiManager.contains(roiName, imageN) or self.roiManager.get_roi_mask_pair(roiName,
                                                                                                      imageN).get_subroi_len() == 0:
                    self._addSubRoi_internal(roiName, imageN)
                n_subrois = self.roiManager.get_roi_mask_pair(roiName, imageN).get_subroi_len()
            roiDict[roiName] = n_subrois  # dict: roiname -> n subrois per slice
        self.toolbox_window.set_rois_list(roiDict)
        self.updateContourPainters()
        self.updateMasksFromROIs()

    def alert(self, text, type="Warning"):
        self.alert_signal.emit(text, type)

    #############################################################################################
    ###
    ### History
    ###
    #############################################################################################

    def saveSnapshot(self, save_head = False):
        #print("Saving snapshot")
        if self.roiManager is None:
            try:
                self.roiManager = ROIManager(self.imList[0].shape)
            except:
                return
        current_point = pickle.dumps(self.roiManager)
        if save_head:
            #print("Saving head state")
            self.historyHead = current_point
        else:
            # clear history until the current point, so we can't redo anymore
            while self.currentHistoryPoint > 0:
                self.history.popleft()
                self.currentHistoryPoint -= 1
            self.history.appendleft(current_point)
            self.historyHead = None

        self.undo_possible.emit(self.canUndo())
        self.redo_possible.emit(self.canRedo())

    def canUndo(self):
        #print("Can undo history point", self.currentHistoryPoint, "len history", len(self.history))
        return self.currentHistoryPoint < len(self.history)

    def canRedo(self):
        return self.currentHistoryPoint > 0 or self.historyHead is not None

    def _changeHistory(self):
        #print('Current history point', self.currentHistoryPoint, 'history len', len(self.history))
        if self.currentHistoryPoint == 0 and self.historyHead is None:
            print('Warning: invalid redo')
            return
        roiName = self.getCurrentROIName()
        subRoiNumber = self.getCurrentSubroiNumber()
        self.clearAllROIs()
        if self.currentHistoryPoint == 0:
            #print("loading head")
            self.roiManager = pickle.loads(self.historyHead)
            self.historyHead = None
        else:
            #print("loading", self.currentHistoryPoint-1)
            self.roiManager = pickle.loads(self.history[self.currentHistoryPoint-1])

        self.updateRoiList()
        if self.roiManager.contains(roiName):
            if self.toolbox_window.get_edit_mode() == ToolboxWindow.EDITMODE_MASK:
                self.toolbox_window.set_current_roi(roiName, -1)
            else:
                if subRoiNumber < self.roiManager.get_roi_mask_pair(roiName, self.curImage).get_subroi_len():
                    self.toolbox_window.set_current_roi(roiName, subRoiNumber)
                else:
                    self.toolbox_window.set_current_roi(roiName, 0)
        self.activeMask = None
        self.otherMask = None
        self.redraw()
        self.undo_possible.emit(self.canUndo())
        self.redo_possible.emit(self.canRedo())

    @pyqtSlot()
    def undo(self):
        if not self.canUndo(): return
        if self.currentHistoryPoint == 0:
            self.saveSnapshot(save_head=True)  # push current status into the history for redo
        self.currentHistoryPoint += 1
        self._changeHistory()

    @pyqtSlot()
    def redo(self):
        if not self.canRedo(): return
        self.currentHistoryPoint -= 1
        self._changeHistory()

    ############################################################################################################
    ###
    ### ROI management
    ###
    #############################################################################################################

    def getRoiFileName(self):
        if self.basename:
            roi_fname = self.basename + '.' + GlobalConfig['ROI_FILENAME']
        else:
            roi_fname = GlobalConfig['ROI_FILENAME']
        return os.path.join(self.basepath, roi_fname)

    def clearAllROIs(self):
        self.roiManager.clear()
        self.updateRoiList()
        self.reblit()

    def clearSubrois(self, name, sliceN):
        self.roiManager.clear(name, sliceN)
        self.updateRoiList()
        self.reblit()

    @pyqtSlot(str)
    @snapshotSaver
    def removeRoi(self, roi_name):
        self.roiManager.clear(roi_name)
        self.updateRoiList()
        self.reblit()

    @pyqtSlot(int)
    @snapshotSaver
    def removeSubRoi(self, subroi_number):
        current_name, _ = self.toolbox_window.get_current_roi_subroi()
        self.roiManager.clear_subroi(current_name, int(self.curImage), subroi_number)
        self.updateRoiList()
        self.reblit()

    @pyqtSlot(str)
    @snapshotSaver
    def addRoi(self, roiName):
        if self.editMode == ToolboxWindow.EDITMODE_MASK:
            self.roiManager.add_mask(roiName, int(self.curImage))
        else:
            self.roiManager.add_roi(roiName, int(self.curImage))
        self.updateRoiList()
        self.toolbox_window.set_current_roi(roiName, 0)
        self.updateMasksFromROIs()
        self.updateContourPainters()
        self.reblit()
        self.emit_mask_changed()

    def _addSubRoi_internal(self, roi_name=None, imageN=None):
        if not roi_name:
            roi_name, _ = self.toolbox_window.get_current_roi_subroi()
        if imageN is None:
            imageN = int(self.curImage)
        self.roiManager.add_subroi(roi_name, imageN)

    @pyqtSlot()
    #@snapshotSaver this generates too many calls; anyway we want to add the subroi to the history
    # when something happens to it
    def addSubRoi(self, roi_name=None, imageN=None):
        if not roi_name:
            roi_name, _ = self.toolbox_window.get_current_roi_subroi()
        if imageN is None:
            imageN = int(self.curImage)
        self._addSubRoi_internal(roi_name, imageN)
        self.updateRoiList()
        self.toolbox_window.set_current_roi(roi_name, self.roiManager.get_roi_mask_pair(roi_name,
                                                                                        imageN).get_subroi_len() - 1)
        self.reblit()

    @pyqtSlot(str, int)
    def changeRoi(self, roi_name, subroi_index):
        """ Change the active ROI """
        self.activeMask = None
        self.otherMask = None
        self.updateContourPainters()
        self.reblit()
        self.emit_mask_changed()

    def getCurrentROIName(self):
        """ Gets the name of the ROI selected in the toolbox """
        return self.toolbox_window.get_current_roi_subroi()[0]

    def getCurrentSubroiNumber(self):
        return self.toolbox_window.get_current_roi_subroi()[1]

    def _getSetCurrentROI(self, offset=0, newROI=None):
        """ Generic get/set for ROI objects inside the roi manager """
        if not self.getCurrentROIName():
            return None

        imageN = int(self.curImage + offset)
        curName = self.getCurrentROIName()
        curSubroi = self.getCurrentSubroiNumber()

        #print("Get set ROI", curName, imageN, curSubroi)

        return self.roiManager._get_set_roi(curName, imageN, curSubroi, newROI)

    def getCurrentROI(self, offset=0):
        """ Get current ROI object """
        return self._getSetCurrentROI(offset)

    def setCurrentROI(self, r, offset=0):
        self._getSetCurrentROI(offset, r)

    def getCurrentMask(self, offset=0):
        roi_name = self.getCurrentROIName()
        if not self.roiManager or not roi_name:
            return None
        return self.roiManager.get_mask(roi_name, int(self.curImage + offset))

    def setCurrentMask(self, mask, offset=0):
        roi_name = self.getCurrentROIName()
        if not self.roiManager or not roi_name:
            return None
        self.roiManager.set_mask(roi_name, int(self.curImage + offset), mask)

    def getCurrentSubregion(self, offset=0):
        if not self.roiManager:
            return None
        imageN = int(self.curImage + offset)
        return self.roiManager.get_autosegment_subregion(imageN)

    def setCurrentSubregion(self, subregion, offset=0):
        if not self.roiManager:
            return
        imageN = int(self.curImage + offset)
        if subregion is None:
            self.roiManager.clear_autosegment_subregion(imageN)
        else:
            self.roiManager.set_autosegment_subregion(imageN, subregion)

    def calcOutputData(self, setSplash=False):
        imSize = self.image.shape

        allMasks = {}
        diceScores = []
        n_voxels = []

        dataForTraining = {}
        segForTraining = {}

        roi_names = self.roiManager.get_roi_names()
        current_roi_index = 0

        slices_with_rois = set()

        originalSegmentationMasks = {}

        for roiName in self.roiManager.get_roi_names():
            if setSplash:
                self.setSplash(True, current_roi_index, len(roi_names), "Calculating maps...")
                current_roi_index += 1
            masklist = []
            for imageIndex in range(len(self.imList)):
                roi = np.zeros(imSize, dtype=np.uint8)
                if self.roiManager.contains(roiName, imageIndex):
                    roi = self.roiManager.get_mask(roiName, imageIndex)

                if roi.any():
                    slices_with_rois.add(imageIndex) # add the slice to the set if any voxel is nonzero
                    if imageIndex not in originalSegmentationMasks and self.classifications[imageIndex] != 'None':
                        #print(imageIndex)
                        originalSegmentationMasks[imageIndex] = self.getSegmentedMasks(imageIndex, False, True)

                masklist.append(roi)
                try:
                    originalSegmentation = originalSegmentationMasks[imageIndex][roiName]
                except KeyError:
                    originalSegmentation = None

                if originalSegmentation is not None:
                    diceScores.append(calc_dice_score(originalSegmentation, roi))
                    n_voxels.append(np.sum(roi))
                    #print(diceScores)

                # TODO: maybe add this to the training according to the dice score?
                classification_name = self.classifications[imageIndex]
                if classification_name not in dataForTraining:
                    dataForTraining[classification_name] = {}
                    segForTraining[classification_name] = {}
                if imageIndex not in dataForTraining[classification_name]:
                    dataForTraining[classification_name][imageIndex] = self.imList[imageIndex]
                    segForTraining[classification_name][imageIndex] = {}

                segForTraining[classification_name][imageIndex][roiName] = roi

            npMask = np.transpose(np.stack(masklist), [1, 2, 0])
            allMasks[roiName] = npMask

        # cleanup empty slices and slices that were already used for training
        for classification_name in dataForTraining:
            print('Slices available for', classification_name, ':', list(dataForTraining[classification_name].keys()))
            for imageIndex in list(dataForTraining[classification_name]): # get a list of keys to be able to delete from dict
                if imageIndex not in slices_with_rois or imageIndex in self.slicesUsedForTraining:
                    del dataForTraining[classification_name][imageIndex]
                    del segForTraining[classification_name][imageIndex]
            print('Slices after cleanup', list(dataForTraining[classification_name].keys()))


        diceScores = np.array(diceScores)
        n_voxels =np.array(n_voxels)
        #print(diceScores)
        if np.sum(n_voxels) == 0:
            average_dice = -1.0
        else:
            average_dice = np.average(diceScores, weights=n_voxels)
        print("Average Dice score", average_dice)
        return allMasks, dataForTraining, segForTraining, average_dice

    @pyqtSlot(str, str, bool)
    @snapshotSaver
    def copyRoi(self, originalName, newName, makeCopy=True):
        if makeCopy:
            self.roiManager.copy_roi(originalName, newName)
        else:
            self.roiManager.rename_roi(originalName, newName)
        self.updateRoiList()

    def _getCombineFunction(self, operator):
        if operator == 'Union':
            combine_fn = np.logical_or
        elif operator == 'Subtraction':
            combine_fn = lambda x,y: np.logical_and(x, np.logical_not(y))
        elif operator == 'Intersection':
            combine_fn = np.logical_and
        elif operator == 'Exclusion':
            combine_fn = np.logical_xor
        return combine_fn

    @pyqtSlot(str, str, str, str)
    @snapshotSaver
    def combineRoi(self, roi1, roi2, operator, dest_roi):
        self.combineMultiRoi([roi1, roi2], operator, dest_roi)

    @pyqtSlot(list, str, str)
    @snapshotSaver
    def combineMultiRoi(self, roi_list, operator, dest_roi):
        combine_fn = self._getCombineFunction(operator)
        if len(roi_list) < 2:
            return
        self.roiManager.generic_roi_combine(roi_list[0], roi_list[1], combine_fn, dest_roi)
        for i in range(2, len(roi_list)):
            self.roiManager.generic_roi_combine(dest_roi, roi_list[i], combine_fn, dest_roi)
        self.updateMasksFromROIs()
        self.updateContourPainters()
        self.updateRoiList()

    @pyqtSlot()
    @snapshotSaver
    def roiRemoveOverlap(self):
        curRoiName = self.getCurrentROIName()
        currentMask = self.getCurrentMask()
        currentNotMask = np.logical_not(currentMask)
        for key_tuple, mask in self.roiManager.all_masks(image_number=self.curImage):
            if key_tuple[0] == curRoiName: continue
            self.roiManager.set_mask(key_tuple[0], key_tuple[1], np.logical_and(mask, currentNotMask))

        self.updateMasksFromROIs()
        self.reblit()

    @pyqtSlot()
    def delete_current_subregion(self):
        self.setCurrentSubregion(None)
        self.reblit()

    @pyqtSlot()
    def delete_all_subregions(self):
        if self.roiManager is None:
            return
        self.roiManager.clear_all_autosegment_subregions()
        self.removeSubregion()
        self.redraw()

    @pyqtSlot()
    def copy_all_subregions(self):
        subregion = self.getCurrentSubregion()
        if subregion is None:
            return

        for image_index in range(len(self.imList)):
            self.roiManager.set_autosegment_subregion(image_index, subregion)


    #########################################################################################
    ###
    ### ROI modifications
    ###
    #########################################################################################

    @snapshotSaver
    def simplify(self):
        r = self.getCurrentROI()
        self.setCurrentROI(r.getSimplifiedSpline())
        self.redraw() # this also updates the contour painters

    @snapshotSaver
    def optimize(self):
        r = self.getCurrentROI()
        center = r.getCenterOfMass()
        if center is None:
            print("No roi to optimize!")
            return

        newKnots = []
        for index, knot in enumerate(r.knots):
            # newKnot = self.optimizeKnot(center, knot)
            # newKnot = self.optimizeKnot2(knot, r.getKnot(index-1), r.getKnot(index+1))
            newKnot = self.optimizeKnot3(r, index)
            # newKnot = self.optimizeKnotDL(knot)
            newKnots.append(newKnot)

        for index, knot in enumerate(r.knots):
            r.replaceKnot(index, newKnots[index])
        self.reblit()

    # optimizes a knot along an (approximatE) normal to the curve
    def optimizeKnot2(self, knot, prevKnot, nextKnot):

        print("optimizeKnot2")

        optim_region = 5
        optim_region_points = optim_region * 4  # subpixel resolution

        # special case vertical line
        if prevKnot[0] == nextKnot[0]:
            # optimize along a horizontal line
            ypoints = knot[1] * np.ones((2 * optim_region_points))

            # define inside/outside
            if knot[0] < prevKnot[0]:
                xpoints = np.linspace(knot[0] + optim_region, knot[0] - optim_region, 2 * optim_region_points)
            else:
                xpoints = np.linspace(knot[0] - optim_region, knot[0] + optim_region, 2 * optim_region_points)
            z = ndimage.map_coordinates(self.image, np.vstack((ypoints, xpoints))).astype(np.float32)
        elif prevKnot[1] == nextKnot[1]:  # special case horizontal line
            # optimize along a horizontal line
            xpoints = knot[0] * np.ones((2 * optim_region_points))
            if knot[1] < prevKnot[1]:
                ypoints = np.linspace(knot[1] + optim_region, knot[1] - optim_region, 2 * optim_region_points)
            else:
                ypoints = np.linspace(knot[1] - optim_region, knot[1] + optim_region, 2 * optim_region_points)
            z = ndimage.map_coordinates(self.image, np.vstack((ypoints, xpoints))).astype(np.float32)
        else:
            slope = (nextKnot[1] - prevKnot[1]) / (nextKnot[0] - prevKnot[0])
            slope_perpendicular = -1 / slope
            x_dist = np.sqrt(optim_region / (
                    slope_perpendicular ** 2 + 1))  # solving the system (y1-y0) = m(x1-x0) and (y1-y0)^2 + (x1-x0)^2 = d

            # define inside*outside perimeter. Check line intersection. Is this happening on the right or on the left of the point? Right: go from high x to low x
            # x_intersection = (slope_perpendicular*knot[0] - knot[1] - slope*prevKnot[0] + prevKnot[1])/(slope_perpendicular-slope)
            # print knot[0]
            # print x_intersection
            # if x_intersection > knot[0]: x_dist = -x_dist

            x_min = knot[0] - x_dist
            x_max = knot[0] + x_dist
            y_min = knot[1] - slope_perpendicular * x_dist
            y_max = knot[1] + slope_perpendicular * x_dist
            xpoints = np.linspace(x_min, x_max, 2 * optim_region_points)
            ypoints = np.linspace(y_min, y_max, 2 * optim_region_points)
            z = ndimage.map_coordinates(self.image, np.vstack((ypoints, xpoints))).astype(np.float32)
        diffz = np.diff(z) / (np.abs(np.linspace(-optim_region, +optim_region, len(z) - 1)) + 1) ** (1 / 2)

        #            f = plt.figure()
        #            plt.subplot(121)
        #            plt.plot(z)
        #            plt.subplot(122)
        #            plt.plot(diffz)

        # find sharpest bright-to-dark transition. Maybe check if there are similar transitions in the line and only take the closest one
        minDeriv = np.argmax(np.abs(diffz)) + 1
        return (xpoints[minDeriv], ypoints[minDeriv])

    # optimizes a knot along an (approximate) normal to the curve, going from inside the ROI to outside
    def optimizeKnot3(self, roi, knotIndex):

        knot = roi.getKnot(knotIndex)
        nextKnot = roi.getKnot(knotIndex + 1)
        prevKnot = roi.getKnot(knotIndex - 1)

        # print "optimizeKnot3"

        optim_region = 5
        optim_region_points = optim_region * 4  # subpixel resolution

        # special case vertical line
        if prevKnot[0] == nextKnot[0]:
            # optimize along a horizontal line
            ypoints = knot[1] * np.ones((2 * optim_region_points))

            # define inside/outside
            if knot[0] < prevKnot[0]:
                xpoints = np.linspace(knot[0] + optim_region, knot[0] - optim_region, 2 * optim_region_points)
            else:
                xpoints = np.linspace(knot[0] - optim_region, knot[0] + optim_region, 2 * optim_region_points)
            z = ndimage.map_coordinates(self.image, np.vstack((ypoints, xpoints))).astype(np.float32)
        elif prevKnot[1] == nextKnot[1]:  # special case horizontal line
            # optimize along a horizontal line
            xpoints = knot[0] * np.ones((2 * optim_region_points))
            if knot[1] < prevKnot[1]:
                ypoints = np.linspace(knot[1] + optim_region, knot[1] - optim_region, 2 * optim_region_points)
            else:
                ypoints = np.linspace(knot[1] - optim_region, knot[1] + optim_region, 2 * optim_region_points)
            z = ndimage.map_coordinates(self.image, np.vstack((ypoints, xpoints))).astype(np.float32)
        else:
            slope = (nextKnot[1] - prevKnot[1]) / (nextKnot[0] - prevKnot[0])
            slope_perpendicular = -1 / slope
            x_dist = np.sqrt(optim_region / (
                    slope_perpendicular ** 2 + 1))  # solving the system (y1-y0) = m(x1-x0) and (y1-y0)^2 + (x1-x0)^2 = d

            # this point is just on the right of our knot.
            test_point_x = knot[0] + 1
            test_point_y = knot[1] + slope_perpendicular * 1

            # if the point is inside the ROI, then calculate the line from right to left
            if roi.isPointInside((test_point_x, test_point_y)):
                x_dist = -x_dist

            # define inside*outside perimeter. Check line intersection. Is this happening on the right or on the left of the point? Right: go from high x to low x
            # x_intersection = (slope_perpendicular*knot[0] - knot[1] - slope*prevKnot[0] + prevKnot[1])/(slope_perpendicular-slope)
            # print knot[0]
            # print x_intersection
            # if x_intersection > knot[0]: x_dist = -x_dist

            x_min = knot[0] - x_dist
            x_max = knot[0] + x_dist
            y_min = knot[1] - slope_perpendicular * x_dist
            y_max = knot[1] + slope_perpendicular * x_dist
            xpoints = np.linspace(x_min, x_max, 2 * optim_region_points)
            ypoints = np.linspace(y_min, y_max, 2 * optim_region_points)
            z = ndimage.map_coordinates(self.image, np.vstack((ypoints, xpoints))).astype(np.float32)

        # sensitive to bright-to-dark
        # diffz = np.diff(z) / (np.abs(np.linspace(-optim_region,+optim_region,len(z)-1))+1)**(1/2)

        # sensitive to all edges
        diffz = -np.abs(np.diff(z)) / (np.abs(np.linspace(-optim_region, +optim_region, len(z) - 1)) + 1) ** (1 / 2)

        #        f = plt.figure()
        #        plt.subplot(121)
        #        plt.plot(z)
        #        plt.subplot(122)
        #        plt.plot(diffz)

        # find sharpest bright-to-dark transition. Maybe check if there are similar transitions in the line and only take the closest one
        minDeriv = np.argmin(diffz)
        # print minDeriv
        return (xpoints[minDeriv], ypoints[minDeriv])

    # optimizes a knot along a radius from the center of the ROI
    def optimizeKnot(self, center, knot):

        optim_region = 5  # voxels

        distanceX = knot[0] - center[0]
        distanceY = knot[1] - center[1]
        npoints = int(np.max([abs(2 * distanceX), abs(2 * distanceY)]))
        xpoints = center[0] + np.linspace(0, 2 * distanceX, npoints)
        ypoints = center[1] + np.linspace(0, 2 * distanceY, npoints)

        # restrict to region aroung the knot
        minIndex = np.max([0, int(npoints / 2 - optim_region)])
        maxIndex = np.min([int(npoints / 2 + optim_region), npoints])

        xpoints = xpoints[minIndex:maxIndex]
        ypoints = ypoints[minIndex:maxIndex]

        # print xpoints
        # print ypoints
        z = ndimage.map_coordinates(self.image, np.vstack((ypoints, xpoints))).astype(np.float32)
        diffz = np.diff(z) / (np.abs(np.array(range(len(z) - 1)) - (len(z) - 1) / 2) ** 2 + 1)

        #        f = plt.figure()
        #        plt.subplot(121)
        #        plt.plot(z)
        #        plt.subplot(122)
        #        plt.plot(diffz)

        # find sharpest bright-to-dark transition. Maybe check if there are similar transitions in the line and only take the closest one
        minDeriv = np.argmin(diffz) + 1
        return (xpoints[minDeriv], ypoints[minDeriv])

    # No @snapshotSaver: snapshot is saved in the calling function
    def addPoint(self, spline, event):
        self.currentPoint = spline.addKnot((event.xdata, event.ydata))
        self.reblit()

    # No @snapshotSaver: snapshot is saved in the calling function
    def movePoint(self, spline, event):
        if self.currentPoint is None:
            return
        spline.replaceKnot(self.currentPoint, (event.xdata, event.ydata))
        self.reblit()

    @pyqtSlot()
    @snapshotSaver
    def clearCurrentROI(self):
        if self.editMode == ToolboxWindow.EDITMODE_CONTOUR:
            roi = self.getCurrentROI()
            roi.removeAllKnots()
        elif self.editMode == ToolboxWindow.EDITMODE_MASK:
            self.roiManager.clear_mask(self.getCurrentROIName(), self.curImage)
            self.activeMask = None
        self.reblit()

    @snapshotSaver
    def _currentMaskOperation(self, operation_function):
        """
        Applies a generic operation to the current mask. operation_function is a function that accepts the mask as parameter
        and returns the new mask
        """
        if not self.editMode == ToolboxWindow.EDITMODE_MASK: return
        currentMask = self.getCurrentMask()
        newMask = operation_function(currentMask)
        self.setCurrentMask(newMask)
        if self.activeMask is None:
            self.updateMasksFromROIs()
        else: # only update the active mask
            self.activeMask = newMask.copy()
        self.reblit()

    @pyqtSlot()
    def maskGrow(self):
        self._currentMaskOperation(binary_dilation)

    @pyqtSlot()
    def maskShrink(self):
        self._currentMaskOperation(binary_erosion)

    @pyqtSlot(int)
    def maskDespeckle(self, radius):
        #self._currentMaskOperation(lambda mask: area_opening(mask, radius**2))
        self._currentMaskOperation(functools.partial(area_opening, area_threshold=radius ** 2))

    @pyqtSlot(int)
    def maskFillHoles(self, radius):
        #self._currentMaskOperation(lambda mask: area_closing(mask, radius ** 2))
        self._currentMaskOperation(functools.partial(area_closing, area_threshold=radius ** 2))

    @pyqtSlot()
    @snapshotSaver
    @separate_thread_decorator
    def samAutoRefine(self):
        if not self.editMode == ToolboxWindow.EDITMODE_MASK or \
                not self.roiManager:
            return

        def progress_callback(current, maximum):
            self.setSplash(True, current, maximum, "SAM autorefine")


        try:
            new_mask = enhance_mask(self.image, self.getCurrentMask(), progress_callback)
        except Exception as e:
            print("Error in SAM autorefine:", e)
            self.alert("Error in SAM autorefine: " + str(e))
            self.setSplash(False)
            return

        self.setCurrentMask(new_mask)
        self.updateMasksFromROIs()
        self.reblit()
        self.setSplash(False)

    @pyqtSlot(bool)
    @snapshotSaver
    @separate_thread_decorator
    def maskAutoThreshold(self, apply_to_all=False):
        if not self.editMode == ToolboxWindow.EDITMODE_MASK or \
                not self.roiManager:
            return
        self.setSplash(True, 0, 2, "Calculating threshold mask...")
        # Calculate the mask after bias correction
        bias_corrected_image = biascorrection_image(self.image)
        threshold_mask = sitk.GetArrayFromImage(
                            sitk.OtsuThreshold(
                            sitk.GetImageFromArray(bias_corrected_image), 0, 1, 200))

        self.setSplash(True, 1, 2, "Applying threshold...")
        if apply_to_all:
            for mask_key_tuple, mask in self.roiManager.all_masks(image_number=self.curImage):
                roi_name = mask_key_tuple[0]
                print("Processing", roi_name)
                new_mask = np.logical_and(mask, threshold_mask)
                self.roiManager.set_mask(roi_name, self.curImage, new_mask)
        else:
            mask = self.getCurrentMask()
            if mask is None:
                self.setSplash(False)
                return
            new_mask = np.logical_and(mask, threshold_mask)
            self.setCurrentMask(new_mask)

        self.setSplash(True, 2, 2, "Done!")
        self.updateMasksFromROIs()
        self.reblit()
        self.setSplash(False)




    #####################################################################################################
    ###
    ### Elastix
    ###
    #####################################################################################################

    @separate_thread_decorator
    def calcTransforms(self):
        if not self.registrationManager: return
        def local_setSplash(image_number):
            self.setSplash(True, image_number, len(self.imList), 'Registering images...')

        local_setSplash(0)
        self.registrationManager.calc_transforms(local_setSplash)
        self.setSplash(False, 0, len(self.imList), 'Registering images...')


    def propagateAll(self):
        while self.curImage < len(self.imList) - 1:
            self.propagate()
            plt.pause(.000001)

    def propagateBackAll(self):
        while self.curImage > 0:
            self.propagateBack()
            plt.pause(.000001)

    @snapshotSaver
    #@separate_thread_decorator
    def propagate(self):
        if self.curImage >= len(self.imList) - 1: return
        if not self.registrationManager: return
        # fixedImage = self.image
        # movingImage = self.imList[int(self.curImage+1)]

        self.setSplash(True, 0, 3)


        if self.editMode == ToolboxWindow.EDITMODE_CONTOUR:
            curROI = self.getCurrentROI()
            if curROI is None:
                self.setSplash(False, 0, 0)
                return
            nextROI = self.getCurrentROI(+1)
            knotsOut = self.registrationManager.run_transformix_knots(curROI.knots,
                                                                      self.registrationManager.get_transform(int(self.curImage)))

            if len(nextROI.knots) < 3:
                nextROI.removeAllKnots()
                nextROI.addKnots(knotsOut)
            else:
                for k in knotsOut:
                    i = nextROI.findNearestKnot(k)
                    oldK = nextROI.getKnot(i)
                    newK = ((oldK[0] + k[0]) / 2, (oldK[1] + k[1]) / 2)
                    # print "oldK", oldK, "new", k, "mid", newK
                    nextROI.replaceKnot(i, newK)
        elif self.editMode == ToolboxWindow.EDITMODE_MASK:
            mask_in = self.getCurrentMask()
            if mask_in is None:
                self.setSplash(False, 0, 0)
                return
            # Note: we are using the inverse transform, because the transforms are originally calculated to
            # transform points, which is the inverse as transforming images
            mask_out = self.registrationManager.run_transformix_mask(mask_in,
                                                                     self.registrationManager.get_inverse_transform(int(self.curImage+1)))
            self.setCurrentMask(mask_out, +1)


        self.curImage += 1
        self.displayImage(int(self.curImage), self.cmap, redraw=False)
        self.setSplash(True, 1, 3)

        if self.editMode == ToolboxWindow.EDITMODE_CONTOUR:
            self.simplify()
            self.setSplash(True, 2, 3)
            self.optimize()

        self.redraw()

        self.setSplash(False, 3, 3)

    @snapshotSaver
    #@separate_thread_decorator
    def propagateBack(self):
        if self.curImage < 1: return
        # fixedImage = self.image
        # movingImage = self.imList[int(self.curImage+1)]

        self.setSplash(True, 0, 3)

        if self.editMode == ToolboxWindow.EDITMODE_CONTOUR:
            curROI = self.getCurrentROI()
            if curROI is None:
                self.setSplash(False, 0, 0)
                return
            nextROI = self.getCurrentROI(-1)
            knotsOut = self.registrationManager.run_transformix_knots(curROI.knots,
                                                                      self.registrationManager.get_inverse_transform(int(self.curImage)))

            if len(nextROI.knots) < 3:
                nextROI.removeAllKnots()
                nextROI.addKnots(knotsOut)
            else:
                for k in knotsOut:
                    i = nextROI.findNearestKnot(k)
                    oldK = nextROI.getKnot(i)
                    newK = ((oldK[0] + k[0]) / 2, (oldK[1] + k[1]) / 2)
                    nextROI.replaceKnot(i, newK)
        elif self.editMode == ToolboxWindow.EDITMODE_MASK:
            mask_in = self.getCurrentMask()
            if mask_in is None:
                self.setSplash(False, 0, 0)
                return
            # Note: we are using the inverse transform, because the transforms are originally calculated to
            # transform points, which is the inverse as transforming images
            mask_out = self.registrationManager.run_transformix_mask(mask_in,
                                                                     self.registrationManager.get_transform(int(self.curImage-1)))
            self.setCurrentMask(mask_out, -1)

        self.setSplash(True, 1, 3)

        self.curImage -= 1
        self.displayImage(int(self.curImage), self.cmap, redraw=False)

        self.setSplash(True, 2, 3)

        if self.editMode == ToolboxWindow.EDITMODE_CONTOUR:
            self.simplify()
            self.setSplash(True, 3, 3)
            self.optimize()

        self.redraw()

        self.setSplash(False, 3, 3)

    def _get_masks_above_below(self):
        self.curImage = int(self.curImage)
        masks_above = []
        masks_above_index = []
        for i in range(self.curImage - 1, -1, -1):
            m = self.getCurrentMask(i - self.curImage)
            if np.any(m):
                masks_above.append(m)
                masks_above_index.append(i)

        masks_below = []
        masks_below_index = []
        for i in range(self.curImage + 1, len(self.imList)):
            m = self.getCurrentMask(i - self.curImage)
            if np.any(m):
                masks_below.append(m)
                masks_below_index.append(i)

        return masks_above, masks_above_index, masks_below, masks_below_index

    def _calculateInterpolatedMask(self):
        # find ROIs above and below the current image

        masks_above, masks_above_index, masks_below, masks_below_index = self._get_masks_above_below()

        if not masks_above and not masks_below:
            print('No masks to interpolate')
            return np.zeros(self.image.shape, dtype=np.uint8)
        if not masks_above or not masks_below:
            # all the masks are either above or below the current image: don't interpolate as the results are bad
            #print('Nearest neighbor')
            return (masks_above + masks_below)[0]
        else: # len(masks_above) < 2 or len(masks_below) < 2: Let's disable cubic interpolation
            #print('Linear interpolation')
            # We have fewer than 2 masks above and below. Can't use cubic interpolation. Just do linear
            # interpolation between the closest masks

            spline_list_1 = mask_to_trivial_splines(masks_above[0], spacing=4)
            spline_list_2 = mask_to_trivial_splines(masks_below[0], spacing=4)
            #print('Number of splines', len(spline_list_1))
            index1 = masks_above_index[0]
            index2 = masks_below_index[0]
            if len(spline_list_1) != len(spline_list_2):
                self.alert('Different number of subrois in neighboring regions')
                return np.zeros(self.image.shape, dtype=np.uint8)

            splines_list = masks_splines_to_splines_masks([spline_list_1, spline_list_2])
            out_mask = np.zeros(self.image.shape, dtype=np.uint8)
            for subroi_spline in splines_list:
                out_spline = SplineInterpROIClass()
                spline1 = subroi_spline[0]
                spline2 = subroi_spline[1]

                current_index = self.curImage
                for knot1, knot2 in zip(spline1.knots, spline2.knots):
                    f_x = interp1d([index1, index2], [knot1[0], knot2[0]], kind='linear')
                    f_y = interp1d([index1, index2], [knot1[1], knot2[1]], kind='linear')
                    out_spline.addKnot((f_x(current_index), f_y(current_index)))
                out_mask += out_spline.toMask(self.image.shape)
                out_mask = (out_mask > 0).astype(np.uint8)
                out_mask = binary_dilation(out_mask)
            return out_mask
        if 0: # cubic interpolation disabled
            # we have at least 2 slices above and 2 slices below: cubic interpolation
            #print('Cubic interpolation')
            spline_list_1 = mask_to_trivial_splines(masks_above[1], spacing=4)
            spline_list_2 = mask_to_trivial_splines(masks_above[0], spacing=4)
            spline_list_3 = mask_to_trivial_splines(masks_below[0], spacing=4)
            spline_list_4 = mask_to_trivial_splines(masks_below[1], spacing=4)
            # print('Number of splines', len(spline_list_1))
            index1 = masks_above_index[1]
            index2 = masks_above_index[0]
            index3 = masks_below_index[0]
            index4 = masks_below_index[1]
            if any([len(spline_list_1) != len(spline_list_2), len(spline_list_1) != len(spline_list_3), len(spline_list_1) != len(spline_list_4)]):
                self.alert('Different number of subrois in neighboring regions')
                return np.zeros(self.image.shape, dtype=np.uint8)

            splines_list = masks_splines_to_splines_masks([spline_list_1, spline_list_2, spline_list_3, spline_list_4])
            out_mask = np.zeros(self.image.shape, dtype=np.uint8)
            for subroi_spline in splines_list:
                out_spline = SplineInterpROIClass()
                spline1 = subroi_spline[0]
                spline2 = subroi_spline[1]
                spline3 = subroi_spline[2]
                spline4 = subroi_spline[3]

                current_index = self.curImage
                for knot1, knot2, knot3, knot4 in zip(spline1.knots, spline2.knots, spline3.knots, spline4.knots):
                    f_x = interp1d([index1, index2, index3, index4], [knot1[0], knot2[0], knot3[0], knot4[0]], kind='cubic')
                    f_y = interp1d([index1, index2, index3, index4], [knot1[1], knot2[1], knot3[1], knot4[1]], kind='cubic')
                    out_spline.addKnot((f_x(current_index), f_y(current_index)))

                out_mask += out_spline.toMask(self.image.shape)
                out_mask = (out_mask > 0).astype(np.uint8)
                out_mask = binary_dilation(out_mask)

            return out_mask


    def _registerMask(self):
        if self.registrationManager is None:
            return np.zeros(self.image.shape, dtype=np.uint8)

        self.setSplash(True, 0, 1, 'Calculating registration')

        masks_above, masks_above_index, masks_below, masks_below_index = self._get_masks_above_below()

        if not masks_above and not masks_below:
            return np.zeros(self.image.shape, dtype=np.uint8)

        mask_above = masks_above[0]
        mask_below = masks_below[0]

        mask_above_index = masks_above_index[0]
        mask_below_index = masks_below_index[0]

        registered_mask_above = None
        if mask_above is not None:
            registered_mask_above = mask_above
            for i in range(mask_above_index, self.curImage):
                # Note: we are using the inverse transform, because the transforms are originally calculated to
                # transform points, which is the inverse as transforming images
                registered_mask_above = self.registrationManager.run_transformix_mask(registered_mask_above,
                                                                    self.registrationManager.get_inverse_transform(i+1))

        registered_mask_below = None
        if mask_below is not None:
            registered_mask_below = mask_below
            for i in range(mask_below_index, self.curImage, -1):
                # Note: we are using the inverse transform, because the transforms are originally calculated to
                # transform points, which is the inverse as transforming images
                registered_mask_below = self.registrationManager.run_transformix_mask(registered_mask_below,
                                                                         self.registrationManager.get_transform(
                                                                             i - 1))

        self.setSplash(False)
        if registered_mask_above is None:
            return registered_mask_below
        elif registered_mask_below is None:
            return registered_mask_above
        else:
            return binary_dilation(mask_average([registered_mask_above, registered_mask_below],
                                [self.curImage-mask_below_index, mask_above_index-self.curImage]))

    @pyqtSlot(str)
    @separate_thread_decorator
    def interpolate(self, interpolation_method):
        self.do_interpolate(interpolation_method)

    def do_interpolate(self, interpolation_method):
        #if self.editMode == ToolboxWindow.EDITMODE_CONTOUR: return
        if interpolation_method == ToolboxWindow.INTERPOLATE_MASK_INTERPOLATE:
            interpolated_mask = self._calculateInterpolatedMask()
            self.setCurrentMask(interpolated_mask)
            self.redraw()
        if interpolation_method == ToolboxWindow.INTERPOLATE_MASK_REGISTER:
            registered_mask = self._registerMask()
            self.setCurrentMask(registered_mask)
            self.redraw()
        if interpolation_method == ToolboxWindow.INTERPOLATE_MASK_BOTH:
            interpolated_mask = self._calculateInterpolatedMask()
            registered_mask = self._registerMask()
            self.setCurrentMask(binary_dilation(mask_average([interpolated_mask, registered_mask])))
            self.redraw()

    @pyqtSlot(str)
    @separate_thread_decorator
    def interpolate_block(self, interpolation_method):
        #if self.editMode == ToolboxWindow.EDITMODE_CONTOUR: return

        # there needs to be at least one segmented slice above and one segmented slice below
        masks_above, masks_above_index, masks_below, masks_below_index = self._get_masks_above_below()
        if not masks_above or not masks_below:
            self.alert('Block interpolation only works if there is at least one segmented slice above and one segmented slice below')
            return
        initial_index = masks_above_index[0] + 1
        final_index = masks_below_index[0] - 1
        for i in range(initial_index, final_index+1):
            self.curImage = i
            self.displayImage(self.curImage)
            self.redraw()
            self.do_interpolate(interpolation_method)


    ##############################################################################################################
    ###
    ### Displaying
    ###
    ###############################################################################################################

    def gotoImageDialog(self):
        accepted, output = GenericInputDialog.show_dialog("Go to image", [
            GenericInputDialog.IntSpinInput("Image number", self.curImage, 0, len(self.imList) - 1),
        ], self.fig.canvas)
        if accepted:
            self.displayImage(output[0], redraw=True)

    def removeMasks(self):
        """ Remove the masks from the plot """
        try:
            self.maskImPlot.remove()
        except:
            pass
        self.maskImPlot = None

        try:
            self.maskOtherImPlot.remove()
        except:
            pass
        self.maskOtherImPlot = None

        try:
            self.brush_patch.remove()
        except:
            pass
        self.brush_patch = None

        self.activeMask = None
        self.otherMask = None

    def removeContours(self):
        """ Remove all the contours from the plot """
        self.activeRoiPainter.clear_patches(self.axes)
        self.sameRoiPainter.clear_patches(self.axes)
        self.otherRoiPainter.clear_patches(self.axes)

    def removeSubregion(self):
        """ Remove the autosegment subregion from the plot """
        if not self.region_rectangle:
            return

        try:
            self.region_rectangle.set_visible(False)
        except:
            pass

        try:
            self.region_rectangle.remove()
        except:
            pass

        self.region_rectangle = None


    def updateMasksFromROIs(self):
        roi_name = self.getCurrentROIName()
        mask_size = self.image.shape
        self.otherMask = np.zeros(mask_size, dtype=np.uint8)
        self.activeMask = np.zeros(mask_size, dtype=np.uint8)
        for key_tuple, mask in self.roiManager.all_masks(image_number=self.curImage):
            mask_name = key_tuple[0]
            if mask_name == roi_name:
                if mask is not None:
                    self.activeMask = mask.copy()
            else:
                if mask is not None:
                    self.otherMask = np.logical_or(self.otherMask, mask)
        self.emit_mask_slice_changed()

    def emit_mask_changed(self):
        if not self.toolbox_window.is_3D_viewer_visible(): return
        if self.roiManager is None:
            return
        roi_name = self.getCurrentROIName()
        if not roi_name:
            return
        full_mask = np.zeros((self.image.shape[0], self.image.shape[1], len(self.imList)), dtype=np.uint8)
        for key_tuple, mask in self.roiManager.all_masks(roi_name=roi_name):
            mask_slice = key_tuple[1]
            full_mask[:, :, mask_slice] = mask
        self.mask_changed.emit([self.resolution[0], self.resolution[1], self.resolution[2]], full_mask)

    def emit_mask_slice_changed(self):
        if not self.toolbox_window.is_3D_viewer_visible(): return
        if self.roiManager is None:
            return

        slice_n = int(self.curImage)
        mask = self.getCurrentMask()
        if mask is None:
            return

        self.mask_slice_changed.emit(slice_n, mask)

    def drawMasks(self):
        """ Plot the masks for the current figure """
        # print("Draw masks", time.time())
        # frame = inspect.getouterframes(inspect.currentframe(), 2)
        # for info in frame:
        #     print("Trace", info[3])
        if self.activeMask is None or self.otherMask is None:
            self.updateMasksFromROIs()

        if self.activeMask is None or self.otherMask is None:
            return

        if not self.hideRois:  # if we hide the ROIs, clear all the masks
            active_mask = self.activeMask
            other_mask = self.otherMask
        else:
            active_mask = np.zeros_like(self.activeMask, dtype=np.uint8)
            other_mask = np.zeros_like(self.otherMask, dtype=np.uint8)

        if self.maskImPlot is None:
            original_xlim = self.axes.get_xlim()
            original_ylim = self.axes.get_ylim()
            self.maskImPlot = self.axes.imshow(active_mask, cmap=self.mask_layer_colormap,
                                               alpha=GlobalConfig['MASK_LAYER_ALPHA'],
                                               vmin=0, vmax=1, zorder=100, aspect=self.resolution[0]/self.resolution[1])
            try:
                self.axes.set_xlim(original_xlim)
                self.axes.set_ylim(original_ylim)
            except:
                pass
            self.maskImPlot.set_animated(True)

        self.maskImPlot.set_data(active_mask.astype(np.uint8))
        self.maskImPlot.set_alpha(GlobalConfig['MASK_LAYER_ALPHA'])
        self.axes.draw_artist(self.maskImPlot)

        if self.maskOtherImPlot is None:
            original_xlim = self.axes.get_xlim()
            original_ylim = self.axes.get_ylim()
            relativeAlphaROI = GlobalConfig['ROI_OTHER_COLOR'][3] / GlobalConfig['ROI_COLOR'][3]
            self.maskOtherImPlot = self.axes.imshow(other_mask, cmap=self.mask_layer_other_colormap,
                                                    alpha=relativeAlphaROI*GlobalConfig['MASK_LAYER_ALPHA'],
                                                    vmin=0, vmax=1, zorder=101, aspect=self.resolution[0]/self.resolution[1])
            try:
                self.axes.set_xlim(original_xlim)
                self.axes.set_ylim(original_ylim)
            except:
                pass
            self.maskOtherImPlot.set_animated(True)

        self.maskOtherImPlot.set_data(other_mask.astype(np.uint8))
        self.maskOtherImPlot.set_alpha(GlobalConfig['MASK_LAYER_ALPHA'])
        self.axes.draw_artist(self.maskOtherImPlot)

    def updateContourPainters(self):
        # frame = inspect.getouterframes(inspect.currentframe(), 2)
        # for info in frame:
        #     print("Trace", info[3])


        self.activeRoiPainter.clear_rois(self.axes)
        self.otherRoiPainter.clear_rois(self.axes)
        self.sameRoiPainter.clear_rois(self.axes)
        if not self.roiManager or self.editMode != ToolboxWindow.EDITMODE_CONTOUR: return

        current_name = self.getCurrentROIName()
        current_subroi = self.getCurrentSubroiNumber()
        slice_number = int(self.curImage)

        for key_tuple, roi in self.roiManager.all_rois(image_number=slice_number):
            name = key_tuple[0]
            subroi = key_tuple[2]
            if name == current_name:
                if subroi == current_subroi:
                    self.activeRoiPainter.add_roi(roi)
                else:
                    self.sameRoiPainter.add_roi(roi)
            else:
                self.otherRoiPainter.add_roi(roi)

    def drawContours(self):
        """ Plot the contours for the current figure """
        # frame = inspect.getouterframes(inspect.currentframe(), 2)
        # for info in frame:
        #     print("Trace", info[3])
        #     print("Trace", info[3])add
        self.activeRoiPainter.recalculate_patches() # recalculate the position of the active ROI
        self.activeRoiPainter.draw(self.axes, False)
        self.otherRoiPainter.draw(self.axes, False)
        self.sameRoiPainter.draw(self.axes, False)

    def drawSubregion(self):
        """ Plot the autosegment subregion for the current figure """
        if not self.toolbox_window.get_subregion_restriction():
            self.removeSubregion()
            return

        subregion = self.getCurrentSubregion()

        if not self.region_rectangle:
            self.region_rectangle = Rectangle((subregion[1], subregion[0]), subregion[3], subregion[2],
                                              fill=False,
                                              edgecolor='green',
                                              linewidth=2)
            self.axes.add_patch(self.region_rectangle)
        else:
            self.region_rectangle.set_xy((subregion[1], subregion[0]))
            self.region_rectangle.set_width(subregion[3])
            self.region_rectangle.set_height(subregion[2])
            self.region_rectangle.set_visible(True)
        self.axes.draw_artist(self.region_rectangle)


    # convert a single slice to ROIs
    def maskToRois2D(self, name, mask, imIndex, refresh = True):
        if not self.roiManager: return
        self.roiManager.set_mask(name, imIndex, mask)
        if refresh:
            self.updateRoiList()
            self.redraw()

    # convert a 2D mask or a 3D dataset to rois
    def masksToRois(self, maskDict, imIndex):
        for name, mask in maskDict.items():
            if len(mask.shape) > 2: # multislice
                for sl in range(mask.shape[2]):
                    self.maskToRois2D(name, mask[:,:,sl], sl, False)
            else:
                self.maskToRois2D(name, mask, imIndex, False)
        self.updateRoiList()
        self.redraw()

    def displayImage(self, im, cmap=None, redraw = True):
        self.resetBlitBg()
        self.removeMasks()
        self.removeContours()
        self.removeSubregion()
        ImageShow.displayImage(self, im, cmap, redraw)
        self.updateRoiList()  # set the appropriate (sub)roi list for the current image
        self.activeMask = None
        self.otherMask = None
        self.updateContourPainters()
        self.drawSubregion()
        try:
            self.toolbox_window.set_class(self.classifications[int(self.curImage)])  # update the classification combo
        except:
            pass

    ##############################################################################################################
    ###
    ### UI Callbacks
    ###
    ##############################################################################################################

    def reblit(self):
        self.reblit_signal.emit()

    @pyqtSlot()
    def do_reblit(self):
        if self.suppressRedraw: return
        if self.blitBg is None or \
                self.blitXlim != self.axes.get_xlim() or \
                self.blitYlim != self.axes.get_ylim():
            self.removeMasks()
            self.removeContours()
            self.removeSubregion()
            self.redraw()
            return
        self.fig.canvas.restore_region(self.blitBg)
        self.plotAnimators()
        self.fig.canvas.blit(self.fig.bbox)
        self.suppressRedraw = True # avoid nested calls
        self.fig.canvas.flush_events()
        self.suppressRedraw = False

    def plotAnimators(self):
        if self.brush_patch is not None:
            self.axes.draw_artist(self.brush_patch)
        if self.roiManager:
            if self.editMode == ToolboxWindow.EDITMODE_CONTOUR:
                self.drawContours()
            elif self.editMode == ToolboxWindow.EDITMODE_MASK:
                self.drawMasks()
            self.drawSubregion()

    def redraw(self):
        self.redraw_signal.emit()

    @pyqtSlot()
    def do_redraw(self):
        #print("Redrawing...")
        if self.suppressRedraw: return
        try:
            self.removeMasks()
        except:
            pass
        try:
            self.removeContours()
        except:
            pass
        try:
            self.brush_patch.remove()
        except:
            pass
        try:
            self.removeSubregion()
        except:
            pass
        self.fig.canvas.draw()
        self.suppressRedraw = True # avoid nested calls
        self.fig.canvas.flush_events()
        #plt.pause(0.00001)
        self.suppressRedraw = False
        self.blitBg = self.fig.canvas.copy_from_bbox(self.fig.bbox)
        self.blitXlim = self.axes.get_xlim()
        self.blitYlim = self.axes.get_ylim()
        self.refreshCB()
        try:
            self.updateContourPainters()
        except:
            pass
        try:
            self.updateMasksFromROIs()
        except:
            pass
        self.reblit()

    @pyqtSlot()
    def refreshCB(self):
        # check if ROIs should be autosaved
        now = datetime.now()
        if (now - self.lastsave).total_seconds() > GlobalConfig['AUTOSAVE_INTERVAL'] and \
                not self.separate_thread_running: # avoid autosave while another thread is running
            self.lastsave = now
            self.saveROIPickle()

        if self.wacom:
            self.get_app().setOverrideCursor(Qt.BlankCursor)
        else:
            self.get_app().setOverrideCursor(Qt.ArrowCursor)

    @pyqtSlot()
    def close_slot(self):
        plt.close(self.fig)
        #self.closeCB(None)

    def closeCB(self, event):
        self.toolbox_window.close()
        self.toolbox_window.viewer3D.real_close()
        if not self.basepath: return
        if self.registrationManager:
            self.registrationManager.pickle_transforms()
        self.saveROIPickle()
        sys.exit(0)

    @pyqtSlot()
    def updateBrush(self):
        self.moveBrushPatch(None, True)
        self.reblit()

    def moveBrushPatch(self, event = None, force_update = False):
        """
            moves the brush. Returns True if the brush was moved to a new position
        """
        def remove_brush():
            try:
                self.brush_patch.remove()
                #self.fig.canvas.draw()
            except:
                pass
            self.brush_patch = None

        if not self.getCurrentROIName() or self.editMode != ToolboxWindow.EDITMODE_MASK:
            remove_brush()
            return

        brush_type, brush_size = self.toolbox_window.get_brush()

        try:
            mouseX = event.xdata
            mouseY = event.ydata
        except AttributeError: # event is None
            mouseX = None
            mouseY = None

        if self.toolbox_window.get_edit_button_state() == ToolboxWindow.ADD_STATE:
            brush_color = GlobalConfig['BRUSH_PAINT_COLOR']
        elif self.toolbox_window.get_edit_button_state() == ToolboxWindow.REMOVE_STATE:
            brush_color = GlobalConfig['BRUSH_ERASE_COLOR']
        else:
            brush_color = None
        if (event is not None and (mouseX is None or mouseY is None)) or brush_color is None:
            remove_brush()
            return False

        if event is not None:
            try:
                oldX = self.moveBrushPatch_oldX  # static variables
                oldY = self.moveBrushPatch_oldY
            except:
                oldX = -1
                oldY = -1

            mouseX = np.round(mouseX)
            mouseY = np.round(mouseY)
            self.moveBrushPatch_oldX = mouseX
            self.moveBrushPatch_oldY = mouseY

            if oldX == mouseX and oldY == mouseY and not force_update:
                return False # only return here if we are not forcing an update

        if brush_type == ToolboxWindow.BRUSH_SQUARE:
            if event is not None:
                xy = (math.floor(mouseX - brush_size / 2) + 0.5, math.floor(mouseY - brush_size / 2) + 0.5)
            else:
                try:
                    xy = self.brush_patch.get_xy()
                except:
                    xy = (0.0,0.0)
            if type(self.brush_patch) != SquareBrush:
                try:
                    self.brush_patch.remove()
                except:
                    pass
                self.brush_patch = SquareBrush(xy, brush_size, brush_size, color=brush_color)
                self.axes.add_patch(self.brush_patch)

            self.brush_patch.set_xy(xy)
            self.brush_patch.set_height(brush_size)
            self.brush_patch.set_width(brush_size)

        elif brush_type == ToolboxWindow.BRUSH_CIRCLE:
            if event is not None:
                center = (math.floor(mouseX), math.floor(mouseY))
            else:
                try:
                    center = self.brush_patch.get_center()
                except:
                    center = (0.0,0.0)

            if type(self.brush_patch) != PixelatedCircleBrush:
                try:
                    self.brush_patch.remove()
                except:
                    pass
                self.brush_patch = PixelatedCircleBrush(center, brush_size, color=brush_color)
                self.axes.add_patch(self.brush_patch)

            self.brush_patch.set_center(center)
            self.brush_patch.set_radius(brush_size)

        self.brush_patch.set_animated(True)
        self.brush_patch.set_color(brush_color)
        #self.do_reblit()
        return True

    def modifyMaskFromBrush(self):
        if not self.brush_patch: return
        if self.toolbox_window.get_edit_button_state() == ToolboxWindow.ADD_STATE:
            paintMask = self.brush_patch.to_mask(self.activeMask.shape)
            if self.toolbox_window.get_intensity_aware():
                np.logical_and(paintMask, self.threshold_mask, out=paintMask)
            np.logical_or(self.activeMask, paintMask, out=self.activeMask)
        elif self.toolbox_window.get_edit_button_state() == ToolboxWindow.REMOVE_STATE:
            brush_mask = self.brush_patch.to_mask(self.activeMask.shape)
            if self.toolbox_window.get_intensity_aware():
                np.logical_and(brush_mask, self.threshold_mask, out=brush_mask)
            eraseMask = np.logical_not(brush_mask)
            np.logical_and(self.activeMask, eraseMask, out=self.activeMask)
            if self.toolbox_window.get_erase_from_all_rois():
                np.logical_and(self.otherMask, eraseMask, out=self.otherMask)
        #self.do_reblit()

    # override from ImageShow
    def mouseMoveCB(self, event):
        self.fig.canvas.activateWindow()
        if (self.getState() == 'MUSCLE' and
                self.toolbox_window.get_edit_button_state() in (ToolboxWindow.ADD_STATE, ToolboxWindow.REMOVE_STATE) and
                self.toolbox_window.get_edit_mode() == ToolboxWindow.EDITMODE_MASK and
                self.isCursorNormal() and
                event.button != 2 and
                event.button != 3):
            xy = (event.x, event.y)
            if xy == self.oldMouseXY: return  # reject mouse move events when the mouse doesn't move. From parent
            self.oldMouseXY = xy
            moved_to_new_point = self.moveBrushPatch(event)
            if event.button == 1: # because we are overriding MoveCB, we won't call leftPressCB
                if moved_to_new_point:
                    #print("Moved to new point")
                    self.modifyMaskFromBrush()
            self.reblit()
        else:
            if self.brush_patch:
                try:
                    self.brush_patch.remove()
                except:
                    pass
                self.brush_patch = None
            ImageShow.mouseMoveCB(self, event)

    def leftMoveCB(self, event):
        if event.xdata is None or event.ydata is None:
            return

        if self.toolbox_window.get_subregion_restriction():
            if self.toolbox_window.get_edit_button_state() == ToolboxWindow.SUBREGION_SET_STATE:
                if not self.subregion_start: return
                start_row = self.subregion_start[0]
                start_col = self.subregion_start[1]

                new_row = int(event.ydata)
                new_col = int(event.xdata)

                new_start_row = min(start_row, new_row)
                new_end_row = max(start_row, new_row)
                new_start_col = min(start_col, new_col)
                new_end_col = max(start_col, new_col)
            elif self.toolbox_window.get_edit_button_state() == ToolboxWindow.SUBREGION_MOVE_STATE:
                delta_row = int(event.ydata) - self.subregion_translate_start[0]
                delta_col = int(event.xdata) - self.subregion_translate_start[1]

                original_subregion = self.subregion_start
                new_start_row = original_subregion[0] + delta_row
                new_start_col = original_subregion[1] + delta_col
                new_end_row = new_start_row + original_subregion[2]
                new_end_col = new_start_col + original_subregion[3]

            if new_start_row < 0:
                new_start_row = 0

            if new_start_col < 0:
                new_start_col = 0

            if new_end_row >= self.image.shape[0]:
                new_end_row = self.image.shape[0]

            if new_end_col >= self.image.shape[1]:
                new_end_col = self.image.shape[1]

            self.setCurrentSubregion(
                (new_start_row, new_start_col, new_end_row - new_start_row, new_end_col - new_start_col))
            self.reblit()
            return


        if self.getState() != 'MUSCLE': return

        roi = self.getCurrentROI()
        if self.toolbox_window.get_edit_button_state() == ToolboxWindow.ADD_STATE:  # event.key == 'shift' or checkCapsLock():
            self.movePoint(roi, event)
        elif self.toolbox_window.get_edit_button_state() == ToolboxWindow.TRANSLATE_STATE:
            if self.translateDelta is None: return
            newCenter = (event.xdata - self.translateDelta[0], event.ydata - self.translateDelta[1])
            roi.moveCenterTo(newCenter)
            self.reblit()
        elif self.toolbox_window.get_edit_button_state() == ToolboxWindow.ROTATE_STATE:
            if self.rotationDelta is None: return
            newAngle = roi.getOrientation( (event.xdata, event.ydata), center = self.rotationDelta[0])
            roi.reorientByAngle(newAngle - self.rotationDelta[1])
            self.reblit()

    def leftPressCB(self, event):
        if not self.imPlot.contains(event):
            return

        # These two are independent on the existance of an active ROI
        if self.toolbox_window.get_subregion_restriction():
            if self.toolbox_window.get_edit_button_state() == ToolboxWindow.SUBREGION_SET_STATE:
                self.subregion_start = (int(event.ydata), int(event.xdata))
                self.removeSubregion()
                self.redraw()
                return

            if self.toolbox_window.get_edit_button_state() == ToolboxWindow.SUBREGION_MOVE_STATE:
                self.subregion_translate_start = (int(event.ydata), int(event.xdata))
                self.subregion_start = self.getCurrentSubregion()
                self.removeSubregion()
                self.redraw()
                return

        # Only set if there is an active ROI
        if self.getState() != 'MUSCLE': return

        if self.toolbox_window.get_edit_mode() == ToolboxWindow.EDITMODE_MASK:
            if self.toolbox_window.get_intensity_aware():
                # if the operation has to be intensity aware, create a threshold mask based on current point
                intensity = self.image[int(event.ydata), int(event.xdata)]
                threshold_intensity = intensity * self.toolbox_window.get_intensity_threshold()
                lower_threshold = intensity - threshold_intensity
                upper_threshold = intensity + threshold_intensity
                self.threshold_mask = self.image < upper_threshold
                np.logical_and(self.threshold_mask, self.image > lower_threshold, out=self.threshold_mask)
            self.modifyMaskFromBrush()
        else:
            #print("Edit button state", self.toolbox_window.get_edit_button_state())
            roi = self.getCurrentROI()
            knotIndex, knot = roi.findKnotEvent(event)
            if self.toolbox_window.get_edit_button_state() == ToolboxWindow.TRANSLATE_STATE:
                center = roi.getCenterOfMass()
                if center is None:
                    self.translateDelta = None
                    return
                self.saveSnapshot()
                self.translateDelta = (event.xdata - center[0], event.ydata - center[1])
            elif self.toolbox_window.get_edit_button_state() == ToolboxWindow.ROTATE_STATE:
                center = roi.getCenterOfMass()
                if center is None:
                    self.rotationDelta = None
                    return
                self.saveSnapshot()
                startAngle = roi.getOrientation(center=center)
                self.rotationDelta = (center, roi.getOrientation( (event.xdata, event.ydata), center=center ) - startAngle)
            elif self.toolbox_window.get_edit_button_state() == ToolboxWindow.REMOVE_STATE:
                if knotIndex is not None:
                    self.saveSnapshot()
                    roi.removeKnot(knotIndex)
                    self.reblit()
            elif self.toolbox_window.get_edit_button_state() == ToolboxWindow.ADD_STATE:
                self.saveSnapshot()
                if knotIndex is None:
                    self.addPoint(roi, event)
                else:
                    self.currentPoint = knotIndex

    def leftReleaseCB(self, event):
        self.currentPoint = None  # reset the state
        self.translateDelta = None
        self.rotationDelta = None
        self.subregion_start = None
        self.suregion_translate_start = None
        if self.editMode == ToolboxWindow.EDITMODE_MASK:
            self.saveSnapshot() # save state before modification
            if self.roiManager is not None:
                self.roiManager.set_mask(self.getCurrentROIName(), self.curImage, self.activeMask)
            if self.toolbox_window.get_erase_from_all_rois():
                for (key_tuple, mask) in self.roiManager.all_masks(image_number=self.curImage):
                    if key_tuple[0] == self.getCurrentROIName(): continue
                    self.roiManager.set_mask(key_tuple[0], key_tuple[1], np.logical_and(mask, self.otherMask))
        self.emit_mask_slice_changed()

    def rightPressCB(self, event):
        self.hideRois = GlobalConfig['HIDE_ROIS_RIGHTCLICK']
        self.redraw()

    def rightReleaseCB(self, event):
        self.hideRois = False
        self.redraw()

    def mouseScrollCB(self, event):
        modifier_status, *_ = self.get_key_modifiers(event)
        if modifier_status['ctrl']:
            if event.step < 0:
                self.reduce_brush_size.emit()
            elif event.step > 0:
                self.increase_brush_size.emit()
            return
        ImageShow.mouseScrollCB(self, event)

    @staticmethod
    def get_key_modifiers(event):
        modifiers = event.guiEvent.modifiers()
        try:
            pressed_key_without_modifiers = event.key.split('+')[-1]  # this gets the nonmodifier key if the pressed key is ctrl+z for example
        except:
            pressed_key_without_modifiers = ''
        is_key_modifier_only = (pressed_key_without_modifiers in ['shift', 'control', 'ctrl', 'cmd', 'super', 'alt'])
        out_modifiers = {'ctrl': (modifiers & (Qt.ControlModifier | Qt.MetaModifier)) != Qt.NoModifier,
                         'shift': (modifiers & Qt.ShiftModifier) == Qt.ShiftModifier,
                         'alt': (modifiers & Qt.AltModifier) == Qt.AltModifier,
                         'none': (modifiers == Qt.NoModifier)}
        return out_modifiers, is_key_modifier_only, pressed_key_without_modifiers


    def keyPressCB(self, event):
        modifier_status, is_key_modifier_only, pressed_key_without_modifiers = self.get_key_modifiers(event)

        if is_key_modifier_only:
            if modifier_status['shift']:
                self.toolbox_window.set_temp_edit_button_state(ToolboxWindow.ADD_STATE)
            elif modifier_status['ctrl']:
                self.toolbox_window.set_temp_edit_button_state(ToolboxWindow.REMOVE_STATE)
            return

        if modifier_status['ctrl']:
            if pressed_key_without_modifiers in self.shortcuts:
                self.shortcuts[pressed_key_without_modifiers]()
            return

        if event.key == 'n':
            if self.registration_available:
                self.propagate()
        elif event.key == 'b':
            if self.registration_available:
                self.propagateBack()
        elif event.key == '-' or event.key == 'y' or event.key == 'z':
            self.reduce_brush_size.emit()
        elif event.key == '+' or event.key == 'x':
            self.increase_brush_size.emit()
        elif event.key == 'r':
            self.roiRemoveOverlap()
        else:
            ImageShow.keyPressCB(self, event)

    def keyReleaseCB(self, event):
        modifier_status, is_key_modifier_only, pressed_key_without_modifiers = self.get_key_modifiers(event)

        if modifier_status['shift']:
            self.toolbox_window.set_temp_edit_button_state(ToolboxWindow.ADD_STATE)
        elif modifier_status['ctrl']:
            self.toolbox_window.set_temp_edit_button_state(ToolboxWindow.REMOVE_STATE)
        else:
            self.toolbox_window.restore_edit_button_state()


    ################################################################################################################
    ###
    ### I/O
    ###
    ################################################################################################################

    def getDatasetAsNumpy(self):
        return np.transpose(np.stack(self.imList), [1,2,0])

    @pyqtSlot(str)
    def saveROIPickle(self, roiPickleName=None, async_write = False):

        @separate_thread_decorator
        def write_file(name, bytes_to_write):
            with open(name, 'wb') as f:
                f.write(bytes_to_write)

        showWarning = True
        if not roiPickleName:
            roiPickleName = self.getRoiFileName()
            showWarning = False # don't show a empty roi warning if autosaving
            async_write = True

        #print("Saving ROIs", roiPickleName)
        if self.roiManager and not self.roiManager.is_empty():  # make sure ROIs are not empty
            dumpObj = {'classifications': self.classifications,
                       'roiManager': self.roiManager }
            if async_write:
                bytes_to_write = pickle.dumps(dumpObj)
                write_file(roiPickleName, bytes_to_write) # write file asynchronously for a smoother experience in autosave
            else:
                pickle.dump(dumpObj, open(roiPickleName, 'wb'))
        else:
            if showWarning: self.alert('ROIs are empty - not saved')

    @pyqtSlot(str)
    def loadROIPickle(self, roiPickleName=None):
        if not roiPickleName:
            roiPickleName = self.getRoiFileName()
        #print("Loading ROIs", roiPickleName)
        try:
            dumpObj = pickle.load(open(roiPickleName, 'rb'))
        except UnicodeDecodeError:
            print('Warning: Unicode decode error')
            dumpObj = pickle.load(open(roiPickleName, 'rb'), encoding='latin1')
        except:
            traceback.print_exc()
            self.alert("Unspecified error", "Error")
            return

        roiManager = None
        classifications = self.classifications

        if isinstance(dumpObj, (ROIManager, utils.ROIManager.ROIManager)):
            roiManager = dumpObj
        elif isinstance(dumpObj, dict):
            try:
                classifications = dumpObj['classifications']
                roiManager = dumpObj['roiManager']
            except KeyError:
                self.alert("Unrecognized saved ROI type")
                return

        try:
            assert isinstance(roiManager, (ROIManager, utils.ROIManager.ROIManager))
        except AssertionError:
            self.alert("Unrecognized saved ROI type")
            return

        if roiManager.mask_size[0] != self.image.shape[0] or \
            roiManager.mask_size[1] != self.image.shape[1]:
            self.alert("ROI for wrong dataset")
            return

        # compatibility with old versions that don't have autosegment subregions
        try:
            roiManager.autosegment_subregions
        except AttributeError:
            roiManager.autosegment_subregions = {}

        #print('Rois loaded')
        self.clearAllROIs()
        self.roiManager = roiManager
        available_classes = self.toolbox_window.get_available_classes()
        for i, classification in enumerate(classifications[:]):
            if classification not in available_classes:
                classifications[i] = 'None'

        self.classifications = classifications
        self.updateRoiList()
        self.updateMasksFromROIs()
        self.updateContourPainters()
        self.toolbox_window.set_class(self.classifications[int(self.curImage)])  # update the classification combo
        self.redraw()

    @pyqtSlot(str, str)
    @pyqtSlot(str)
    def loadDirectory(self, path, override_class=None):
        self.setSplash(True, 0, 1, "Loading dataset")

        def __reset_state():
            self.imList = []
            self.resetInternalState()
            self.override_class = override_class
            self.resolution_valid = False
            self.affine = None
            self.image = None
            self.resolution = [1, 1, 1]

        def __cleanup():
            __reset_state()
            self.setSplash(False)

        def __error(error = None):
            print(error, file=sys.stderr)
            self.alert("Error loading dataset. See the log for details", "Error")
            __cleanup()
            self.displayImage(None)
            self.redraw()

        __reset_state()
        _, ext = os.path.splitext(path)
        mask_dictionary = None
        if ext.lower() == '.npz':
            # data and mask bundle
            bundle = np.load(path, allow_pickle=False)
            if 'data' not in bundle and 'image' not in bundle:
                self.alert('No data in bundle!', 'Error')
                self.setSplash(False, 1, 2, "")
                return
            if 'comment' in bundle:
                self.alert('Loading bundle with comment:\n' + str(bundle['comment']), 'Info')

            self.basepath = os.path.dirname(path)
            try:
                if 'data' in bundle:
                    self.loadNumpyArray(bundle['data'])
                elif 'image' in bundle:
                    self.loadNumpyArray(bundle['image'])
                else:
                    __error('No data in bundle!') # should never happen because we are checking above
            except Exception as e:
                __error(e)
                return

            if 'resolution' in bundle:
                self.resolution = list(bundle['resolution'])
                if len(self.resolution) == 2:
                    self.resolution.append(1.0)
                self.resolution_valid = True
                print('Resolution', self.resolution)
                self.medical_volume._affine = np.diag(self.resolution + [1])

            mask_dictionary = {}
            for key in bundle:
                if key.startswith('mask_'):
                    mask_name = key[len('mask_'):]
                    mask_dictionary[mask_name] = bundle[key]
                    print('Found mask', mask_name)

            # from the parent class
            try:
                self.imPlot.remove()
            except:
                pass
            self.imPlot = None
            self.curImage = 0
            self.displayImage(int(0))
            self.axes.set_xlim(-0.5, self.image.shape[1] - 0.5)
            self.axes.set_ylim(self.image.shape[0] - 0.5, -0.5)
        else:
            try:
                ImageShow.loadDirectory(self, path)
            except Exception as e:
                __error(e)
                return

        # ask for resolution to be inserted
        if not self.resolution_valid:
            accepted, output = GenericInputDialog.show_dialog("Insert resolution", [
                GenericInputDialog.FloatSpinInput("X (mm)", 1, 0, 99, 0.1),
                GenericInputDialog.FloatSpinInput("Y (mm)", 1, 0, 99, 0.1),
                GenericInputDialog.FloatSpinInput("Slice (mm)", 1, 0, 99, 0.1)
            ], self.fig.canvas)
            if accepted:
                self.resolution = [output[0], output[1], output[2]]
                self.resolution_valid = True
                self.axes.set_aspect(aspect=self.resolution[0]/self.resolution[1])
                self.medical_volume._affine = np.diag(self.resolution + [1])

        # this is in case appendimage was never called
        if len(self.classifications) == 0:
            self.update_all_classifications()

        roi_bak_name = self.getRoiFileName() + '.' + datetime.now().strftime('%Y%m%d%H%M%S')
        try:
            shutil.copyfile(self.getRoiFileName(), roi_bak_name)
        except:
            print("Warning: cannot copy roi file")

        self.roiManager = ROIManager(self.imList[0].shape)
        self.registrationManager = RegistrationManager(self.imList,
                                                       None,
                                                       os.getcwd(),
                                                       GlobalConfig['TEMP_DIR'])
        self.registrationManager.set_standard_transforms_name(self.basepath, self.basename)
        #self.loadROIPickle()
        self.updateRoiList()
        try:
            self.toolbox_window.set_class(self.classifications[int(self.curImage)])  # update the classification combo
        except:
            pass
        self.redraw()
        self.toolbox_window.general_enable(True)
        self.toolbox_window.set_exports_enabled(numpy= True,
                                                dicom= (self.dicomHeaderList is not None),
                                                nifti= (self.affine is not None)
                                                )
        if mask_dictionary:
            self.setSplash(True, 1, 2, "Loading masks")
            self.masksToRois(mask_dictionary, 0)
        self.setSplash(False, 1, 2, "Loading masks")
        self.volume_loaded_signal.emit([self.resolution[0], self.resolution[1], self.resolution[2]], self.medical_volume.volume)

    def update_all_classifications(self):
        self.classifications = []
        for imIndex in range(len(self.imList)):
            if self.override_class:
                self.classifications.append(self.override_class)
                continue
            if not self.dl_classifier:
                self.classifications.append('None')
                continue
            class_input = {'image': self.imList[imIndex], 'resolution': self.resolution[0:2]}
            class_str = self.dl_classifier(class_input)
            # class_str = 'Thigh' # DEBUG
            print("Classification", class_str)
            self.classifications.append(class_str)


    def appendImage(self, im):
        ImageShow.appendImage(self, im)
        if self.override_class:
            self.classifications.append(self.override_class)
            return
        if not self.dl_classifier:
            self.classifications.append('None')
            return
        class_input = {'image': self.imList[-1], 'resolution': self.resolution[0:2]}
        class_str = self.dl_classifier(class_input)
        #class_str = 'Thigh' # DEBUG
        print("Classification", class_str)
        self.classifications.append(class_str)

    @pyqtSlot(str, str)
    @separate_thread_decorator
    def saveBundle(self, path_out: str, comment: str):
        self.setSplash(True, 0, 1, "Saving bundle...")
        bundle = self.prepare_numpy_bundle(comment)
        np.savez_compressed(path_out, **bundle)
        self.setSplash(False)

    @pyqtSlot(str, str)
    @separate_thread_decorator
    def saveResults(self, pathOut: str, outputType: str):
        # outputType is 'dicom', 'npy', 'npz', 'nifti', 'compact_dicom', 'compact_nifti'
        print("Saving results...")

        self.setSplash(True, 0, 4, "Calculating maps...")

        allMasks, dataForTraining, segForTraining, meanDiceScore = self.calcOutputData(setSplash=True)

        self.setSplash(True, 1, 4, "Incremental learning...")

        # perform incremental learning
        if GlobalConfig['DO_INCREMENTAL_LEARNING']:
            self.incrementalLearn(dataForTraining, segForTraining, meanDiceScore, True)

        self.setSplash(True, 3, 4, "Saving file...")

        if outputType == 'dicom':
            save_dicom_masks(pathOut, allMasks, self.affine, self.dicomHeaderList)
        elif outputType == 'nifti':
            save_nifti_masks(pathOut, allMasks, self.affine)
        elif outputType == 'npy':
            save_npy_masks(pathOut, allMasks)
        elif outputType == 'compact_dicom':
            save_single_dicom_dataset(pathOut, allMasks, self.affine, self.dicomHeaderList)
        elif outputType == 'compact_nifti':
            save_single_nifti(pathOut, allMasks, self.affine)
        else: # assume the most generic outputType == 'npz':
            save_npz_masks(pathOut, allMasks)

        self.setSplash(False, 4, 4, "End")

    @pyqtSlot(str)
    @separate_thread_decorator
    def saveStats_singleslice(self, file_out: str):
        """ Saves the statistics for a datasets. Exported statistics:
            - Number of slices where ROI is present
            - Number of voxels
            - Average value of the data over ROI
            - Standard Deviation of the data
            - 0-25-50-75-100 percentiles of the data distribution
        """
        self.setSplash(True, 0, 2, "Calculating maps...")

        allMasks, dataForTraining, segForTraining, meanDiceScore = self.calcOutputData(setSplash=True)

        self.setSplash(True, 1, 2, "Calculating stats...")

        dataset = self.getDatasetAsNumpy()

        csv_file = open(file_out, 'w')
        field_names = ['roi_name',
                       'slice',
                       'voxels',
                       'volume',
                       'mean',
                       'standard_deviation',
                       'perc_0',
                       'perc_25',
                       'perc_50',
                       'perc_75',
                       'perc_100']
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
        csv_writer.writeheader()

        for roi_name, roi_mask in allMasks.items():
            for slice_number in range(roi_mask.shape[2]):
                mask_slice = roi_mask[:, :, slice_number]
                data_slice = dataset[:, :, slice_number]
                if mask_slice.sum() == 0:
                    continue
                try:
                    csvRow = {}
                    csvRow['roi_name'] = roi_name
                    csvRow['slice'] = slice_number
                    mask = mask_slice > 0
                    masked = np.ma.array(data_slice, mask=np.logical_not(mask))
                    csvRow['voxels'] = mask.sum()
                    try:
                        csvRow['volume'] = csvRow['voxels']*self.resolution[0]*self.resolution[1]*self.resolution[2]
                    except:
                        csvRow['volume'] = 0
                    compressed_array = masked.compressed()
                    csvRow['mean'] = compressed_array.mean()
                    csvRow['standard_deviation'] = compressed_array.std()
                    csvRow['perc_0'] = compressed_array.min()
                    csvRow['perc_100'] = compressed_array.max()
                    csvRow['perc_25'] = np.percentile(compressed_array, 25)
                    csvRow['perc_50'] = np.percentile(compressed_array, 50)
                    csvRow['perc_75'] = np.percentile(compressed_array, 75)
                    csv_writer.writerow(csvRow)
                except:
                    print('Error calculating statistics for ROI', roi_name)
                    traceback.print_exc()

        csv_file.close()
        self.setSplash(False, 2, 2, "Finished")


    @pyqtSlot(str)
    @separate_thread_decorator
    def saveStats(self, file_out: str):
        """ Saves the statistics for a datasets. Exported statistics:
            - Number of slices where ROI is present
            - Number of voxels
            - Average value of the data over ROI
            - Standard Deviation of the data
            - 0-25-50-75-100 percentiles of the data distribution
        """
        self.setSplash(True, 0, 2, "Calculating maps...")

        allMasks, dataForTraining, segForTraining, meanDiceScore = self.calcOutputData(setSplash=True)

        self.setSplash(True, 1, 2, "Calculating stats...")

        dataset = self.getDatasetAsNumpy()

        csv_file = open(file_out, 'w')
        field_names = ['roi_name',
                       'slices',
                       'voxels',
                       'volume',
                       'mean',
                       'standard_deviation',
                       'perc_0',
                       'perc_25',
                       'perc_50',
                       'perc_75',
                       'perc_100']
        csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
        csv_writer.writeheader()

        for roi_name, roi_mask in allMasks.items():
            try:
                csvRow = {}
                csvRow['roi_name'] = roi_name
                mask = roi_mask > 0
                masked = np.ma.array(dataset, mask=np.logical_not(roi_mask))
                csvRow['voxels'] = mask.sum()
                try:
                    csvRow['volume'] = csvRow['voxels']*self.resolution[0]*self.resolution[1]*self.resolution[2]
                except:
                    csvRow['volume'] = 0
                # count the slices where the roi is present
                mask_pencil = np.sum(mask, axis=(0,1))
                csvRow['slices'] = np.sum(mask_pencil > 0)
                compressed_array = masked.compressed()
                csvRow['mean'] = compressed_array.mean()
                csvRow['standard_deviation'] = compressed_array.std()
                csvRow['perc_0'] = compressed_array.min()
                csvRow['perc_100'] = compressed_array.max()
                csvRow['perc_25'] = np.percentile(compressed_array, 25)
                csvRow['perc_50'] = np.percentile(compressed_array, 50)
                csvRow['perc_75'] = np.percentile(compressed_array, 75)
                csv_writer.writerow(csvRow)
            except:
                print('Error calculating statistics for ROI', roi_name)
                traceback.print_exc()

        csv_file.close()
        self.setSplash(False, 2, 2, "Finished")

    @pyqtSlot(str, bool, int, int)
    @separate_thread_decorator
    def saveRadiomics(self, file_out: str, do_quantization=True, quant_levels=32, erode_px=0):
        """ Saves the radiomics features from pyradiomics
        """
        self.setSplash(True, 0, 2, "Calculating maps...")

        allMasks, dataForTraining, segForTraining, meanDiceScore = self.calcOutputData(setSplash=True)

        self.setSplash(True, 1, 2, "Calculating stats...")

        dataset = self.getDatasetAsNumpy()

        if do_quantization:
            data_min = dataset.min()
            data_max = dataset.max()
            dataset = np.round((dataset-data_min) * quant_levels / (data_max - data_min))

        first_run = True
        header = 'roi_name'

        with open(file_out, 'w') as featureFile:
            for roi_name, roi_mask in allMasks.items():
                if erode_px > 0:
                    eroded_mask = binary_erosion(roi_mask, iterations=erode_px)
                else:
                    eroded_mask = roi_mask

                extractor = radiomics.featureextractor.RadiomicsFeatureExtractor()
                image = sitk.GetImageFromArray(dataset)
                features = extractor.execute(image, sitk.GetImageFromArray(eroded_mask.astype(np.uint8)))
                featureLine = f'{roi_name}'
                for k, v in features.items():
                    if k.startswith('original'):
                        if first_run:
                            header += ',' + k
                        try:
                            featureLine += ',{:.6f}'.format(v[0])
                        except:
                            featureLine += ',{:.6f}'.format(v)
                if first_run:
                    featureFile.write(header + '\n')
                    first_run = False
                featureFile.write(featureLine + '\n')

        self.setSplash(False, 2, 2, "Finished")

    def prepare_numpy_bundle(self, comment = ''):
        dataset = self.getDatasetAsNumpy()
        allMasks, dataForTraining, segForTraining, meanDiceScore = self.calcOutputData(setSplash=True)
        resolution = np.array(self.resolution)
        out_data = {'data': dataset, 'resolution': resolution, 'comment': comment}
        for mask_name, mask in allMasks.items():
            out_data[f'mask_{mask_name}'] = mask
        return out_data

    @pyqtSlot(str)
    def uploadData(self, comment = ''):
        print('Uploading data')
        out_data = self.prepare_numpy_bundle(comment)
        self.model_provider.upload_data(out_data)
        self.setSplash(False, 2, 2, "Finished")

    @pyqtSlot(str)
    @snapshotSaver
    @separate_thread_decorator
    def loadMask(self, filename: str):
        dicom_ext = ['.dcm', '.ima']
        nii_ext = ['.nii', '.gz']
        npy_ext = ['.npy']
        npz_ext = ['.npz']
        path = os.path.abspath(filename)
        _, ext = os.path.splitext(path)

        if os.path.isdir(path):
            containsDirs = False
            containsDicom = False
            nii_list = []
            dir_list = []
            firstDicom = None
            for element in os.listdir(path):
                if element.startswith('.'): continue
                new_path = os.path.join(path, element)
                if os.path.isdir(new_path):
                    containsDirs = True
                    dir_list.append(new_path)
                else: # check if the folder contains dicoms
                    _, ext2 = os.path.splitext(new_path)
                    if ext2.lower() in dicom_ext:
                        containsDicom = True
                        if firstDicom is None:
                            firstDicom = new_path
                    elif ext2.lower() in nii_ext:
                        nii_list.append(new_path)

            if containsDicom and containsDirs:
                msgBox = QMessageBox()
                msgBox.setText('Folder contains both dicom files and subfolders.\nWhat do you want to do?')
                buttonDicom = msgBox.addButton('Load files as one ROI', QMessageBox.YesRole)
                buttonDir = msgBox.addButton('Load subfolders as multiple ROIs', QMessageBox.NoRole)
                msgBox.exec()
                if msgBox.clickedButton() == buttonDicom:
                    containsDirs = False
                else:
                    containsDicom = False

            if containsDicom:
                path = new_path # "fake" the loading of the first image
                _, ext = os.path.splitext(path)
            elif containsDirs:
                ext = 'multidicom' # "fake" extension to load a directory

        basename = os.path.basename(path)
        is3D = False

        self.setSplash(True, 0, 2, "Loading mask")

        def fail(text):
            self.setSplash(False, 0, 2, "Loading mask")
            self.alert(text, "Error")

        def load_mask_validate(name, mask):
            if name.lower().endswith('.nii'):
                name = name[:-4]
            if mask.shape[0] != self.image.shape[0] or mask.shape[1] != self.image.shape[1]:
                print("Mask shape", mask.shape, "self image shape", self.image.shape)
                fail("Mask size mismatch")
                return
            if mask.ndim > 2:
                is3D = True
                if mask.shape[2] != len(self.imList):
                    print("Mask shape", mask.shape, "self length", len(self.imList))
                    fail("Mask size mismatch")
                    return
            mask = mask > 0
            self.masksToRois({name: mask}, int(self.curImage)) # this is OK for 2D and 3D

        def align_masks(medical_volume):
            # check if 1) we have dicom headers to align the dataset and 2) the datasets are not already aligned
            if (self.affine is not None and
                    (not np.all(np.isclose(self.affine, medical_volume.affine, rtol=1e-3)) or
                     not np.all(medical_volume.shape == self.medical_volume.shape))):
                print("Aligning masks")
                self.setSplash(True, 1, 3, "Performing alignment")

                realigned_volume = realign_medical_volume(medical_volume, self.medical_volume, interpolation_order=0)

                mask = realigned_volume.volume
            else:
                # we cannot align the datasets
                print("Skipping alignment")
                mask = medical_volume.volume
            return mask

        def load_accumulated_mask(names, accumulated_mask):
            accumulated_mask = accumulated_mask.astype(np.uint16)
            if names is None:
                # load data without legend
                mask_values = np.unique(accumulated_mask)
                for index in mask_values:
                    if index == 0:
                        continue
                    print("Loading mask", index)
                    mask = np.zeros_like(accumulated_mask)
                    mask[accumulated_mask == index] = 1
                    load_mask_validate(str(index), mask)
                return

            for index, name in names.items():
                print("Loading mask", name, "with index", index)
                mask = np.zeros_like(accumulated_mask)
                mask[accumulated_mask == int(index)] = 1
                load_mask_validate(name, mask)

        def read_names_from_legend(legend_file):
            name_dict = {}
            with open(legend_file, newline='') as csv_file:
                reader = csv.reader(csv_file)
                header = next(reader)
                for row in reader:
                    name_dict[row[0]] = row[1]
                    print(row[0], row[1])
            return name_dict


        ext = ext.lower()

        if ext in npy_ext:
            mask = np.load(path)
            name = basename
            self.setSplash(True, 1, 2, "Importing masks")
            load_mask_validate(name, mask)
            self.setSplash(False, 0, 0, "")
            return
        if ext in npz_ext:
            mask_dict = np.load(path)
            n_masks = len(mask_dict)
            cur_mask = 0
            for name, mask in mask_dict.items():
                self.setSplash(True, cur_mask, n_masks, "Importing masks")
                load_mask_validate(name, mask)
            self.setSplash(False, 0, 0, "")
            return
        elif ext in nii_ext:
            mask_medical_volume, *_ = dosma_volume_from_path(path, reorient_data=False, sort=GlobalConfig['DICOM_SORT'])
            name, _ = os.path.splitext(os.path.basename(path))

            mask = align_masks(mask_medical_volume)

            self.setSplash(True, 2, 3, "Importing masks")
            if mask.max() > 1: # dataset with multiple labels
                # try loading the legend
                legend_name = path + '.csv'
                try:
                    names = read_names_from_legend(legend_name)
                except FileNotFoundError:
                    self.alert(f'Legend file not found. Loading mask without legend.', 'Warning')
                    names = None
                load_accumulated_mask(names, mask)
            else:
                load_mask_validate(name, mask)
            self.setSplash(False, 0, 0, "")
            return
        elif ext in dicom_ext:
            # load dicom masks
            path = os.path.dirname(path)
            mask_medical_volume, *_ = dosma_volume_from_path(path, reorient_data=False, sort=GlobalConfig['DICOM_SORT'])
            name = os.path.basename(path)

            mask = align_masks(mask_medical_volume)
            self.setSplash(True, 2, 3, "Importing masks")
            if mask.max() > 1: # dataset with multiple labels
                # try loading the legend
                legend_name = os.path.join(path, 'legend.csv')
                try:
                    names = read_names_from_legend(legend_name)
                except FileNotFoundError:
                    self.alert(f'Legend file not found. Loading mask without legend.', 'Warning')
                    names = None
                load_accumulated_mask(names, mask)
            else:
                load_mask_validate(name, mask)
            self.setSplash(False, 0, 0, "")
            return
        elif ext == 'multidicom' or len(nii_list) > 0:
            if ext == 'multidicom':
                path_list = dir_list
            else:
                path_list = nii_list
            # load multiple dicom masks and align them at the same time
            accumulated_mask = None
            current_mask_number = 1
            dicom_info_ok = None
            names = []
            for data_path in path_list:
                if data_path.startswith('.'): continue
                try:
                    mask_medical_volume, *_ = dosma_volume_from_path(data_path, reorient_data=False, sort=GlobalConfig['DICOM_SORT'])
                except:
                    continue
                dataset = mask_medical_volume.volume
                dataset[dataset > 0] = 1
                dataset[dataset < 1] = 0
                name, _ = os.path.splitext(os.path.basename(data_path))
                if accumulated_mask is None:
                    accumulated_mask = mask_medical_volume
                else:
                    try:
                        accumulated_mask.volume += dataset*current_mask_number
                    except:
                        print('Incompatible mask')
                        continue
                names.append(name)
                current_mask_number += 1
            if len(names) == 0:
                self.alert('No available mask found!')
                return

            aligned_masks = align_masks(accumulated_mask).astype(np.uint8)

            self.setSplash(True, 2, 3, "Importing masks")
            load_accumulated_mask(names, aligned_masks)
            self.setSplash(False, 0, 0, "")
            return

    @pyqtSlot(str)
    def save_data_as_reoriented_nifti(self, path):
        self.setSplash(True, 1, 3, "Saving data")
        reoriented_volume = reorient_data_ui(self.medical_volume, self.fig.canvas, inplace=False)
        nifti_writer = NiftiWriter()
        nifti_name = os.path.abspath(path)
        nifti_writer.save(reoriented_volume, nifti_name)
        self.setSplash(False, 0, 0, "")

    @pyqtSlot(str)
    def reorient_data(self, orientation):
        print(orientation)
        if self.medical_volume is None:
            return
        medical_volume = self.medical_volume
        self.resetInternalState()
        self.resetInterface()
        if orientation == 'Invert Slices':
            current_orientation = medical_volume.orientation
            slc_orientation = current_orientation[2]
            new_slc_orientation = slc_orientation[1] + slc_orientation[0]
            new_medical_volume = medical_volume.reformat((current_orientation[0], current_orientation[1], new_slc_orientation))
        else:
            new_medical_volume = medical_volume.reformat(get_nifti_orientation(orientation))
            new_medical_volume._headers = None
        self.load_dosma_volume(new_medical_volume)
        self.roiManager = ROIManager(self.imList[0].shape)
        self.registrationManager = RegistrationManager(self.imList,
                                                       None,
                                                       os.getcwd(),
                                                       GlobalConfig['TEMP_DIR'])
        self.registrationManager.set_standard_transforms_name(self.basepath, self.basename)
        # self.loadROIPickle()
        self.updateRoiList()
        self.override_class = None
        self.update_all_classifications()
        self.toolbox_window.set_exports_enabled(numpy= True,
                                                dicom= (self.dicomHeaderList is not None),
                                                nifti= (self.affine is not None)
                                                )
        self.axes.set_xlim(auto=True)
        self.axes.set_ylim(auto=True)
        self.displayImage(0)
        self.axes.set_xlim(auto=False)
        self.axes.set_ylim(auto=False)





    ########################################################################################
    ###
    ### Deep learning functions
    ###
    ########################################################################################

    @pyqtSlot(str, str)
    def importModel(self, modelFile, modelName):
        self.setSplash(True, 0, 1, 'Importing model...')

        modelName = modelName.replace('_', '-').replace(',', '.')

        try:
            self.model_provider.import_model(modelFile, modelName)
        except AttributeError:
            self.alert('Model provider does not support import')
            self.setSplash(False, 0, 1, 'Importing model...')
            return
        except Exception as err:
            self.alert('Error while importing model. Probably invalid model', 'Error')
            self.setSplash(False, 0, 1, 'Importing model...')
            traceback.print_exc()
            return
        self.setSplash(True, 1, 1, 'Importing model...')
        self.alert('Model imported successfully', 'Info')
        self.setSplash(False, 1, 1, 'Importing model...')
        GlobalConfig['ENABLED_MODELS'].append(modelName)
        self.setAvailableClasses(self.model_provider.available_models())

    def setModelProvider(self, modelProvider):
        self.model_provider = modelProvider
        if GlobalConfig['USE_CLASSIFIER']:
            try:
                self.dl_classifier = modelProvider.load_model('Classifier', force_download=GlobalConfig['FORCE_MODEL_DOWNLOAD'])
            except:
                self.dl_classifier = None
        else:
            self.dl_classifier = None

    def setAvailableClasses(self, classList, filter_classes = False):
        original_classifications = self.classifications[:]
        try:
            classList.remove('Classifier')
        except ValueError: # Classifier doesn't exist. It doesn't matter
            pass

        new_class_list = []
        self.model_details = {}
        for c in classList:
            if self.model_provider is None:
                new_class_list.append(c)
            else:
                model_details = self.model_provider.model_details(c)
                self.model_details[c] = model_details
                # if filter_classes, only show explicitly enabled models
                if filter_classes and c not in GlobalConfig['ENABLED_MODELS']:
                    continue
                try:
                    variants = model_details['variants']
                except:
                    new_class_list.append(c)
                    continue
                for variant in variants:
                    if variant.strip() == '':
                        new_class_list.append(c)
                    else:
                        new_class_list.append(f'{c}, {variant}')

        for i, classification in enumerate(original_classifications[:]):
            if classification not in new_class_list:
                original_classifications[i] = 'None'
        self.toolbox_window.set_available_classes(new_class_list, self.model_details)

        try:
            self.toolbox_window.set_class(original_classifications[int(self.curImage)])  # update the classification combo
        except IndexError:
            pass

    @pyqtSlot(str)
    @pyqtSlot(str)
    def changeClassification(self, newClass):
        try:
            self.classifications[int(self.curImage)] = newClass
        except IndexError:
            print("Trying to change classification to an unexisting image")

    @pyqtSlot(str)
    def changeAllClassifications(self, newClass):
        for i in range(len(self.classifications)):
            self.classifications[i] = newClass

    @pyqtSlot(int, int)
    @separate_thread_decorator
    def doSegmentationMultislice(self, min_slice, max_slice):
        if min_slice > max_slice: # invert order if one is bigger than the other
            min_slice, max_slice = max_slice, min_slice

        for slice_number in range(min_slice, max_slice+1):
            self.displayImage(slice_number)
            self.doSegmentation()
            self.setSplash(True, 0, 3, "Loading model...")
            time.sleep(0.5)
        self.setSplash(False, 0, 3, "")

    def getSegmentedMasks(self, imIndex, setSplash=False, downloadModel=True):
        class_str = self.classifications[imIndex]
        if class_str == 'None':
            self.alert('Segmentation with "None" model is impossible!', 'Error')
            return

        model_str = class_str.split(',')[0].strip()  # get the base model string in case of multiple variants.
        # variants are identified by "Model, Variant"

        if setSplash:
            self.setSplash(True, 0, 3, "Loading model...")

        try:
            segmenter = self.dl_segmenters[model_str]
        except KeyError:
            if downloadModel:
                if setSplash:
                    splashCallback = lambda cur_val, max_val: self.setSplash(True, cur_val, max_val,
                                                                                               'Downloading Model...')
                else:
                    splashCallback = None
                segmenter = self.model_provider.load_model(model_str, splashCallback,
                                                       force_download=GlobalConfig['FORCE_MODEL_DOWNLOAD'])
                if segmenter is None:
                    self.setSplash(False, 0, 3, "Loading model...")
                    self.alert(f"Error loading model {model_str}", 'Error')
                    return None
                self.dl_segmenters[class_str] = segmenter
            else:
                return None

        if setSplash:
            self.setSplash(True, 1, 3, "Running segmentation...")

        image = self.imList[imIndex]
        if self.toolbox_window.get_subregion_restriction():
            subregion = self.roiManager.get_autosegment_subregion(imIndex)
            image = image[subregion[0]:(subregion[0] + subregion[2]), subregion[1]:(subregion[1]+subregion[3])]

        inputData = {'image': image, 'resolution': self.resolution[0:2],
                     'split_laterality': GlobalConfig['SPLIT_LATERALITY'], 'classification': class_str}
        print("Segmenting image...")
        masks_out = segmenter(inputData)
        if self.toolbox_window.get_subregion_restriction():
            # reformat the masks
            new_masks_out = {}
            for mask_name, mask in masks_out.items():
                new_masks_out[mask_name] = np.zeros_like(self.imList[imIndex])
                new_masks_out[mask_name][subregion[0]:(subregion[0] + subregion[2]), subregion[1]:(subregion[1]+subregion[3])] = mask
            masks_out = new_masks_out
        return masks_out

    @pyqtSlot()
    @snapshotSaver
    def doSegmentation(self):
        # run the segmentation
        imIndex = int(self.curImage)

        t = time.time()
        masks_out=self.getSegmentedMasks(imIndex, True, True)
        if masks_out is None:
            self.setSplash(False, 0, 3, "Loading model...")
            return
        self.setSplash(True, 2, 3, "Converting masks...")
        print("Done")
        self.masksToRois(masks_out, imIndex)
        self.activeMask = None
        self.otherMask = None
        print("Segmentation/import time:", time.time() - t)
        self.setSplash(False, 3, 3)
        time.sleep(0.1)
        self.redraw()

    #@pyqtSlot()
    #@separate_thread_decorator # this crashes tensorflow!!
    @pyqtSlot()
    def incrementalLearnStandalone(self):
        self.setSplash(True, 0, 4, "Calculating maps...")
        allMasks, dataForTraining, segForTraining, meanDiceScore = self.calcOutputData(setSplash=True)
        self.setSplash(True, 1, 4, "Incremental learning...")
        # perform incremental learning
        self.incrementalLearn(dataForTraining, segForTraining, meanDiceScore, True)
        self.setSplash(False, 3, 4, "Saving file...")

    def incrementalLearn(self, dataForTraining, segForTraining, meanDiceScore, setSplash=False):
        performed = False
        for classification_name in dataForTraining:
            if classification_name == 'None': continue
            print(f'Performing incremental learning for {classification_name}')
            if len(dataForTraining[classification_name]) < GlobalConfig['IL_MIN_SLICES']:
                print(f"Not enough slices for {classification_name}")
                continue
            performed = True
            model_str = classification_name.split(',')[0].strip()  # get the base model string in case of multiple variants.
                                                        # variants are identified by "Model, Variant"
            try:
                model = self.dl_segmenters[model_str]
            except KeyError:
                model = self.model_provider.load_model(model_str, force_download=GlobalConfig['FORCE_MODEL_DOWNLOAD'])
                if model is None:
                    self.setSplash(False, 0, 3, "Loading model...")
                    self.alert(f"Error loading model {model_str}", 'Error')
                    return
                self.dl_segmenters[model_str] = model
            training_data = []
            training_outputs = []
            for imageIndex in dataForTraining[classification_name]:
                training_data.append(dataForTraining[classification_name][imageIndex])
                training_outputs.append(segForTraining[classification_name][imageIndex])
                self.slicesUsedForTraining.add(imageIndex) # add the slice to the set of already used ones

            try:
                # todo: adapt bs and minTrainImages if needed
                model.incremental_learn({'image_list': training_data, 'resolution': self.resolution[0:2], 'classification': classification_name},
                                        training_outputs, bs=5, minTrainImages=GlobalConfig['IL_MIN_SLICES'])
                model.reset_timestamp()
            except Exception as e:
                print("Error during incremental learning")
                traceback.print_exc()

            # Uploading new model

            # Only upload delta, to reduce model size -> only activate if rest of federated learning
            # working properly
            # all weights lower than threshold will be set to 0 for model compression
            # threshold = 0.0001
            # model = model.calc_delta(orig_model, threshold=threshold)
            if setSplash:
                self.setSplash(True, 2, 4, "Sending the improved model to server...")

            st = time.time()
            if meanDiceScore is None:
                meanDiceScore = -1.0
            self.model_provider.upload_model(model_str, model, meanDiceScore)
            print(f"took {time.time() - st:.2f}s")
        if not performed:
            self.alert("Not enough images for incremental learning")