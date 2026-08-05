#
# Project: laser_beam_measurements
#
# File: virtual_camera_factory.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from laser_beam_measurements.camera_control.camera_factory_base import CameraFactoryBase
from laser_beam_measurements.camera_control.pixel_format import PixelFormat, get_pixel_format, PixelFormatEnum
from .virtual_camera import VirtualCamera
from typing import Optional, Union

class VirtualCameraFactory(CameraFactoryBase):
    camera_class = VirtualCamera

    def get_available_pixel_formats(self, camera_id: Optional[Union[int, str]], *args, **kwargs) -> list[PixelFormat]:
        return [
            get_pixel_format(PixelFormatEnum.MONO_8),
            get_pixel_format(PixelFormatEnum.MONO_10),
            get_pixel_format(PixelFormatEnum.MONO_12),
        ]

    def __init__(self):
        super(VirtualCameraFactory, self).__init__(
            func=[
                "zero",
                "round",
                "perpendicular",
                "left",
                "right",
                "line"]
        )
