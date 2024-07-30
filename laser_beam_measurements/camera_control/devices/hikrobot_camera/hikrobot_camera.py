# 
# Project: laser_beam_measurements
#
# File: hikrobot_camera.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

import sys
sys.path.append("./MvImport")

from laser_beam_measurements.camera_control.camera_base import CameraBase
from MvImport import MvCameraControl_class as hik
from typing import override
import numpy


class HikCamera(CameraBase):

    type = "HikRobot"

    def __init__(self, **kwargs):
        super(HikCamera, self).__init__(**kwargs)
        self._device_info = hik.MV_CC_DEVICE_INFO
        self._cam = hik.MvCamera()

    @override
    def _initialize(self) -> None:
        pass

    @override
    def open(self, camera_id: str | int | None = None) -> None:
        if self._cam.MV_CC_CreateHandle(self._device_info) == 0:
            self._cam.MV_CC_OpenDevice(hik.MV_ACCESS_Exclusive, 0)

    @override
    def close(self) -> None:
        if self._cam.MV_CC_CloseDevice() == 0:
            self._cam.MV_CC_DestroyHandle()

    @override
    def start(self) -> None:
        self._cam.MV_CC_StartGrabbing()

    @override
    def stop(self) -> None:
        self._cam.MV_CC_StopGrabbing()

    @override
    def query_frame(self, *args, **kwargs) -> numpy.ndarray or None:
        pass
