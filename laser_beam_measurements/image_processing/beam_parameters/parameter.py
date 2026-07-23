# 
# Project: laser_beam_measurements
#
# File: parameter.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from typing import Optional, Union, Self, Sized
from statistics import mean

from .average_control import AverageControl

ParameterValue = Union[float, tuple[float, float]]
ParameterStat = tuple[str, str, bool]

class Parameter(object):

    def __init__(self, name: str, value: Optional[ParameterValue] = None, verbose_name: Optional[str] = None) -> None:
        self._name: str = name
        self._verbose_name: str = self._name
        self._enabled: bool = True
        self._value: Optional[ParameterValue] = value
        # self._averaging: bool = False
        self._values: Optional[list[ParameterValue]] = None
        self._average_control: Optional[AverageControl] = None
        if verbose_name is not None:
            self._verbose_name: str = verbose_name

    @property
    def name(self) -> str:
        return self._name

    @property
    def verbose_name(self) -> str:
        return self._verbose_name

    @verbose_name.setter
    def verbose_name(self, value: str) -> None:
        self._verbose_name = value

    def reset_verbose_name(self) -> None:
        self._verbose_name = self._name

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, enabled: bool) -> None:
        self._enabled = enabled

    def value(self, axis: Optional[int] = None) -> Optional[ParameterValue]:
        value = self._value if self._average_control is None or not self._average_control.enabled else self.average_value()
        if axis is None:
            return value
        if axis == 0:
            return self._value[0] if isinstance(value, tuple) else value
        else:
            return self._value[1] if isinstance(value, tuple) else None

    @property
    def count(self) -> int:
        if isinstance(self._value, Sized):
            return len(self._value)
        else:
            return 1

    def update(self, value: ParameterValue):
        self._value = value
        if self._average_control is not None and self._average_control.enabled:
            if self._average_control.counter == 0:
                if self._values:
                    self._values.clear()
                else:
                    self._values = list()
            self._values.append(value)

    def average_value(self) -> Optional[ParameterValue]:
        if self._values is None or len(self._values) == 0:
            return None
        if isinstance(self._values[0], tuple):
            first, second = zip(*self._values)
            return mean(first), mean(second)
        return mean(self._values)

    def reset_values(self) -> None:
        if self._values is not None:
            self._values.clear()

    def set_average_control(self, control: AverageControl) -> None:
        self._average_control = control

    def __str__(self) -> str:
        return f"Parameter '{self._name}': {self._value}"

    def __copy__(self) -> Self:
        return Parameter(self._name, value=self.value(), verbose_name=self.verbose_name)

    def copy(self) -> Self:
        # return self.__copy__()
        return Parameter(self._name, value=self.value(), verbose_name=self.verbose_name)

    # @property
    # def stat(self) -> ParameterStat:
    #     return self._name, self._verbose_name, self._enabled

    def __len__(self) -> int:
        return 1 if self._enabled and self._value is not None else 0