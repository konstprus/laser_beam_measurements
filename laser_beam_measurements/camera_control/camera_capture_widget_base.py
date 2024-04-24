# 
# Project: laser_beam_measurements
#
# File: camera_capture_widget_base.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QWidget
import numpy
from .camera_listener import CameraListener
from .camera_property_controller import CameraPropertyController
from .camera_grabber import CameraGrabber

__all__ = ["CameraCaptureWidgetBase"]


class CameraCaptureWidgetBase(QWidget):

    signal_grabber_status_run_changed = Signal(bool)
    signal_camera_property_changed = Signal(str, object)

    def __init__(self, parent=None, grabber: CameraGrabber | None = None):
        super(CameraCaptureWidgetBase, self).__init__(parent)
        self._listener: CameraListener | None = None
        self._camera_grabber: CameraGrabber | None = None
        self._property_controller: CameraPropertyController | None = None
        if grabber is not None:
            self.set_grabber(grabber)

    def set_camera_listener(self, listener: CameraListener) -> None:
        if self._listener:
            self._listener.signal_new_image_received.disconnect(self.on_new_image)
            self._listener.signal_camera_state_changed.disconnect(self.on_camera_state_changed)
            self._listener.signal_error_received.disconnect(self.on_error)
            self._listener.signal_statistic_collected.disconnect(self.on_statistic_got)
        self._listener = listener
        self._listener.signal_new_image_received.connect(self.on_new_image)
        self._listener.signal_camera_state_changed.connect(self.on_camera_state_changed)
        self._listener.signal_error_received.connect(self.on_error)
        self._listener.signal_statistic_collected.connect(self.on_statistic_got)

    def set_grabber(self, grabber: CameraGrabber) -> None:
        if self._camera_grabber:
            self._camera_grabber.run_status_changed(False)
            self.signal_grabber_status_run_changed.disconnect(self._camera_grabber.run_status_changed)
        self._camera_grabber = grabber
        self.signal_grabber_status_run_changed.connect(self._camera_grabber.run_status_changed)
        listener = self._camera_grabber.listener
        if isinstance(listener, CameraListener):
            self.set_camera_listener(listener)
        self.set_property_controller(self._camera_grabber.property_controller)

    def set_property_controller(self, controller: CameraPropertyController) -> None:
        if self._property_controller:
            self._property_controller.signal_camera_changed.disconnect(self.camera_is_set)
            self.signal_camera_property_changed.disconnect(self._property_controller.set_property_value)
            self._property_controller.signal_property_value_changed.disconnect(self.update_property_value)
        self._property_controller = controller
        self._property_controller.signal_camera_changed.connect(self.camera_is_set)
        self.signal_camera_property_changed.connect(self._property_controller.set_property_value)
        self._property_controller.signal_property_value_changed.connect(self.update_property_value)

    @Slot(numpy.ndarray)
    def on_new_image(self, img: numpy.ndarray) -> None:
        self._on_new_image(img)

    @Slot(bool)
    def on_camera_state_changed(self, state: bool) -> None:
        self._on_camera_state_changed(state)

    @Slot(str)
    def on_error(self, error_message: str) -> None:
        self._on_error(error_message)

    @Slot(int, int, float)
    def on_statistic_got(self, frame_counter: int, error_counter: int, actual_fps: float) -> None:
        self._on_statistic_got(frame_counter, error_counter, actual_fps)

    @Slot()
    def camera_is_set(self):
        self._update_properties()

    @Slot(str, object)
    def update_property_value(self, name: str, value: object) -> None:
        self.blockSignals(True)
        self._update_property_value(name, value)
        self.blockSignals(False)

    def change_run_status(self, status: bool) -> None:
        self.signal_grabber_status_run_changed.emit(status)

    def _on_new_image(self, img: numpy.ndarray) -> None:
        raise NotImplementedError()

    def _on_camera_state_changed(self, state: bool) -> None:
        raise NotImplementedError()

    def _on_error(self, error_message: str) -> None:
        raise NotImplementedError()

    def _on_statistic_got(self, frame_counter: int, error_counter: int, actual_fps: float) -> None:
        raise NotImplementedError()

    def _update_properties(self, disable_all: bool = False) -> None:
        raise NotImplementedError()

    def _update_property_value(self, name: str, value: object) -> None:
        raise NotImplementedError()

    def closeEvent(self, event):
        if self._camera_grabber:
            self._camera_grabber.run_status_changed(False)
        super(CameraCaptureWidgetBase, self).closeEvent(event)
