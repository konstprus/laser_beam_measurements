#
# Project: laser_beam_measurements
#
# File: camera_listener_base.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

import numpy
from enum import Enum

__all__ = ["CameraListenerBase", "CameraState"]


class CameraState(Enum):
    CLOSED = -1
    STOPPED = 0
    STARTED = 1


class CameraListenerBase(object):

    def on_new_image(self, img: numpy.ndarray) -> None:
        pass

    def on_camera_state_changed(self, flag_state: CameraState) -> None:
        pass

    def on_error(self, error_message: str) -> None:
        pass

    def reset(self) -> None:
        pass
