# 
# Project: laser_beam_measurements
#
# File: hikrobot_camera_factory.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from laser_beam_measurements.camera_control.camera_factory_base import CameraFactoryBase, CameraCreateException


class HikRobotCameraFactory(CameraFactoryBase):
    
    def __init__(self):
        super().__init__()