# 
# Project: laser_beam_measurements
#
# File: parameter_logger_widget_base.py
#
# Author: Konstantin Prusakov
#
# Copyright 2025 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import Signal, Slot
from PySide6.QtWidgets import QWidget
from pyqtgraph import disconnect

from .parameter_logger import ParameterLogger
from typing import Optional


class ParameterLoggingWidgetBase(QWidget):

    signal_change_state = Signal(bool)
    signal_set_parameter_to_show = Signal(str)

    def __init__(self, parent=None):
        super(ParameterLoggingWidgetBase, self).__init__(parent)
        self._logger: Optional[ParameterLogger] = None


    def set_logger(self, logger: ParameterLogger) -> None:
        if self._logger:
            self.signal_change_state.disconnect(self._logger.slot_change_state)
            self.signal_set_parameter_to_show.disconnect(self._logger.slot_set_parameter_to_show)
            self._logger.signal_state_changed.disconnect(self.slot_logger_state_changed)
            self._logger.signal_available_parameters_updated.disconnect(self.slot_show_available_parameters)
            self._logger.signal_show_selected_parameter.disconnect(self.slot_show_selected_parameter)
            self._logger.signal_timeout.disconnect(self.slot_show_current_interval)

        self._logger = logger
        self.signal_change_state.connect(self._logger.slot_change_state)
        self.signal_set_parameter_to_show.connect(self._logger.slot_set_parameter_to_show)
        self._logger.signal_state_changed.connect(self.slot_logger_state_changed)
        self._logger.signal_available_parameters_updated.connect(self.slot_show_available_parameters)
        self._logger.signal_show_selected_parameter.connect(self.slot_show_selected_parameter)
        self._logger.signal_timeout.connect(self.slot_show_current_interval)
        self._show_available_parameters(self._logger.available_parameters)

    @Slot(bool)
    def slot_logger_state_changed(self, state: bool) -> None:
        self._logger_state_changed(state)

    def _logger_state_changed(self, state: bool) -> None:
        raise NotImplementedError()

    @Slot(list)
    def slot_show_available_parameters(self, parameters_list: list) -> None:
        self._show_available_parameters(parameters_list)

    def _show_available_parameters(self, parameters_list: list) -> None:
        raise NotImplementedError()

    @Slot(str, list, dict)
    def slot_show_selected_parameter(self, group_name: str, logging_time: list, parameters: dict[str, list]) -> None:
        self._slot_show_selected_parameter(group_name, logging_time, parameters)

    def _slot_show_selected_parameter(self, group_name: str, logging_time: list, parameters: dict[str, list]) -> None:
        raise NotImplementedError

    @Slot(int, float)
    def slot_show_current_interval(self, counter: int, interval: float) -> None:
        self._show_current_interval(counter, interval)

    def _show_current_interval(self, counter: int, interval: float) -> None:
        raise NotImplementedError()