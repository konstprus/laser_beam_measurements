# 
# Project: laser_beam_measurements
#
# File: main_object.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget
from laser_beam_measurements.camera_control.camera_grabber import CameraGrabber
from laser_beam_measurements.camera_control.camera_selector import CameraSelector


class MainObject(QObject):

    def __init__(self, parent=None):
        super(MainObject, self).__init__(parent)
        self._camera_grabber: CameraGrabber = CameraGrabber()
        self._camera_selector: CameraSelector = CameraSelector(self._camera_grabber)

    @property
    def camera_grabber(self) -> CameraGrabber:
        return self._camera_grabber

    def set_display(self, display_widget: QWidget) -> False:
        if hasattr(display_widget, "set_camera_listener"):
            display_widget.set_camera_listener(self._camera_grabber.listener)

    @property
    def camera_selector(self) -> CameraSelector:
        return self._camera_selector
