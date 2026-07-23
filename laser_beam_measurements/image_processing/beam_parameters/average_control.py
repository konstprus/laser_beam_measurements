# 
# Project: laser_beam_measurements
#
# File: average_control.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtCore import QReadWriteLock, QReadLocker, QWriteLocker


class AverageControl:

    def __init__(self):
        self._lock = QReadWriteLock()
        self._enabled: bool = False
        self._number: int = 1
        self._counter: int = 0

    @property
    def counter(self) -> int:
        return self._counter

    def reset_counter(self) -> None:
        self._counter = 0

    def should_reset(self) -> bool:
        with QReadLocker(self._lock):
            return self._counter > self._number

    def increase_counter(self) -> None:
        with QWriteLocker(self._lock):
            self._counter += 1

    @property
    def ready(self) -> bool:
        with QReadLocker(self._lock):
            return self._counter >= self._number

    @property
    def number(self) -> int:
        with QReadLocker(self._lock):
            return self._number

    @number.setter
    def number(self, number: int) -> None:
        with QWriteLocker(self._lock):
            self._number = number

    @property
    def enabled(self) -> bool:
        with QReadLocker(self._lock):
            return self._enabled

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        with QWriteLocker(self._lock):
            self._enabled = enabled