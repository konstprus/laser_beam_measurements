#
# Project: laser_beam_measurements
#
# File: opencv_camera.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from laser_beam_measurements.camera_control.camera_base import CameraBase
# from camera_control.property_base import PropertyBase
from .opencv_camera_property import OpenCVCameraProperty

import cv2

__all__ = ['OpenCVCamera', ]


class OpenCVCamera(CameraBase):

    type = "OpenCV"

    def __init__(self, **kwargs):
        camera_id = kwargs.get("camera_id", 0)
        kwargs.update({"camera_id": camera_id})
        super(OpenCVCamera, self).__init__(**kwargs)
        self._cap: [cv2.VideoCapture, None] = None

    def _initialize(self) -> None:
        self._properties.clear()

    def _init_properties(self) -> None:
        self._properties.clear()
        self._properties['fps'] = OpenCVCameraProperty(self._cap, 'fps', cv2.CAP_PROP_FPS, min=1, max=30, step=1)
        self._properties['gain'] = OpenCVCameraProperty(self._cap, 'gain', cv2.CAP_PROP_GAIN, min=1, max=250, step=1)
        self._properties['exposure'] = OpenCVCameraProperty(
            self._cap, 'exposure', cv2.CAP_PROP_EXPOSURE, min=-14, max=0, step=1)

    def open(self, camera_id: str | int | None = None) -> None:
        if self.is_opened:
            self.close()
        if isinstance(camera_id, int) or isinstance(camera_id, float):
            self._id = int(camera_id)
        else:
            if self._id is None:
                self._id = 0
        if self._cap is None:
            self._cap = cv2.VideoCapture(int(self._id), cv2.CAP_DSHOW)
        elif isinstance(self._cap, cv2.VideoCapture) and not self._cap.isOpened():
            self._cap.open(int(self._id))
        if self._cap.isOpened():
            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 10000)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 10000)
            w = self._cap.get(cv2.CAP_PROP_FRAME_WIDTH)
            h = self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
            self._resolution = [w, h]
            self._init_properties()

    def close(self):
        if isinstance(self._cap, cv2.VideoCapture) and self._cap.isOpened():
            self._cap.release()

    @property
    def is_opened(self) -> bool:
        if isinstance(self._cap, cv2.VideoCapture):
            return self._cap.isOpened()
        return False

    def query_frame(self, *args, **kwargs):
        if self.is_opened:
            res, im = self._cap.read()
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            return im
        return None
