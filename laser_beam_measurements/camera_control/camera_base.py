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
from typing import Union, Optional

from .pixel_format import PixelFormat, PixelFormatEnum, get_pixel_format

CameraID = Union[int, str]

class CameraBase(object):

    type = "Base"

    def __init__(self, *args, **kwargs):
        self._pixel_size: float = kwargs.get("pixel_size", 1.0)
        self._id: str | int | None = kwargs.get('camera_id', None)
        self._resolution: tuple[int, int] = kwargs.get('resolution', (1920, 1080))
        self._bit_depth: int = kwargs.get('bit_depth', 8)
        self._properties: dict[str, CameraPropertyBase] = {}
        self._pixel_format: PixelFormat = get_pixel_format(PixelFormatEnum.DEFAULT)
        pixel_format_name = kwargs.get("pixel_format", get_pixel_format(PixelFormatEnum.DEFAULT))
        if isinstance(pixel_format_name, str):
            pixel_format = get_pixel_format(pixel_format_name)
            if pixel_format is not None:
                self._pixel_format = pixel_format

        self._initialize()

    def _initialize(self) -> None:
        pass

    def open(self, camera_id: Optional[CameraID] = None) -> None:
        pass

    def close(self) -> None:
        pass

    def start(self) -> None:
        pass

    def stop(self) -> None:
        pass

    def query_frame(self, *args, **kwargs) -> Optional[numpy.ndarray]:
        pass

    @property
    def is_opened(self) -> bool:
        return False

    @property
    def pixel_size(self) -> float:
        return self._pixel_size

    @property
    def resolution(self) -> tuple[int, int]:
        return self._resolution

    @property
    def camera_id(self) -> Union[str, int, None]:
        return self._id

    @property
    def pixel_format(self) -> PixelFormat:
        return self._get_pixel_format()

    def _get_pixel_format(self) -> PixelFormat:
        return self._pixel_format

    def get_all_property_names(self) -> list[str]:
        return list(self._properties.keys())

    def has_property(self, name: str) -> bool:
        return name in self._properties.keys()

    def set_property_value(self, name, value) -> None:
        if name in self._properties.keys():
            self._properties.get(name).value = value

    def get_property_value(self, name) -> Optional[object]:
        if name in self._properties.keys():
            return self._properties.get(name).value
        return None

    def get_property(self, name) -> Optional[CameraPropertyBase]:
        if name in self._properties.keys():
            return self._properties.get(name)
        return None

    def has_property_dialog(self) -> bool:
        return False

    def show_property_dialog(self) -> None:
        pass
