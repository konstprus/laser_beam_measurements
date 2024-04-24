# 
# Project: laser_beam_measurements
#
# File: camera_property_base.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

import typing

__all__ = ["CameraPropertyBase"]


class CameraPropertyBase(object):

    def __init__(self, handler: typing.Any, name: str):
        self._handler = handler
        self._name = name

    @property
    def available(self) -> bool:
        return False

    @property
    def name(self) -> str:
        return self._name

    @property
    def min(self) -> int | float:
        raise NotImplementedError()

    @property
    def max(self) -> int | float:
        raise NotImplementedError()

    @property
    def range(self) -> tuple[int | float, int | float]:
        return self.min, self.max

    @property
    def step(self) -> int | float:
        raise NotImplementedError()

    @property
    def value(self) -> int | float:
        raise NotImplementedError()

    @value.setter
    def value(self, value: int | float):
        raise NotImplementedError()
