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
from typing import Dict, Tuple, Union, Optional, Iterable, Sized, List
from time import time
from datetime import datetime


__all__ = ["ParameterLogger"]


class ParameterLoggingStorage:

    def __init__(self, parameter_name: str, dim: int = 1):
        self._name: str = parameter_name
        self._dimension: int = dim
        self._storage: dict[str, list] = dict()
        self._loggable_name: tuple = tuple()

    @property
    def name(self) -> str:
        return self._name

    @property
    def loggable_names(self) -> tuple:
        return self._loggable_name

    @property
    def storage(self) -> dict:
        return self._storage

    def generate_loggable_names(self) -> None:
        if self._dimension == 1:
            self._loggable_name = (self._name, )
        elif self._dimension == 2:
            self._loggable_name = (f"{self._name}_X", f"{self._name}_Y")
        elif self._dimension > 2:
            names_list = list()
            for i in range(self._dimension):
                names_list.append(f"{self._name}_{i}")
            self._loggable_name = tuple(names_list)
        self._storage = {n: list() for n in self._loggable_name}

    def add_value(self, data: dict) -> Optional[tuple]:
        if self._name in data.keys():
            param_value = data[self._name]
            if isinstance(param_value, (tuple, list)):
                if len(self._loggable_name) != len(param_value):
                    return None
                [self._storage[self._loggable_name[i]].append(param_value[i]) for i in range(len(param_value))]
                return tuple(param_value)
            else:
                if len(self._loggable_name) != 1:
                    return None
                self._storage[self._loggable_name[0]].append(param_value)
                return (param_value, )
        else:
            return None


class LoggingStorage:

    def __init__(self):
        self._time: list[float] = list()
        self._data: list[ParameterLoggingStorage] = list()
        self._counter: int = 0
        self._data_to_write = list()
        self._selected_storage: Optional[ParameterLoggingStorage] = None

    def clear(self) -> None:
        self._time.clear()
        self._data.clear()
        self._counter = 0
        self._data_to_write.clear()

    @property
    def data_to_write(self) -> list:
        return self._data_to_write

    @property
    def parameter_names(self) -> list:
        result = list()
        for parameter in self._data:
            result += list(parameter.loggable_names)
        return result

    @property
    def logging_time(self) -> list:
        return self._time

    @property
    def selected_storage(self) -> Optional[ParameterLoggingStorage]:
        return self._selected_storage

    def prepare(self, selected_parameters: list, data: dict) -> None:
        for param in selected_parameters:
            if param in data.keys():
                value = data[param]
                if isinstance(value, (tuple, list)):
                    self._data.append(ParameterLoggingStorage(param, len(value)))
                else:
                    self._data.append(ParameterLoggingStorage(param))
        [storage.generate_loggable_names() for storage in self._data]

    def add_values(self, t: float, data: dict) -> bool:
        self._data_to_write.clear()
        self._time.append(t)
        self._data_to_write.append(t)
        for storage in self._data:
            added = storage.add_value(data)
            if added is None:
                return False
            # if storage.add_value(data) is None:
            #     return False
            self._data_to_write = [*self._data_to_write, *added]
        self._counter += 1
        return True

    def select_storage(self, name: str) -> None:
        for storage in self._data:
            if storage.name == name:
                self._selected_storage = storage
                return


def adapt_data(data: Dict[str, Dict[str, Union[Tuple[float, float], float]]]) -> Dict[str, Union[int, float]]:
    if len(data) == 0:
        return dict()
    result = dict()
    for key, value in data.items():
        if isinstance(value, dict):
            for key2, value2 in value.items():
                result.update({f"{key}: {key2}": value2})
        elif isinstance(value, Union[int, float]):
            result.update({key: value})
    return result


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
        self._current_data: Dict[str, Dict[str, Union[Tuple[float, float], float]]] = dict()
        self._logging_data: LoggingStorage = LoggingStorage()
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

    @property
    def available_parameters(self) -> list:
        return self._available_parameters

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

    @Slot(dict)
    def slot_set_data(self, data: dict) -> None:
        self._current_data = data

    def _save_data(self) -> None:
        data = self._current_data.copy()
        data = adapt_data(data)
        # keys = data.keys()
        current_time = time()
        elapsed_time = current_time - self._start_time
        result = self._logging_data.add_values(elapsed_time, data)
        if not result:
            self.stop()
            return
        data_to_write = self._logging_data.data_to_write
        if self._filename is None:
            return
        with open(self._filename, 'a') as file:
            str_to_write = "\t".join([str(data) for data in data_to_write])
            file.write(f"{str_to_write}\n")

    def _prepare_data_for_logging(self) -> None:
        self._logging_data.clear()
        data = self._current_data.copy()
        data = adapt_data(data)
        self._logging_data.prepare(self._selected_parameters, data)

    @Slot(str)
    def set_filename(self, filename: str) -> None:
        self._filename = filename
        self._validate_filename()

    def _validate_filename(self) -> None:
        default_name: str = datetime.now().strftime('%Y_%m_%d__%H%M') + ".txt"
        if self._filename is None or (isinstance(self._filename, str) and len(self._filename) == 0):
            self._filename = default_name
        #TODO: check existence of the file

    def _prepare_file(self):
        self._validate_filename()
        str_to_write: str = "Elapsed Time\t"
        str_to_write += "\t".join(self._logging_data.parameter_names)
        with open(self._filename, 'a') as file:
            file.write(f"{str_to_write}\n")

    def _show_parameters(self):
        pass
        # if self._selected_parameter in self._selected_parameters:
        #     self.signal_selected_parameter_updated.emit(self._logging_data.time, self._logging_data.data[self._selected_parameter])