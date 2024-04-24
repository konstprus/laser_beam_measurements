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
from .opencv_camera import OpenCVCamera


class OpenCVCameraFactory(CameraFactoryBase):
    camera_class = OpenCVCamera

    def __init__(self):
        super(OpenCVCameraFactory, self).__init__(func=[0])
