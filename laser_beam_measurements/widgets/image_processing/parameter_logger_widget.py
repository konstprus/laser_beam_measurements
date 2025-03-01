# 
# Project: laser_beam_measurements
#
# File: parameter_logger_widget.py
#
# Author: Konstantin Prusakov
#
# Copyright 2025 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

# pyside6-uic laser_beam_measurements/widgets/image_processing/parameter_logger_widget.ui -o laser_beam_measurements/widgets/image_processing/ui_parameter_logger_widget.py


from PySide6.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QListWidgetItem
from PySide6.QtCore import Qt, Slot
from laser_beam_measurements.image_processing.parameter_logger import ParameterLogger
from laser_beam_measurements.image_processing.parameter_logger_widget_base import ParameterLoggingWidgetBase
from .ui_parameter_logger_widget import Ui_Form

class ParameterLoggerWidget(ParameterLoggingWidgetBase):


    def __init__(self, parent=None):
        super(ParameterLoggerWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.start_stop_button.clicked.connect(self._slot_change_logger_state)
        self.ui.time_step.setText("1")


    def _logger_state_changed(self, state: bool) -> None:
        if state:
            self._set_enabled(False)
            self.ui.start_stop_button.setText("Stop")
        else:
            self._set_enabled(True)
            self.ui.start_stop_button.setText("Start")

    def _show_available_parameters(self, parameters_list: list) -> None:
        self.ui.available_parameters.clear()
        for parameter in parameters_list:
            item = QListWidgetItem(str(parameter))
            item.setCheckState(Qt.CheckState.Unchecked)
            self.ui.available_parameters.addItem(item)

    @Slot()
    def _slot_change_logger_state(self) -> None:
        if self.ui.start_stop_button.text() == "Start":
            self._start_logging()
        elif self.ui.start_stop_button.text() == "Stop":
            self._stop_logging()

    def _start_logging(self) -> None:
        selected_parameters = self._collect_selected_parameters()
        self._logger.slot_update_selected_parameters(selected_parameters)
        timer_interval = self._get_timer_interval()
        self._logger.timer_interval = timer_interval
        self.signal_change_state.emit(True)

    def _stop_logging(self) -> None:
        self.signal_change_state.emit(False)

    def _collect_selected_parameters(self) -> list:
        selected_parameters = list()
        for i in range(self.ui.available_parameters.count()):
            item = self.ui.available_parameters.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected_parameters.append(item.text())
        return selected_parameters

    def _get_timer_interval(self) -> int:
        try:
            value = float(self.ui.time_step.text()) * 1000
            unit = self.ui.time_unit.currentText()
            if unit == "min":
                value *= 60
            return int(value)
        except Exception:
            return 1000

    def _set_enabled(self, value: bool) -> None:
        self.ui.available_parameters.setEnabled(value)
        self.ui.time_step.setEnabled(value)
        self.ui.time_unit.setEnabled(value)
