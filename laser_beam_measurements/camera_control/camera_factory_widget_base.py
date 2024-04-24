# 
# Project: laser_beam_measurements
#
# File: camera_factory_widget_base.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtWidgets import QDialog, QWidget

from .camera_factory import CameraFactory

__all__ = ["CameraFactoryWidgetBase"]


class CameraFactoryWidgetBase(QDialog):

    def __init__(self, parent=None):
        super(CameraFactoryWidgetBase, self).__init__(parent)
        self._factory: CameraFactory | None = None

    def set_factory(self, factory: CameraFactory) -> None:
        self._factory = factory

    def show_enabled_camera_types(self):
        if self._factory is not None:
            cameras = self._factory.camera_device_types
            self._show_enabled_camera_types(cameras)

    def show_available_devices(self, camera_type: str, *args, **kwargs) -> None:
        if self._factory is None:
            return
        factory = self._factory.get_factory(camera_type)
        if factory is None:
            return
        devices = factory.get_available_devices(*args, **kwargs)
        if len(devices) == 0:
            return
        self._show_available_devices(devices)

    def _show_enabled_camera_types(self, cameras: list[str]) -> None:
        raise NotImplementedError()

    def _show_available_devices(self, devices_list: list) -> None:
        raise NotImplementedError()

