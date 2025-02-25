# 
# Project: laser_beam_measurements
#
# File: parameter_logger.py
#
# Author: Konstantin Prusakov
#
# Copyright 2025 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import QObject, QThread, QCoreApplication, Signal, Slot, QMutex
from typing import Dict, Tuple, Union, Optional
from time import time
from datetime import datetime
from dataclasses import dataclass

__all__ = ["ParameterLogger"]

@dataclass
class LoggingData:

    time: list[float]
    data: Dict[str, list[Union[int, float]]]
    counter: int

    def __init__(self):
        self.time = []
        self.data = {}
        self.counter = 0

    def clear(self):
        self.time.clear()
        self.data.clear()
        self.counter = 0

    def prepare(self, parameter_list: list[str]):
        [self.data.update({parameter: list()}) for parameter in parameter_list]


class ParameterLogger(QObject):

    signal_state_changed = Signal(bool)
    signal_selected_parameter_updated = Signal(list, list)
    signal_selected_parameters_updated = Signal(list)
    signal_available_parameters_updated = Signal(list)
    signal_timeout = Signal(int, int)

    MIN_TIMER_INTERVAL = 10

    def __init__(self, parent=None):
        super(ParameterLogger, self).__init__(parent)
        self._mutex = QMutex()
        self._available_parameters: list = list()
        self._selected_parameters: list = list()
        self._current_data: Dict[str, Union[int, float]] = dict() # Dict[str, Dict[str, Union[Tuple[float, float], float]]] = dict()
        self._logging_data: LoggingData = LoggingData()
        self._timer_interval: int = 100
        self._timer_id: int = -1
        self._filename: Optional[str] = ""
        self._selected_parameter: Optional[str] = ""
        self._start_time: float = 0.0
        self._flag_show_parameters: bool = True
        self._flag_available: bool = False

    @property
    def available(self) -> bool:
        return len(self._available_parameters) > 0

    @Slot(list)
    def slot_update_available_parameters(self, parameters_list: list[str]) -> None:
        if self.is_active:
            return
        self._available_parameters.clear()
        self._available_parameters = parameters_list
        self.signal_available_parameters_updated.emit(self._available_parameters)

    @Slot(str)
    def slot_add_available_parameter(self, parameter: str) -> None:
        if self.is_active:
            return
        self._available_parameters.append(parameter)
        self.signal_available_parameters_updated.emit(self._available_parameters)

    @Slot(list)
    def slot_update_selected_parameters(self, parameters_list: list[str]) -> None:
        if self.is_active:
            return
        self._selected_parameters.clear()
        self._selected_parameters = parameters_list
        self.signal_selected_parameters_updated.emit(self._selected_parameters)

    @Slot(str)
    def slot_add_selected_parameter(self, parameter: str) -> None:
        if self.is_active:
            return
        self._selected_parameters.append(parameter)
        self.signal_selected_parameters_updated.emit(self._selected_parameters)

    @property
    def is_active(self) -> bool:
        return self._timer_id != -1

    @property
    def timer_interval(self) -> int:
        return self._timer_interval

    @timer_interval.setter
    def timer_interval(self, value: int) -> None:
        if self.is_active:
            return
        if value > self.MIN_TIMER_INTERVAL:
            self._timer_interval = value

    @Slot(bool)
    def slot_change_state(self, state: bool) -> None:
        if state:
            if not self.is_active:
                self.start()
        else:
            self.stop()

    def set_all_parameters(self, parameters_list: list, timer_interval: int) -> None:
        if self.is_active:
            return
        self.slot_update_selected_parameters(parameters_list)
        self.timer_interval = timer_interval

    def start(self, interval: Optional[int] = None) -> None:
        if len(self._selected_parameters) == 0:
            return
        if interval:
            self._timer_interval = interval
        if self._timer_id != -1:
            self.stop()
        self._start_time = time()
        self._prepare_data_for_logging()
        self._prepare_file()
        self._timer_id = self.startTimer(self._timer_interval)
        self.signal_state_changed.emit(True)


    def stop(self) -> None:
        if self._timer_id > 0:
            self.killTimer(self._timer_id)
            self._timer_id = -1
            self.signal_state_changed.emit(False)

    def timerEvent(self, *args, **kwargs) -> None:
        QCoreApplication.sendPostedEvents(self, 0)
        self._save_data()
        if self._flag_show_parameters:
            self._show_parameters()
        super().timerEvent(*args, **kwargs)

    def _save_data(self) -> None:
        data = self._current_data.copy()
        keys = data.keys()
        current_time = time()
        elapsed_time = current_time - self._start_time
        self._logging_data.time.append(elapsed_time)
        data_to_write: list[Union[float, int]] = [self._logging_data.time[-1]]
        for param in self._selected_parameters:
            if param in keys:
                data_to_write.append(data[param])
                self._logging_data.data[param].append(data[param])
            else:
                self.stop()
                return
        if self._filename is None:
            return
        with open(self._filename, 'a') as file:
            str_to_write = "\t".join([str(data) for data in data_to_write])
            file.write(f"{str_to_write}\n")
        self._logging_data.counter += 1

    def _prepare_data_for_logging(self) -> None:
        self._logging_data.clear()
        self._logging_data.prepare(self._selected_parameters)

    # def select_parameters(self, parameter_list: list) -> None:
    #     self._selected_parameters.clear()
    #     self._selected_parameters = parameter_list

    @Slot(str)
    def set_filename(self, filename: str) -> None:
        self._filename = filename
        self._validate_filename()

    def _validate_filename(self) -> None:
        if self._filename is None:
            self._filename = datetime.now().strftime('%Y_%m_%d__%H%M') + ".txt"
        #TODO: check existence of the file

    def _prepare_file(self):
        self._validate_filename()
        with open(self._filename, 'a') as file:
            str_to_write: str = "Elapsed Time\t" + "\t".join(self._selected_parameters)
            file.write(f"{str_to_write}\n")

    def _show_parameters(self):
        if self._selected_parameter in self._selected_parameters:
            self.signal_selected_parameter_updated.emit(self._logging_data.time, self._logging_data.data[self._selected_parameter])