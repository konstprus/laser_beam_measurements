# 
# Project: laser_beam_measurements
#
# File: camera_selector.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import QObject, Slot, Signal
from .camera_factory import CameraFactory
from .camera_grabber import CameraGrabber

__all__ = ["CameraSelector"]


class CameraSelector(QObject):

    signal_camera_selected = Signal(str, str, float)
    signal_factory_selected = Signal(list)

    def __init__(self, parent=None):
        super(CameraSelector, self).__init__(parent)
        self._factory = CameraFactory()
        self._grabber: CameraGrabber | None = None
        if isinstance(parent, CameraGrabber):
            self._grabber = parent

    def set_grabber(self, camera_grabber: CameraGrabber):
        self._grabber = camera_grabber

    @Slot(str, object, object)
    def slot_select_camera(self, factory_name: str, camera_id, pixel_size: float | None) -> None:
        if self._grabber is None:
            return
        # camera = None
        if pixel_size is None:
            camera = self._factory.create_camera(factory_name, camera_id)
        else:
            camera = self._factory.create_camera(factory_name, camera_id, pixel_size=pixel_size)
        if camera:
            camera.open()
            self._grabber.set_camera(camera)

            _camera_type = camera.type
            _camera_id = camera.camera_id
            _pixel_size = camera.pixel_size
            self.signal_camera_selected.emit(_camera_type, _camera_id, _pixel_size)

    @Slot(str)
    def slot_select_factory(self, factory_name: str) -> None:
        factory = self._factory.get_factory(factory_name)
        if factory is None:
            return
        available_cameras = factory.get_available_devices()
        self.signal_factory_selected.emit(available_cameras)

    def get_available_factories(self) -> list[str]:
        return self._factory.camera_device_types
