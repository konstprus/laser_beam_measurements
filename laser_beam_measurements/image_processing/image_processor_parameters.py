# 
# Project: laser_beam_measurements
#
# File: image_processor_parameters.py
#
# Author: Konstantin Prusakov
#
# Copyright 2025 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from typing import Optional, Union
from contextlib import suppress


class Parameter(object):

    def __init__(self, name: str, available: bool = False, **kwargs) -> None:
        self._available: bool = available
        self._name: str = name
        self._available_extra_value: bool = kwargs.get("available_extra_value", False)
        self._extra_values: set[float] = set()
        if self._available_extra_value:
            self._mask: str = kwargs.get("mask", "")
            self._default_extra_value: Optional[float] = kwargs.get("default_extra_value", None)

    @property
    def valid(self) -> bool:
        return len(self._name) > 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def available(self) -> bool:
        return self._available

    @available.setter
    def available(self, value: bool) -> None:
        self._available = value

    @property
    def default_extra_value(self) -> Optional[float]:
        return self._default_extra_value

    @property
    def extra_values(self) -> list[float]:
        return list(self._extra_values)

    @property
    def available_extra_value(self) -> bool:
        return self._available_extra_value

    def set_extra_value(self, value: float) -> None:
        if  self._available_extra_value:
            self._extra_values.add(value)

    def remove_extra_value(self, value: float) -> None:
        with suppress(ValueError, KeyError):
            self._extra_values.remove(value)

    @property
    def default_verbose_name(self) -> str:
        return self._name

    def verbose_name(self, *args, **kwargs) -> str:
        return self._mask.format(args, kwargs)


class Section(Parameter):

    def __init__(self, name: str, parameters: Optional[list[Parameter]] = None, finish: bool = False) -> None:
        super(Parameter, self).__init__(name)
        self._parameters: dict[str, Parameter] = dict()
        self._can_add_parameters: bool = True
        if parameters:
            self.add_parameters(parameters, finish)

    def disable_add_parameters(self) -> None:
        self._can_add_parameters = False

    def add_parameter(self, parameter: Parameter) -> None:
        if not self._can_add_parameters:
            return
        if not parameter.valid:
            return
        if parameter.name in self._parameters:
            return
        self._parameters[parameter.name] = parameter

    def add_parameters(self, parameters: list[Parameter], finish = False) -> None:
        for parameter in parameters:
            self.add_parameter(parameter)
        if finish:
            self.disable_add_parameters()

    def get_parameter(self, name: str) -> Optional[Parameter]:
        if name in self._parameters:
            return self._parameters[name]
        return None

    def parameter_names(self) -> list[str]:
        return list(self._parameters.keys())

    def is_parameters_available(self, name: str) -> bool:
        parameter = self.get_parameter(name)
        return parameter.available if parameter else False


class ImageProcessorParameters(Section):

    def __init__(self, name: str) -> None:
        super(Parameter, self).__init__(name)
        self._sections: dict[str, Section] = dict()

    def add_section(self, section: Union[str, Section]) -> None:
        if not self._can_add_parameters:
            return
        if isinstance(section, str):
            if section in self._sections:
                return
            self._sections[section] = Section(section)
        elif isinstance(section, Section):
            if not section.valid:
                return
            if section.name in self._sections:
                return
            self._sections[section.name] = section
            for parameter_name in section.parameter_names():
                parameter = section.get_parameter(parameter_name)
                if parameter is not None:
                    self.add_parameter(parameter)

    def get_section(self, name: str) -> Optional[Section]:
        if name in self._sections:
            return self._sections[name]
        return None
