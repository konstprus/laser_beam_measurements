#
# Project: laser_beam_measurements
#
# File: float_slider.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtWidgets import QSlider
from PySide6.QtCore import Signal, Slot


__all__ = ["FloatSlider"]


class FloatSlider(QSlider):

    signal_value_changed = Signal(float)

    def __init__(self, *args, **kwargs):
        super(FloatSlider, self).__init__(*args, **kwargs)
        self._max_int_value = 10 ** 4
        super(FloatSlider, self).setMinimum(0)
        super(FloatSlider, self).setMaximum(self._max_int_value)
        self._max_value = 1.0
        self._min_value = 0.0
        self.valueChanged.connect(self._emit_value_changed)

    @Slot()
    def _emit_value_changed(self):
        self.signal_value_changed.emit(self.value())

    @property
    def _range(self):
        return self._max_value - self._min_value

    def value(self):
        return float(super(FloatSlider, self).value()) / self._max_int_value * self._range + self._min_value

    def setValue(self, value):
        if self._range > 0:
            float_value = (value - self._min_value) / self._range * self._max_int_value
            super(FloatSlider, self).setValue(int(float_value))

    def setMinimum(self, value):
        self._min_value = value
        self.setValue(self.value())

    def setMaximum(self, value):
        self._max_value = value
        self.setValue(self.value())

    def minimum(self):
        return self._min_value

    def maximum(self):
        return self._max_value

    def set_factor(self, value):
        self._max_int_value = value
        super(FloatSlider, self).setMaximum(self._max_int_value)
        self.setValue(self.value())

    def get_range(self):
        return self._range
