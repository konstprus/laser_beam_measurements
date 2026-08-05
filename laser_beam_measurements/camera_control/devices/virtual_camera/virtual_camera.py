#
# Project: laser_beam_measurements
#
# File: virtual_camera.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

import numpy
from numpy.random import random, randint
from time import time, sleep
from typing import Optional, Union

from laser_beam_measurements.camera_control.camera_base import CameraBase
from laser_beam_measurements.camera_control.camera_property_base import CameraPropertyBase
from laser_beam_measurements.camera_control.pixel_format import PixelFormatEnum, PixelFormat, get_pixel_format
from .helper_functions import generate_gauss, generate_line

__all__ = ['VirtualCamera', 'VirtualProperty']


class VirtualCamera(CameraBase):
    type = 'Virtual'

    def __init__(self, **kwargs):
        # kwargs.update({'resolution': [1920, 1080]})
        # kwargs.update({'resolution': [4000, 3000]})
        kwargs.update({'resolution': [1366, 768]})
        super(VirtualCamera, self).__init__(**kwargs)
        self.fps = kwargs.get('fps', 30)
        self.x0 = randint(self._resolution[0] / 4, self._resolution[0] / 2)
        self.y0 = randint(self._resolution[1] / 4, self._resolution[1] / 2)
        self.t_ms = 100.0
        self.flag_opened = False
        self.prev_frame_time = 0.0

        # pixel_format: str = kwargs.get('pixel_format', PixelFormatEnum.MONO_12)
        # self._pixel_format: PixelFormat = get_pixel_format(pixel_format)
        # if self._pixel_format is None:
        #     self._pixel_format = get_pixel_format(PixelFormatEnum.MONO_12)

        self.exp_range = (1, self.pixel_format.max_pixel_value)
        self._max_fps_t = 60.0
        self.fps_range = (1.0, round(1.0/self._max_fps_t, 2))
        self.gain_range = (0.0, 4.0)
        self._properties = {
            'fps': VirtualProperty(self, 'fps', self.fps_range),
            'exposure': VirtualProperty(self, 'exposure', self.exp_range)
        }

        self._initialize1()

    def _initialize1(self) -> None:
        self._max_fps_t = 60.0
        for _ in range(5):
            t0 = time()
            _ = self._get_stimulated_image(self.x0, self.y0, False)
            t1 = time()
            if self._max_fps_t > t1 - t0:
                self._max_fps_t = t1 - t0

    def _get_stimulated_image(self, x0, y0, is_sleep=True, static=False) -> numpy.ndarray:
        t0 = time()
        if is_sleep:
            if 1.0/self.fps > (t0 - self.prev_frame_time):
                sleep(1.0/self.fps - t0 + self.prev_frame_time)
        x = numpy.arange(0, self._resolution[0])
        y = numpy.arange(0, self._resolution[1])
        max_pixel_value =  self._pixel_format.max_pixel_value
        sigma = min(self._resolution[0], self._resolution[1])/5
        power = max_pixel_value * 4
        xx, yy = numpy.meshgrid(x, y)
        if self._id == "zero":
            img = (self.t_ms * 0.01 * random([self._resolution[1],
                                              self._resolution[0]]))
        elif self._id == "line":
            img = generate_line(xx, yy, x0, y0, sigma, power)
        else:
            img = generate_gauss(yy, xx, y0, x0, sigma, power)
        if self._id == "perpendicular":
            img += generate_gauss(yy, xx, y0 + sigma/1.5, x0, sigma, power)
        elif self._id == "left":
            img += generate_gauss(yy, xx, y0 + sigma/1.5, x0 + sigma/2, sigma, power)
        elif self._id == "right":
            img += generate_gauss(yy, xx, y0 + sigma/1.5, x0 - sigma/2, sigma, power)
        # img = numpy.array((self.t_ms + 100.0) * img / numpy.max(img))
        img = numpy.array((self.t_ms + max_pixel_value*0.4) * img / numpy.max(img))
        if not static:
            img += (self.t_ms*0.01*random([self._resolution[1],
                                           self._resolution[0]]))
        numpy.putmask(
            img,
            img > max_pixel_value,
            max_pixel_value
        )
        dtype = numpy.uint8
        if max_pixel_value > 255:
            dtype = numpy.uint16
        img = numpy.array(img, dtype=dtype)
        self.prev_frame_time = time()
        return img

    def open(self, camera_id: Optional[Union[str , int]] = None) -> None:
        if camera_id is not None:
            self._id = camera_id
        self.flag_opened = True

    def close(self):
        self.flag_opened = False

    def is_opened(self):
        return self.flag_opened

    def start(self):
        self.prev_frame_time = time()

    def query_frame(self, *args, **kwargs):
        img = self._get_stimulated_image(self.x0, self.y0, False)
        return img


class VirtualProperty(CameraPropertyBase):

    def __init__(self, handle: VirtualCamera, name: str, value_range: tuple):
        assert(isinstance(handle, VirtualCamera))
        super(VirtualProperty, self).__init__(handle, name)
        self._range = value_range

    @property
    def available(self):
        if self._name == 'gain':
            return False
        return True

    @property
    def max(self):
        return self._range[1]

    @property
    def min(self):
        return self._range[0]

    @property
    def range(self):
        return self._range

    @property
    def step(self):
        return 0.1

    @property
    def value(self):
        if self._name == 'exposure':
            return self._handler.t_ms
        return getattr(self._handler, self._name)

    @value.setter
    def value(self, value):
        if value < self.min:
            value = self.min
        elif value > self.max:
            value = self.max
        if self._name == 'exposure':
            self._handler.t_ms = value
        else:
            setattr(self._handler, self._name, value)
