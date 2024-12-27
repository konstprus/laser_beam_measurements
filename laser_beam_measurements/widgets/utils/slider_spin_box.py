#
# Project: laser_beam_measurements
#
# File: slider_spin_box.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtWidgets import QWidget, QHBoxLayout, QDoubleSpinBox, QLabel
from PySide6.QtCore import Signal, Slot, Qt
import sys

from .float_slider import FloatSlider

__all__ = ["SliderSpinBox"]


class SliderSpinBox(QWidget):

    value_changed = Signal(float)

    def __init__(self, parent=None, *args, **kwargs):
        super(SliderSpinBox, self).__init__(parent=parent, *args, **kwargs)

        self._outerLayout = QHBoxLayout(self)
        self._outerLayout.setSpacing(0)
        self._outerLayout.setContentsMargins(0, 0, 0, 0)

        self._slider = FloatSlider(self)
        self._slider.setOrientation(Qt.Orientation.Horizontal)
        self._spinBox = QDoubleSpinBox(self)
        self._labelMinValue = QLabel(self)
        self._labelMaxValue = QLabel(self)
        self._labelTitle = QLabel(self)

        self._outerLayout.addWidget(self._labelMinValue)
        self._outerLayout.addWidget(self._slider)
        self._outerLayout.addWidget(self._labelMaxValue)
        self._outerLayout.addWidget(self._spinBox)
        self._outerLayout.addWidget(self._labelTitle)

        self.setMinimum(self._slider.minimum())
        self.setMaximum(self._slider.maximum())
        self._spinBox.setSingleStep(self._slider.get_range()/100.0)
        self._connect()

    def _connect(self) -> None:
        self._slider.signal_value_changed.connect(self._on_slider_value_changed)
        self._spinBox.valueChanged.connect(self._on_spin_box_value_changed)
        self._spinBox.valueChanged.connect(self.value_changed)

    def _update_single_step(self):
        self._spinBox.setSingleStep(self._slider.get_range() / 100.0)

    @Slot(float)
    def _on_slider_value_changed(self, value: float) -> None:
        if abs(self._spinBox.value() - value) > sys.float_info.epsilon:
            self._spinBox.setValue(value)

    @Slot(float)
    def _on_spin_box_value_changed(self, value: float) -> None:
        if abs(self._slider.value() - value) > sys.float_info.epsilon:
            self._slider.setValue(value)

    def setValue(self, value: float) -> None:
        self._on_spin_box_value_changed(value)

    def setMinimum(self, value) -> None:
        self._slider.setMinimum(value)
        self._spinBox.setMinimum(value)
        self._labelMinValue.setText(str(value))
        self._spinBox.setSingleStep(self._slider.get_range()/10.0)
        self._update_single_step()

    def setMaximum(self, value):
        self._slider.setMaximum(value)
        self._spinBox.setMaximum(value)
        self._labelMaxValue.setText(str(value))
        self._spinBox.setSingleStep(self._slider.get_range()/10.0)
        self._update_single_step()

    def setRange(self, values: tuple) -> None:
        self.setMinimum(values[0])
        self.setMaximum(values[1])

    def setTitle(self, value: str) -> None:
        self._labelTitle.setText(value)

    def setSliderFactor(self, value: float) -> None:
        self._slider.set_factor(value)

    def title(self) -> str:
        return self._labelTitle.text()