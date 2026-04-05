# 
# Project: laser_beam_measurements
#
# File: parameter_group.py.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from .parameter import Parameter, ParameterStat
from typing import Optional, Self, Iterable

class ParameterGroup(object):

    class Iterator:

        def __init__(self, group: 'ParameterGroup'):
            self.group: ParameterGroup = group
            self._current_index = -1

        def __iter__(self) -> Self:
            return self

        def __next__(self) -> Parameter:
            self._current_index += 1
            if self._current_index < len(self.group._append_order):
                return self.group._parameters[self.group._append_order[self._current_index]]
            raise StopIteration

    def __init__(self, group_name: str, copied: Optional[Self] = None) -> None:
        self._name: str = group_name
        self._parameters: dict[str, Parameter] = {}
        self._append_order: list[str] = []
        self._enabled_to_add: bool = True

        if copied is not None:
            [self.add_parameter(copied._parameters[name].copy()) for name in copied._append_order]
            self.finish_to_add()

    def add_parameter(self, parameter: Parameter) -> None:
        if self._enabled_to_add and parameter.name not in self._append_order:
            self._parameters[parameter.name] = parameter
            self._append_order.append(parameter.name)

    def finish_to_add(self) -> None:
        self._enabled_to_add = False

    @property
    def name(self) -> str:
        return self._name

    def get_parameter(self, parameter_name: str) -> Optional[Parameter]:
        return self._parameters.get(parameter_name, None)

    def __copy__(self) -> Self:
        return ParameterGroup(group_name=self._name, copied=self)

    def copy(self) -> Self:
        return self.__copy__()

    def __iter__(self) -> Iterable:
        return self.Iterator(self)

    def __len__(self) -> int:
        non_zero_parameters: int = 0
        for param in self._parameters.values():
            non_zero_parameters += len(param)
        return non_zero_parameters

    # @property
    # def stat(self) -> list[ParameterStat]:
    #     return [self._parameters[name].stat for name in self._append_order]
