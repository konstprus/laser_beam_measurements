#
# Project: laser_beam_measurements
#
# File: opencv_camera_factory.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from laser_beam_measurements.camera_control.camera_factory_base import CameraFactoryBase
from laser_beam_measurements.camera_control.pixel_format import PixelFormat, get_pixel_format, PixelFormatEnum
from .opencv_camera import OpenCVCamera
from typing import Optional, Union


class OpenCVCameraFactory(CameraFactoryBase):
    camera_class = OpenCVCamera

    def get_available_pixel_formats(self, camera_id: Optional[Union[int, str]], *args, **kwargs) -> list[PixelFormat]:
        return [get_pixel_format(PixelFormatEnum.DEFAULT)]

    def __init__(self):
        super(OpenCVCameraFactory, self).__init__(func=[0])
