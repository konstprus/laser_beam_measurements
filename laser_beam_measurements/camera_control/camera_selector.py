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
from dataclasses import dataclass
from typing import Optional
from .pixel_format import PixelFormat

__all__ = ["CameraSelector", "CameraParameters"]

@dataclass
class CameraParameters:
    factory: str
    camera_id: str
    pixel_size: Optional[float]
    pixel_format: Optional[str]



class CameraSelector(QObject):

    # signal_camera_selected = Signal(str, str, float)
    signal_camera_selected = Signal(dict)
    signal_factory_selected = Signal(list)
    signal_pixel_formats_selected = Signal(list)

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

    @Slot(CameraParameters)
    def slot_select_camera(self, cp: CameraParameters) -> None:
        if self._grabber is None:
            return

        params = dict()
        if cp.pixel_size is not None:
            params.update({"pixel_size": cp.pixel_size})
        if cp.pixel_format is not None:
            params.update({"pixel_format": cp.pixel_format})
        camera = self._factory.create_camera(cp.factory, cp.camera_id, **params)
        self.set_camera(camera)

    @Slot(str)
    def slot_select_factory(self, factory_name: str) -> None:
        factory = self._factory.get_factory(factory_name)
        if factory is None:
            return
        available_cameras = factory.get_available_devices()
        self.signal_factory_selected.emit(available_cameras)

    @Slot(str, str)
    def slot_select_camera_id(self, factory_name: str, camera_id: str) -> None:
        factory = self._factory.get_factory(factory_name)
        if factory is None:
            return
        pixel_formats = factory.get_available_pixel_formats(camera_id)
        pf_list = [str(pf) for pf in pixel_formats]
        self.signal_pixel_formats_selected.emit(pf_list)

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
        settings.setValue("PixelFormat", camera.pixel_format.name)
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
                kwargs = dict()
                if settings.contains("PixelFormat"):
                    pixel_format_str = settings.value("PixelFormat")
                    kwargs.update({"pixel_format": pixel_format_str})
                camera = factory.create(camera_id, pixel_size=pixel_size, **kwargs)
                self.set_camera(camera)
            else:
                return
            settings.endGroup()

        except Exception as ex:
            # print(str(ex))
            pass
