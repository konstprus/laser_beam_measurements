# 
# Project: laser_beam_measurements
#
# File: camera_listener.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


import numpy
from PySide6.QtCore import QObject, Signal, QElapsedTimer
from PySide6.QtGui import QImage
from .camera_listener_base import CameraListenerBase

__all__ = ["CameraListener"]


class CameraListener(QObject, CameraListenerBase):

    signal_new_image_received = Signal(numpy.ndarray)
    signal_camera_state_changed = Signal(bool)
    signal_error_received = Signal(str)
    signal_statistic_collected = Signal(int, int, float)

    def __init__(self, parent=None, *args, **kwargs):
        super(CameraListener, self).__init__(parent, *args, **kwargs)
        self._frame_counter: int = 0
        self._error_counter: int = 0
        self._actual_fps: float = -1.0
        self._error_message: str = ""
        self._elapsed_timer: QElapsedTimer = QElapsedTimer()
        self._t0: float = 0.0
        self._t1: float = 0.0

    def reset(self):
        self._frame_counter = 0
        self._error_counter = 0
        self._error_message = 0
        self._actual_fps = -1.0
        self._error_message = ""

    def on_new_image(self, img: numpy.ndarray) -> None:
        self._frame_counter += 1
        self.signal_new_image_received.emit(img)
        self._t1 = self._elapsed_timer.nsecsElapsed()
        if self._actual_fps < 0.0:
            self._actual_fps = 0.0
        else:
            self._actual_fps = round(1e9 / (self._t1 - self._t0), 2)
        self._t0 = self._t1
        self.signal_statistic_collected.emit(self._frame_counter, self._error_counter, self._actual_fps)

    def on_camera_state_changed(self, flag_state: bool) -> None:
        self.signal_camera_state_changed.emit(flag_state)

    def on_error(self, error_message: str) -> None:
        self._error_counter += 1
        self._error_message = error_message
        self.signal_error_received.emit(error_message)

    def get_statistics(self) -> tuple:
        return self._frame_counter, self._error_counter, self._actual_fps

    def get_error_message(self) -> str:
        return self._error_message
