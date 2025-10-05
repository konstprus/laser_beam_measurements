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
from .virtual_camera import VirtualCamera


class VirtualCameraFactory(CameraFactoryBase):
    camera_class = VirtualCamera

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
