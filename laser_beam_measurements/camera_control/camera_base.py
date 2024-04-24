#
# Project: laser_beam_measurements
#
# File: camera_base.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


__all__ = ["CameraBase", ]

import numpy
from .camera_property_base import CameraPropertyBase


class CameraBase(object):

    type = "Base"

    def __init__(self, **kwargs):
        self._pixel_size: float = kwargs.get("pixel_size", 1.0)
        self._id: str | int | None = kwargs.get('camera_id', None)
        self._resolution: tuple[int, int] | list[int, int] = kwargs.get('resolution', (1920, 1080))
        self._bit_depth: int = kwargs.get('bit_depth', 8)
        self._properties: dict[str, CameraPropertyBase] = {}
        self._initialize()

    def _initialize(self) -> None:
        pass

    def open(self, camera_id: str | int | None = None) -> None:
        pass

    def close(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def query_frame(self, *args, **kwargs) -> numpy.ndarray or None:
        pass

    @property
    def is_opened(self) -> bool:
        return False

    @property
    def pixel_size(self) -> float:
        return self._pixel_size

    @property
    def camera_id(self) -> str | int | None:
        return self._id

    def get_all_property_names(self) -> list[str]:
        return list(self._properties.keys())

    def has_property(self, name: str) -> bool:
        return name in self._properties.keys()

    def set_property_value(self, name, value) -> None:
        if name in self._properties.keys():
            self._properties.get(name).value = value

    def get_property_value(self, name) -> object | None:
        if name in self._properties.keys():
            return self._properties.get(name).value
        return None

    def get_property(self, name) -> CameraPropertyBase | None:
        if name in self._properties.keys():
            return self._properties.get(name)
        return None
