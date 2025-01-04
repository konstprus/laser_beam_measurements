# 
# Project: laser_beam_measurements
#
# File: hikrobot_camera_property.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from laser_beam_measurements.camera_control.camera_property_base import CameraPropertyBase
from .mv_import import MvCameraControl_class as hik
from ctypes import Structure, memset, byref, sizeof


class HikRobotCameraProperty(CameraPropertyBase):

    def __init__(self, handler: hik.MvCamera, name: str, prop_key: str, prop_type: str = 'float'):
        super().__init__(handler, name)
        self._st_param: Structure | None = None
        self._prop_key: str = prop_key
        self._prop_type: str = prop_type
        if prop_type == 'float':
            self._st_param = hik.MVCC_FLOATVALUE()
            memset(byref(self._st_param), 0, sizeof(hik.MVCC_FLOATVALUE))
        elif prop_type == 'int':
            self._st_param = hik.MVCC_INTVALUE()
            memset(byref(self._st_param), 0, sizeof(hik.MVCC_INTVALUE))

    def _read_parameter(self) -> bool:
        if self._prop_type == 'float':
            return self._handler.MV_CC_GetFloatValue(self._prop_key, self._st_param) == 0

        if self._prop_type == 'int':
            return self._handler.MV_CC_GetIntValue(self._prop_key, self._st_param) == 0

    def _write_parameter(self, value) -> bool:
        if self._prop_type == 'float':
            return self._handler.MV_CC_SetFloatValue(self._prop_key, float(value)) == 0

        if self._prop_type == 'int':
            return self._handler.MV_CC_SetIntValue(self._prop_key, float(value)) == 0

    def _get_values(self) -> tuple:
        if self._prop_type == 'float':
            return (float(self._st_param.fCurValue),
                    float(self._st_param.fMin),
                    float(self._st_param.fMax),
                    0.00001)

        if self._prop_type == 'int':
            return (int(self._st_param.nCurValue),
                    int(self._st_param.nMin),
                    int(self._st_param.nMax),
                    int(self._st_param.nInc))

    @property
    def min(self):
        if self._read_parameter():
            return self._get_values()[1]
        return None

    @property
    def max(self):
        if self._read_parameter():
            if self.name == 'exposure':
                return 1.0
            return self._get_values()[2]
        return None

    @property
    def step(self):
        if self._read_parameter():
            return self._get_values()[3]
        return None

    @property
    def value(self):
        if self._read_parameter():
            return self._get_values()[0]
        return None

    @value.setter
    def value(self, value):
        self._write_parameter(value)
