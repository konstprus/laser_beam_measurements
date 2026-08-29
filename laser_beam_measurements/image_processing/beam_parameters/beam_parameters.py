# 
# Project: laser_beam_measurements
#
# File: beam_parameters.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtCore import QObject, Slot, Signal, QSettings
from .beam_width_group import BeamWidthGroup
from .parameter import ParameterStat, Parameter
from .beam_position_and_orientation_group import BeamPositionAndOrientationGroup
from .beam_other_parameters_group import BeamOtherParametersGroup
from .parameter_group import ParameterGroup
from .average_control import AverageControl
from typing import Optional, Self

BeamParametersStat = list[tuple[str, list[ParameterStat]]]


class BeamParameters(QObject):

    signal_stat_updated = Signal()

    def __init__(self, parent=None, copied: Optional[Self] = None):
        super(BeamParameters, self).__init__(parent)
        self._width_group = None
        self._position_and_orientation_group = None
        self._other_parameters_group = None
        self._average_control: Optional[AverageControl] = None

        if copied:
            self._width_group = copied._width_group.copy()
            self._position_and_orientation_group = copied._position_and_orientation_group.copy()
            self._other_parameters_group = copied._other_parameters_group.copy()
        else:
            self._width_group = BeamWidthGroup()
            self._position_and_orientation_group = BeamPositionAndOrientationGroup()
            self._other_parameters_group = BeamOtherParametersGroup()

            self._average_control = AverageControl()
            self._width_group.set_average_control(self._average_control)
            self._position_and_orientation_group.set_average_control(self._average_control)
            self._other_parameters_group.set_average_control(self._average_control)


    @property
    def width(self) -> BeamWidthGroup:
        return self._width_group

    @property
    def position_and_orientation(self) -> BeamPositionAndOrientationGroup:
        return self._position_and_orientation_group

    @property
    def other_parameters(self) -> BeamOtherParametersGroup:
        return self._other_parameters_group

    def __copy__(self) -> Self:
        return BeamParameters(parent=self.parent(), copied=self)

    def copy(self) -> Self:
        return self.__copy__()

    def __len__(self) -> int:
        return (len(self._width_group) +
                len(self._position_and_orientation_group) +
                len(self._other_parameters_group))

    @property
    def average_control(self) -> AverageControl:
        return self._average_control

    # @Slot(list)
    # def update_stat(self, stat: BeamParametersStat) -> None:
    #     for stat_name, stat_value in stat:
    #         group: Optional[ParameterGroup] = None
    #         match stat_name:
    #             case self._width_group.name:
    #                 group = self._width_group
    #             case self._position_and_orientation_group.name:
    #                 group = self._position_and_orientation_group
    #             case self._other_parameters_group.name:
    #                 group = self._other_parameters_group
    #         if group is None:
    #             continue
    #         for parameter_stat in stat_value:
    #             param = group.get_parameter(parameter_stat[0])
    #             if param is None:
    #                 continue
    #             param.verbose_name = parameter_stat[1]
    #             param.enabled = parameter_stat[2]
    #     self.signal_stat_updated.emit()

    def save_settings(self, settings: QSettings) -> None:
        self._save_group(settings, self._width_group)
        self._save_group(settings, self._position_and_orientation_group)
        self._save_group(settings, self._other_parameters_group)

        settings.beginGroup("AverageControl")
        settings.setValue("Enabled", self._average_control.enabled)
        settings.setValue("Count", self._average_control.number)
        settings.endGroup()

    def _save_group(self, settings: QSettings, group: ParameterGroup) -> None:
        settings.beginGroup(group.name)
        for param in group:
            settings.beginGroup(param.name)
            settings.setValue("Enabled", param.enabled)
            settings.setValue("VerboseName", param.verbose_name)
            settings.endGroup()
        settings.endGroup()

    def load_settings(self, settings: QSettings) -> None:
        self._load_group(settings, self._width_group)
        self._load_group(settings, self._position_and_orientation_group)
        self._load_group(settings, self._other_parameters_group)

        settings.beginGroup("AverageControl")
        if settings.contains("Enabled"):
            enabled = settings.value("Enabled")
            if enabled == "true":
                self._average_control.enabled = True
            else:
                self._average_control.enabled = False

            if settings.contains("Count"):
                self._average_control.number = int(settings.value("Count"))
        settings.endGroup()

    def _load_group(self, settings: QSettings, group: ParameterGroup) -> None:
        settings.beginGroup(group.name)

        for param in group:
            settings.beginGroup(param.name)
            if settings.contains("Enabled"):
                enabled = settings.value("Enabled")
                if enabled == "true":
                    param.enabled = True
                else :
                    param.enabled = False
            if settings.contains("VerboseName"):
                param.verbose_name = settings.value("VerboseName")
            settings.endGroup()

        settings.endGroup()