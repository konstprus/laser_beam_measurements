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
import os

sys.path.append(str(os.path.dirname(os.path.realpath(__file__))) + "/MvImport")

from laser_beam_measurements.camera_control.camera_base import CameraBase
import numpy
from ctypes import *
from .MvImport import MvCameraControl_class as hik
from .MvImport import PixelType_header as PixelType
from .hikrobot_camera_property import HikRobotCameraProperty


class HikRobotCamera(CameraBase):

    type = "HikRobot"

    def __init__(self, device_info: hik.MV_CC_DEVICE_INFO, mv_cam: hik.MvCamera, **kwargs):
        self._device_info: hik.MV_CC_DEVICE_INFO = device_info
        self._cam: hik.MvCamera = mv_cam
        self._is_opened: bool = False
        self._st_out_frame: hik.MV_FRAME_OUT = hik.MV_FRAME_OUT()
        super(HikRobotCamera, self).__init__(**kwargs)

    def _initialize(self) -> None:
        memset(byref(self._st_out_frame), 0, sizeof(self._st_out_frame))

    def _init_properties(self) -> None:
        self._properties.clear()
        self._properties['fps'] = HikRobotCameraProperty(self._cam, 'fps', "AcquisitionFrameRate")
        self._properties['gain'] = HikRobotCameraProperty(self._cam, 'gain', "Gain")
        self._properties['exposure'] = HikRobotCameraProperty(self._cam, 'exposure', "ExposureTime")

    def open(self, camera_id: str | int | None = None) -> None:
        if self._cam.MV_CC_OpenDevice(hik.MV_ACCESS_Exclusive, 0) == 0:
            self._is_opened = True
            self._init_properties()

            self._cam.MV_CC_SetEnumValue("TriggerMode", hik.MV_TRIGGER_MODE_OFF)

            int_value = hik.MVCC_INTVALUE()
            memset(byref(int_value), 0, sizeof(hik.MVCC_INTVALUE))
            self._cam.MV_CC_GetIntValue("Width", int_value)
            width = int(int_value.nCurValue)

            self._cam.MV_CC_GetIntValue("Height", int_value)
            height = int(int_value.nCurValue)

            self._resolution = (width, height)

    def close(self) -> None:
        if self._cam.MV_CC_CloseDevice() == 0:
            self._is_opened = False

    def __del__(self) -> None:
        self._cam.MV_CC_DestroyHandle()

    def start(self) -> None:
        ret = self._cam.MV_CC_StartGrabbing()

    def stop(self) -> None:
        self._cam.MV_CC_StopGrabbing()

    def query_frame(self, *args, **kwargs) -> numpy.ndarray or None:
        ret = self._cam.MV_CC_GetImageBuffer(self._st_out_frame, 1000)

        if ret != 0:
            return None

        st_frame_info = self._st_out_frame.stFrameInfo
        h, w = st_frame_info.nHeight, st_frame_info.nWidth

        buf_save_image = (c_ubyte * st_frame_info.nFrameLen)()
        cdll.msvcrt.memcpy(byref(buf_save_image), self._st_out_frame.pBufAddr, st_frame_info.nFrameLen)
        en_pixel_size = st_frame_info.enPixelType
        img: numpy.ndarray | None = None
        if en_pixel_size == PixelType.PixelType_Gvsp_Mono8:
            img = numpy.frombuffer(buf_save_image, count=int(w * h), dtype=numpy.uint8, offset=0)
            img = img.copy().reshape(h, w)
        self._cam.MV_CC_FreeImageBuffer(self._st_out_frame)
        return img

    @property
    def is_opened(self) -> bool:
        return self._is_opened

