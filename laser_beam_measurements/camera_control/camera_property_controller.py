# 
# Project: laser_beam_measurements
#
# File: camera_property_controller.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from .camera_property_base import CameraPropertyBase
from .camera_base import CameraBase
from PySide6.QtCore import QObject, Signal, Slot, QMutex, QMutexLocker

__all__ = ["CameraPropertyController"]


class CameraPropertyController(QObject):

    signal_camera_changed = Signal()
    signal_property_value_changed = Signal(str, object)

    def __init__(self, parent: QObject = None, camera: CameraBase = None):
        super(CameraPropertyController, self).__init__(parent)
        self._camera: CameraBase | None = camera
        self._mutex = QMutex()
        # self._camera = camera

    def set_camera(self, camera: CameraBase) -> None:
        with QMutexLocker(self._mutex):
            self._camera = camera
        self.signal_camera_changed.emit()

    def unset_camera(self):
        with QMutexLocker(self._mutex):
            self._camera = None

    @property
    def available(self) -> bool:
        with QMutexLocker(self._mutex):
            if self._camera is None:
                return False
            return self._camera.is_opened

    def has_property(self, name: str) -> bool:
        if not self.available:
            return False
        with QMutexLocker(self._mutex):
            return self._camera.has_property(name)

    def get_property_value(self, name: str) -> object | None:
        with QMutexLocker(self._mutex):
            if self._camera.has_property(name):
                return self._camera.get_property_value(name)
            return None

    @Slot(str, object)
    def set_property_value(self, name: str, value: object) -> None:
        if self._camera.has_property(name):
            last_value = self._camera.get_property_value(name)
            print(last_value, value)
            if last_value is None:
                return
            if last_value != value:
                self._camera.set_property_value(name, value)
                self.signal_property_value_changed.emit(name, value)

    def get_property(self, name: str) -> CameraPropertyBase | None:
        with QMutexLocker(self._mutex):
            if self._camera.has_property(name):
                return self._camera.get_property(name)
            return None
