# 
# Project: laser_beam_measurements
#
# File: pixel_format.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from enum import StrEnum
from typing import Optional


class PixelFormat:

    def __init__(self,
                 name: str,
                 bit_depth: int = 8,
                 channels_number: int = 1,
                 **kwargs) -> None:
        self._name: str = name
        self._bit_depth: int = bit_depth
        self._max_pixel_value: int = 2**bit_depth - 1
        self._channels_number: int = channels_number

    def __str__(self) -> str:
        return self._name

    @property
    def name(self) -> str:
        return self._name

    @property
    def max_pixel_value(self) -> int:
        return self._max_pixel_value

    @property
    def channels_number(self) -> int:
        return self._channels_number

    @property
    def is_mono(self) -> bool:
        return self._channels_number == 1


DEFAULT_PIXEL_FORMAT = PixelFormat("default")
MONO8 = PixelFormat("mono8", bit_depth=8)
MONO10 = PixelFormat("mono10", bit_depth=10)
MONO12 = PixelFormat("mono12", bit_depth=12)


class PixelFormatEnum(StrEnum):
    DEFAULT = str(DEFAULT_PIXEL_FORMAT)
    MONO_8 = str(MONO8)
    MONO_10 = str(MONO10)
    MONO_12 = str(MONO12)


_pixel_formats_map: dict[str, PixelFormat] = {
    "default": DEFAULT_PIXEL_FORMAT,
    "mono8": MONO8,
    "mono10": MONO10,
    "mono12": MONO12,
}

def get_pixel_format(name: str) -> Optional[PixelFormat]:
    return _pixel_formats_map.get(name, None)

def get_pixel_range(pixel_format: PixelFormat) -> tuple[int, int]:
    max_pixel_value = pixel_format.max_pixel_value
    if max_pixel_value == MONO8.max_pixel_value:
        return 190, 240
    elif max_pixel_value == MONO10.max_pixel_value:
        return 760, 970
    elif max_pixel_value == MONO12.max_pixel_value:
        return 3000, 3900
    return 190, 240