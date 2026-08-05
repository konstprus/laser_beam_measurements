# 
# Project: laser_beam_measurements
#
# File: hikrobot_camera_factory.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#
from typing import Optional, Union, Any

from laser_beam_measurements.camera_control.camera_factory_base import CameraFactoryBase, CameraCreateException

from .hikrobot_camera import HikRobotCamera

from .mv_import import MvCameraControl_class as hik
from .mv_import import PixelType_header as PixelType
from ctypes import *

from laser_beam_measurements.camera_control.pixel_format import PixelFormat, PixelFormatEnum, get_pixel_format


class HikRobotCameraFactory(CameraFactoryBase):
    camera_class = HikRobotCamera

    def __init__(self):
        super(HikRobotCameraFactory, self).__init__()
        self._name_info_mapping: dict[str, hik.MV_CC_DEVICE_INFO] = {}
        self._pixel_format_mapping: dict[Any, Optional[PixelFormat]] = {
            PixelType.PixelType_Gvsp_Mono12: get_pixel_format(PixelFormatEnum.MONO_12),
            PixelType.PixelType_Gvsp_Mono8: get_pixel_format(PixelFormatEnum.MONO_8),
            PixelType.PixelType_Gvsp_Mono10: get_pixel_format(PixelFormatEnum.MONO_10),
        }
        # hik.MvCamera.MV_CC_Initialize()

    def _get_available_devices(self) -> list:
        self._name_info_mapping.clear()
        device_list = hik.MV_CC_DEVICE_INFO_LIST()
        t_layer_type = (hik.MV_GIGE_DEVICE |
                        hik.MV_USB_DEVICE |
                        hik.MV_GENTL_CAMERALINK_DEVICE |
                        hik.MV_GENTL_CXP_DEVICE |
                        hik.MV_GENTL_XOF_DEVICE)
        if hik.MvCamera.MV_CC_EnumDevices(t_layer_type, device_list) != 0:
            return []

        for i in range(0, device_list.nDeviceNum):
            mvcc_dev_info = cast(device_list.pDeviceInfo[i], POINTER(hik.MV_CC_DEVICE_INFO)).contents

            if mvcc_dev_info.nTLayerType == hik.MV_GIGE_DEVICE or mvcc_dev_info.nTLayerType == hik.MV_GENTL_GIGE_DEVICE:
                str_model_name = ""
                for per in mvcc_dev_info.SpecialInfo.stGigEInfo.chModelName:
                    if per == 0:
                        break
                    str_model_name = str_model_name + chr(per)

                nip1 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0xff000000) >> 24)
                nip2 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x00ff0000) >> 16)
                nip3 = ((mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x0000ff00) >> 8)
                nip4 = (mvcc_dev_info.SpecialInfo.stGigEInfo.nCurrentIp & 0x000000ff)

                model_id = f"{str_model_name}. ip:{nip1}.{nip2}.{nip3}.{nip4}"
                self._name_info_mapping.update({model_id: mvcc_dev_info})

            elif mvcc_dev_info.nTLayerType == hik.MV_USB_DEVICE:
                str_model_name = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chModelName:
                    if per == 0:
                        break
                    str_model_name = str_model_name + chr(per)

                str_serial_number = ""
                for per in mvcc_dev_info.SpecialInfo.stUsb3VInfo.chSerialNumber:
                    if per == 0:
                        break
                    str_serial_number = str_serial_number + chr(per)

                model_id = f"{str_model_name}. SN: {str_serial_number}"
                self._name_info_mapping.update({model_id: mvcc_dev_info})

            # TODO
            # elif mvcc_dev_info.nTLayerType == hik.MV_GENTL_CAMERALINK_DEVICE:
            #     pass
            #
            # elif mvcc_dev_info.nTLayerType == hik.MV_GENTL_CXP_DEVICE:
            #     pass
            #
            # elif mvcc_dev_info.nTLayerType == hik.MV_GENTL_XOF_DEVICE:
            #     pass
        return list(self._name_info_mapping.keys())

    def get_available_pixel_formats(self, camera_id: Optional[str | int], *args, **kwargs) -> list[PixelFormat]:
        if camera_id in self._name_info_mapping.keys():
            cam = hik.MvCamera()
            device_info = self._name_info_mapping.get(camera_id)
            if cam.MV_CC_CreateHandle(device_info) != 0:
                cam.MV_CC_DestroyHandle()
                return []
            if cam.MV_CC_OpenDevice(hik.MV_ACCESS_Exclusive, 0) != 0:
                cam.MV_CC_DestroyHandle()
                return []
            enum_value = hik.MVCC_ENUMVALUE()
            memset(byref(enum_value), 0, sizeof(hik.MVCC_ENUMVALUE))
            ret = cam.MV_CC_GetEnumValue("PixelFormat", enum_value)
            if ret != 0:
                return []
            pf_list = []
            for i in range(enum_value.nSupportedNum):
                pf_code = enum_value.nSupportValue[i]
                if pf_code in self._pixel_format_mapping.keys():
                    pf_list.append(self._pixel_format_mapping[pf_code])
            cam.MV_CC_CloseDevice()
            cam.MV_CC_DestroyHandle()
            return pf_list
        return []

    def create(self, camera_id=None, *args, **kwargs):
        if camera_id in self._name_info_mapping.keys():
            device_info = self._name_info_mapping.get(camera_id)
            cam = hik.MvCamera()
            if cam.MV_CC_CreateHandle(device_info) != 0:
                raise CameraCreateException("Error occurred during creation HikRobotCamera")

            kwargs.update({"mv_cam": cam, "device_info": device_info})
            pixel_format: str = kwargs.get("pixel_format", None)
            if pixel_format is not None:
                for key, value in self._pixel_format_mapping.items():
                    if value.name == pixel_format:
                        kwargs.update({"pixel_type": key})
                        break

            return super(HikRobotCameraFactory, self).create(camera_id=camera_id, *args, **kwargs)
        raise CameraCreateException("camera_id is unknown")