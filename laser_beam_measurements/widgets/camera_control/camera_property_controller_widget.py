# 
# Project: laser_beam_measurements
#
# File: camera_property_controller_widget.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

# pyside6-uic laser_beam_measurements/widgets/camera_control/camera_property_controller_widget.ui -o laser_beam_measurements/widgets/camera_control/ui_camera_property_controller_widget.py


from PySide6.QtWidgets import QWidget, QTableWidgetItem
from PySide6.QtCore import Slot, Signal
from laser_beam_measurements.camera_control.camera_property_controller import CameraPropertyController
from laser_beam_measurements.camera_control.camera_property_auto_controller import CameraPropertyAutoController
from laser_beam_measurements.camera_control.camera_base import CameraBase
from laser_beam_measurements.camera_control.camera_property_base import CameraPropertyBase
from laser_beam_measurements.icons import Icon

from .ui_camera_property_controller_widget import Ui_Form


class CameraPropertyControllerWidget(QWidget):

    signal_camera_property_changed = Signal(str, object)

    def __init__(self, parent=None, property_controller: CameraPropertyController | None = None):
        super(CameraPropertyControllerWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._property_controller: CameraPropertyController | None = None
        self._auto_controller: CameraPropertyAutoController | None = None
        self._connect_signals()
        if property_controller is not None:
            self.set_controller(property_controller)
        self.ui.auto_control_run_button.setIcon(Icon('update.svg'))
        # self.ui.property_dialog_button.clicked.connect(self.show_property_dialog)
        # self.ui.property_dialog_button.setVisible(False)

    def set_controller(self, property_controller: CameraPropertyController) -> None:
        if self._property_controller:
            self._property_controller.signal_camera_changed.disconnect(self.slot_camera_changed)
            self.signal_camera_property_changed.disconnect(self._property_controller.set_property_value)
            self._property_controller.signal_property_value_changed.disconnect(self.slot_update_property_value)
            self._property_controller.signal_camera_unset.disconnect(self.slot_camera_unset)
        self._property_controller = property_controller
        self._property_controller.signal_camera_changed.connect(self.slot_camera_changed)
        self.signal_camera_property_changed.connect(self._property_controller.set_property_value)
        self._property_controller.signal_property_value_changed.connect(self.slot_update_property_value)
        self._property_controller.signal_camera_unset.connect(self.slot_camera_unset)
        # if self._property_controller.property_dialog_available:
        #     self.ui.property_dialog_button.setEnabled(True)
        # else:
        #     self.ui.property_dialog_button.setEnabled(False)
        self._update_properties()

    def set_auto_controller(self, auto_controller: CameraPropertyAutoController) -> None:
        if self._auto_controller:
            self._auto_controller.set_active(False)
            self._auto_controller.signal_check_result.disconnect(self.ui.status_label.show_status)
            self.ui.auto_control_run_button.clicked.disconnect(self._auto_controller.slot_control_change)
            # self.ui.auto_control_run_check_box.disconnect(self._auto_controller.slot_control_always_change)
            self.ui.auto_control_run_check_box.checkStateChanged.disconnect(self._auto_controller.set_control_always)

        self._auto_controller = auto_controller
        self._auto_controller.signal_check_result.connect(self.ui.status_label.show_status)
        self.ui.auto_control_run_button.clicked.connect(self._auto_controller.slot_control_change)
        # self.ui.auto_control_run_check_box.clicked.connect(self._auto_controller.slot_control_always_change)
        self.ui.auto_control_run_check_box.checkStateChanged.connect(self._auto_controller.set_control_always)
        self._auto_controller.set_active(True)


    @Slot()
    def slot_camera_changed(self) -> None:
        self._update_properties()
        # if self._property_controller.property_dialog_available:
        #     self.ui.property_dialog_button.setEnabled(True)
        #     self.ui.property_dialog_button.clicked.connect(self._property_controller.show_property_dialog)
        # else:
        #     self.ui.property_dialog_button.setEnabled(False)

    def _update_properties(self, disable_all: bool = False) -> None:
        if disable_all:
            self.ui.fps_slider.setDisabled(True)
            self.ui.gain_slider.setDisabled(True)
            self.ui.exposure_slider.setDisabled(True)
            info = {
                "type": "",
                "id": "",
                "resolution": "",
                "pixel_size": ""
            }
            self._fill_camera_info(info)
            return
        controller = self._property_controller
        if controller is not None and controller.available:
            self.blockSignals(True)
            if controller.has_property("fps"):
                self.ui.fps_slider.setEnabled(True)
                prop = controller.get_property("fps")
                self.ui.fps_slider.setMinimum(prop.min)
                self.ui.fps_slider.setMaximum(prop.max)
                self.ui.fps_slider.setValue(prop.value)
            else:
                self.ui.fps_slider.setDisabled(True)

            if controller.has_property("gain"):
                self.ui.gain_slider.setEnabled(True)
                prop = controller.get_property("gain")
                self.ui.gain_slider.setMinimum(prop.min)
                self.ui.gain_slider.setMaximum(prop.max)
                self.ui.gain_slider.setValue(prop.value)
            else:
                self.ui.gain_slider.setDisabled(True)

            if controller.has_property("exposure"):
                self.ui.exposure_slider.setEnabled(True)
                prop = controller.get_property("exposure")
                self.ui.exposure_slider.setMinimum(prop.min)
                self.ui.exposure_slider.setMaximum(prop.max)
                self.ui.exposure_slider.setValue(prop.value)
            else:
                self.ui.exposure_slider.setDisabled(True)
            self.blockSignals(False)
            camera_info = controller.collect_camera_info()
            if camera_info is not None:
                self._fill_camera_info(camera_info)

    @Slot(str, object)
    def slot_update_property_value(self, name: str, value: object) -> None:
        self.blockSignals(True)
        self._update_property_value(name, value)
        self.blockSignals(False)

    @Slot()
    def slot_camera_unset(self) -> None:
        self._update_properties(disable_all=True)

    def _update_property_value(self, name: str, value: object) -> None:
        if name == "fps":
            self.ui.fps_slider.setValue(value)
        elif name == "gain":
            self.ui.gain_slider.setValue(value)
        elif name == "exposure":
            self.ui.exposure_slider.setValue(value)

    def _connect_signals(self) -> None:
        self.ui.exposure_slider.value_changed.connect(self._change_exposure_value)
        self.ui.fps_slider.value_changed.connect(self._change_fps_value)
        self.ui.gain_slider.value_changed.connect(self._change_gain_value)

    @Slot(float)
    def _change_exposure_value(self, value: float) -> None:
        self.signal_camera_property_changed.emit("exposure", value)

    @Slot(float)
    def _change_fps_value(self, value: float) -> None:
        self.signal_camera_property_changed.emit("fps", value)

    @Slot(float)
    def _change_gain_value(self, value: float) -> None:
        self.signal_camera_property_changed.emit("gain", value)

    def _fill_camera_info(self, info: dict) -> None:
        self.ui.camera_info.setItem(0, 0, QTableWidgetItem(info['type']))
        self.ui.camera_info.setItem(1, 0, QTableWidgetItem(info['id']))
        if isinstance(info['resolution'], (list, tuple)):
            matrix_shape = '{}x{} pixels'.format(info['resolution'][0], info['resolution'][1])
        else:
            matrix_shape = info['resolution']
        self.ui.camera_info.setItem(2, 0, QTableWidgetItem(matrix_shape))
        if info['pixel_size'] != '':
            pixel_size = '{} um'.format(info['pixel_size'])
        else:
            pixel_size = ''
        self.ui.camera_info.setItem(3, 0, QTableWidgetItem(pixel_size))

    @Slot()
    def show_property_dialog(self):
        if self._property_controller:
            self._property_controller.show_property_dialog()
