# 
# Project: laser_beam_measurements
#
# File: camera_selector.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import QObject, Slot, Signal, QSettings
from .camera_factory import CameraFactory
from .camera_grabber import CameraGrabber
from .camera_base import CameraBase

__all__ = ["CameraSelector"]


class CameraSelector(QObject):

    # signal_camera_selected = Signal(str, str, float)
    signal_camera_selected = Signal(dict)
    signal_factory_selected = Signal(list)

    def __init__(self, parent=None):
        _parent = None
        if not isinstance(parent, CameraGrabber):
            _parent = parent
        super(CameraSelector, self).__init__(_parent)
        self._factory = CameraFactory()
        self._grabber: CameraGrabber | None = None
        if isinstance(parent, CameraGrabber):
            self.set_grabber(parent)
            # self._grabber = parent
            # self.moveToThread(self._grabber.thread())
            # self.setParent(self._grabber)

    def set_grabber(self, camera_grabber: CameraGrabber):
        self._grabber = camera_grabber
        self.moveToThread(self._grabber.thread())
        self.setParent(self._grabber)

    @Slot(str, object, object)
    def slot_select_camera(self, factory_name: str, camera_id, pixel_size: float | None) -> None:
        if self._grabber is None:
            return
        # camera = None
        if pixel_size is None:
            camera = self._factory.create_camera(factory_name, camera_id)
        else:
            camera = self._factory.create_camera(factory_name, camera_id, pixel_size=pixel_size)
        self.set_camera(camera)
        # if camera:
        #     camera.open()
        #     self._grabber.set_camera(camera)
        #
        #     _camera_type = camera.type
        #     _camera_id = camera.camera_id
        #     _pixel_size = camera.pixel_size
        #     self.signal_camera_selected.emit(_camera_type, _camera_id, _pixel_size)

    @Slot(str)
    def slot_select_factory(self, factory_name: str) -> None:
        factory = self._factory.get_factory(factory_name)
        if factory is None:
            return
        available_cameras = factory.get_available_devices()
        self.signal_factory_selected.emit(available_cameras)

    def set_camera(self, camera: CameraBase) -> None:
        if camera is None:
            return
        if not camera.is_opened:
            camera.open()
        self._grabber.set_camera(camera)

        _camera_type = camera.type
        _camera_id = camera.camera_id
        _pixel_size = camera.pixel_size
        camera_parameters = {
            "camera_type": _camera_type,
            "camera_id": _camera_id,
            "pixel_size": _pixel_size,
        }
        self.signal_camera_selected.emit(camera_parameters)
        # self.signal_camera_selected.emit(_camera_type, _camera_id, _pixel_size)

    def get_available_factories(self) -> list[str]:
        return self._factory.camera_device_types

    def save_settings(self, settings: QSettings) -> None:
        camera = self._grabber.camera
        if camera is None:
            return
        settings.beginGroup("CameraConfiguration")
        settings.setValue("Type", camera.type)
        settings.setValue("CameraID", camera.camera_id)
        settings.setValue("PixelSize", camera.pixel_size)
        settings.endGroup()

    def load_settings(self, settings: QSettings) -> None:
        try:
            settings.beginGroup("CameraConfiguration")
            camera_type = None
            if settings.contains("Type"):
                camera_type = str(settings.value("Type"))
            if camera_type is None:
                return
            if camera_type not in self._factory.camera_types:
                return
            factory = self._factory.get_factory_by_camera_type(camera_type)
            if factory is None:
                return
            if settings.contains("CameraID"):
                camera_id = settings.value("CameraID")
                pixel_size = settings.value("PixelSize", 1.0)
                camera = factory.create(camera_id, pixel_size=pixel_size)
                self.set_camera(camera)
            else:
                return
            settings.endGroup()

        except Exception as ex:
            # print(str(ex))
            pass
