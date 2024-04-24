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

__all__ = ["CameraListenerBase"]


class CameraListenerBase(object):

    def on_new_image(self, img: numpy.ndarray) -> None:
        pass

    def on_camera_state_changed(self, flag_state: bool) -> None:
        pass

    def on_error(self, error_message: str) -> None:
        pass

    def reset(self) -> None:
        pass
