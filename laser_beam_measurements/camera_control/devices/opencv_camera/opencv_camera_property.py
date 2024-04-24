#
# Project: laser_beam_measurements
#
# File: opencv_camera_property.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from laser_beam_measurements.camera_control.camera_property_base import CameraPropertyBase
import cv2

__all__ = ["OpenCVCameraProperty"]


class OpenCVCameraProperty(CameraPropertyBase):

    def __init__(self, handler: cv2.VideoCapture, name: str, prop_id: id, **kwargs):
        super(OpenCVCameraProperty, self).__init__(handler, name)
        self._prop_id = prop_id
        self._min: float = kwargs.get("min", -1.0)
        self._max: float = kwargs.get("max", 1.0)
        self._step: float = kwargs.get("step", 1.0)
        self._available = True

    @property
    def available(self) -> bool:
        return self._available

    @property
    def min(self):
        return self._min

    @property
    def max(self):
        return self._max

    @property
    def step(self):
        return self._step

    @property
    def value(self):
        return self._handler.get(self._prop_id)

    @value.setter
    def value(self, value):
        self._handler.set(self._prop_id, value)
