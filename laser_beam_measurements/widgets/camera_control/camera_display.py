# 
# Project: laser_beam_measurements
#
# File: camera_display.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

# pyside6-uic laser_beam_measurements/widgets/camera_control/camera_display.ui -o laser_beam_measurements/widgets/camera_control/ui_camera_display.py

import numpy
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Slot, QSettings
from laser_beam_measurements.camera_control.camera_listener import CameraListener
from laser_beam_measurements.camera_control.camera_listener_base import CameraState
from laser_beam_measurements.widgets.utils.custom_graphics_scene import CustomGraphicsScene
from laser_beam_measurements.utils.colormap import COLORMAPS
from laser_beam_measurements.utils.image_saver import ImageSaver
from .ui_camera_display import Ui_Form


__all__ = ['CameraDisplay']


class CameraDisplay(QWidget):

    def __init__(self, parent=None, listener: CameraListener | None = None):
        super(CameraDisplay, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle("Display")
        self._scene = CustomGraphicsScene(self)
        self._set_colormap_name: str | None = None
        self.ui.graphicsView.setScene(self._scene)
        self._listener: CameraListener | None = None
        self._fill_colormap_combobox()
        if listener is not None:
            self.set_camera_listener(listener)
        self.ui.colormap_combo_box.currentTextChanged.connect(self.set_colormap)
        self._image_saver = ImageSaver(self)

    @Slot(numpy.ndarray)
    def on_new_image(self, img: numpy.ndarray) -> None:
        self._scene.update_image(img)

    @Slot(int, int, float)
    def on_statistic_got(self, frame_counter: int, error_counter: int, actual_fps: float) -> None:
        text_fps = "Actual FPS: {}".format(actual_fps)
        self.ui.fps_label.setText(text_fps)
        text_fps = "Frames: {}".format(int(frame_counter))
        self.ui.frames_label.setText(text_fps)
        text_fps = "Errors: {}".format(int(error_counter))
        self.ui.errors_label.setText(text_fps)

    @Slot()
    def save(self):
        self._image_saver.set_image(self._scene.image_item.raw_image)
        self._image_saver.set_colormap(self._scene.image_item.colormap)
        self._image_saver.show_save_dialog()

    def _fill_colormap_combobox(self) -> None:
        for name in COLORMAPS.get_names():
            self.ui.colormap_combo_box.addItem(name)

    @Slot(str)
    def set_colormap(self, name: str) -> None:
        self._set_colormap_name = name
        self._scene.set_colormap(COLORMAPS.get_colormap(name))

    @Slot(bool)
    def on_camera_state_changed(self, value: CameraState) -> None:
        if value == CameraState.CLOSED:
            self._scene.image_item.setVisible(False)
        else:
            self._scene.image_item.setVisible(True)

    def set_camera_listener(self, listener: CameraListener) -> None:
        if self._listener:
            self._listener.signal_new_image_received.disconnect(self.on_new_image)
            self._listener.signal_camera_state_changed.disconnect(self.on_camera_state_changed)
            self._listener.signal_statistic_collected.disconnect(self.on_statistic_got)
        self._listener = listener
        self._listener.signal_new_image_received.connect(self.on_new_image)
        self._listener.signal_camera_state_changed.connect(self.on_camera_state_changed)
        self._listener.signal_statistic_collected.connect(self.on_statistic_got)

    def save_widget_settings(self, settings: QSettings) -> None:
        settings.setValue("SetColormap", self._set_colormap_name)

    def load_widget_settings(self, settings: QSettings) -> None:
        if settings.contains("SetColormap"):
            colormap_name = str(settings.value("SetColormap"))
            self.set_colormap(colormap_name)
            self.ui.colormap_combo_box.setCurrentText(colormap_name)
