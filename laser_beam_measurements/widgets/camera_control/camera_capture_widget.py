#
# Project: laser_beam_measurements
#
# File: camera_capture_widget.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

# pyside6-uic laser_beam_measurements/widgets/camera_control/camera_capture_widget.ui -o laser_beam_measurements/widgets/camera_control/ui_camera_capture_widget.py

import numpy
from laser_beam_measurements.camera_control.camera_capture_widget_base import CameraCaptureWidgetBase
from PySide6.QtCore import Slot
from .ui_camera_capture_widget import Ui_Form
from laser_beam_measurements.widgets.utils.custom_graphics_scene import CustomGraphicsScene
from laser_beam_measurements.utils.colormap import COLORMAPS
from .camera_select_dialog import CameraSelectDialog
from laser_beam_measurements.camera_control.camera_selector import CameraSelector
from laser_beam_measurements.camera_control.camera_listener_base import CameraState


class CameraCaptureWidget(CameraCaptureWidgetBase):
    
    def __init__(self, parent=None, use_camera_select_dialog: bool = False):
        super(CameraCaptureWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Camera Capture")
        self.setObjectName("Camera Capture")

        self._scene = CustomGraphicsScene(self)
        self.ui.graphicsView.setScene(self._scene)

        self.ui.fps_slider.setTitle("fps")
        self.ui.gain_slider.setTitle("gain")
        self.ui.exposure_slider.setTitle("exposure")

        self._connect_signals()
        self._fill_colormap_combobox()
        self._use_camera_select_dialog: bool = use_camera_select_dialog

    def _connect_signals(self) -> None:
        self.ui.start_button.clicked.connect(self.start_button_clicked)
        self.ui.colormap_combo_box.currentTextChanged.connect(self.set_colormap)
        self.ui.exposure_slider.value_changed.connect(self._change_exposure_value)
        self.ui.fps_slider.value_changed.connect(self._change_fps_value)
        self.ui.gain_slider.value_changed.connect(self._change_gain_value)

    def _on_new_image(self, img: numpy.ndarray) -> None:
        self._scene.update_image(img)

    def _on_camera_state_changed(self, state: CameraState) -> None:
        if state == CameraState.STARTED:
            self._update_properties()
            self.ui.start_button.setText("Stop")
        else:
            self.ui.start_button.setText("Start")
            self._update_properties(disable_all=True)
            if self._use_camera_select_dialog:
                camera = self._camera_grabber.camera
                if camera is not None:
                    camera.close()

    def _on_error(self, error_message: str) -> None:
        pass

    def _on_statistic_got(self, frame_counter: int, error_counter: int, actual_fps: float) -> None:
        text_fps = "Actual FPS: {}".format(actual_fps)
        self.ui.fps_label.setText(text_fps)
        text_fps = "Frames: {}".format(int(frame_counter))
        self.ui.frames_label.setText(text_fps)
        text_fps = "Errors: {}".format(int(error_counter))
        self.ui.errors_label.setText(text_fps)

    def _fill_colormap_combobox(self) -> None:
        for name in COLORMAPS.get_names():
            self.ui.colormap_combo_box.addItem(name)

    @Slot(str)
    def set_colormap(self, name: str) -> None:
        self._scene.set_colormap(COLORMAPS.get_colormap(name))

    @Slot()
    def start_button_clicked(self):
        if self.ui.start_button.text() == "Start":
            if self._use_camera_select_dialog:
                self.show_camera_select_dialog()
            self.change_run_status(True)
        else:
            self.change_run_status(False)

    @Slot(float)
    def _change_exposure_value(self, value: float) -> None:
        self.signal_camera_property_changed.emit("exposure", value)

    @Slot(float)
    def _change_fps_value(self, value: float) -> None:
        self.signal_camera_property_changed.emit("fps", value)

    @Slot(float)
    def _change_gain_value(self, value: float) -> None:
        self.signal_camera_property_changed.emit("gain", value)

    def _update_properties(self, disable_all: bool = False) -> None:
        if disable_all:
            self.ui.fps_slider.setDisabled(True)
            self.ui.gain_slider.setDisabled(True)
            self.ui.exposure_slider.setDisabled(True)
        controller = self._property_controller
        if controller is not None:
            if not controller.available:
                return
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

    def _update_property_value(self, name: str, value: object) -> None:
        if name == "fps":
            self.ui.fps_slider.setValue(value)
        elif name == "gain":
            self.ui.gain_slider.setValue(value)
        elif name == "exposure":
            self.ui.exposure_slider.setValue(value)

    def show_camera_select_dialog(self):
        selector = CameraSelector(self._camera_grabber)
        selector.set_grabber(self._camera_grabber)
        camera_select_dialog = CameraSelectDialog(self)
        camera_select_dialog.set_selector(selector)
        camera_select_dialog.exec()
