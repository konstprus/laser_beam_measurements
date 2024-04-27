#
# Project: laser_beam_measurements
#
# File: camera_factory_base.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from .camera_base import CameraBase

__all__ = ["CameraCreateException", "CameraFactoryBase"]


class CameraCreateException(Exception):
    pass


class CameraFactoryBase(object):

    camera_class: type(CameraBase) | None = None

    def __init__(self, func=None, **kwargs):
        self._func = func
        self._config_file = str(kwargs.get("config_file", None))

    def get_available_devices(self, *args, **kwargs) -> list:
        if isinstance(self._func, list):
            return self._func
        if hasattr(self._func, '__call__'):
            return self._func(*args, **kwargs)
        if hasattr(self, "_get_available_devices"):
            return self._get_available_devices(*args, **kwargs)
        return []

    def create(self, camera_id=None, *args, **kwargs):
        if self.camera_class:
            try:
                if camera_id is not None:
                    return self.camera_class(camera_id=camera_id, *args, **kwargs)
            except Exception as ex:
                raise CameraCreateException(
                    f"Error occurred during creation of camera object. Error message: {ex}")
        raise CameraCreateException("Camera class is not registered")
