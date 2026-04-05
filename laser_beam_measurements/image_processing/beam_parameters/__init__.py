# 
# Project: laser_beam_measurements
#
# File: __init__.py.py
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
from .item_model import ParameterGroupItemModel
from typing import Optional, Self

BeamParametersStat = list[tuple[str, list[ParameterStat]]]


class BeamParameters(QObject):

    signal_stat_updated = Signal()

    def __init__(self, parent=None, copied: Optional[Self] = None):
        super(BeamParameters, self).__init__(parent)
        self._width_group = None
        self._position_and_orientation_group = None
        self._other_parameters_group = None

        if copied:
            self._width_group = copied._width_group.copy()
            self._position_and_orientation_group = copied._position_and_orientation_group.copy()
            self._other_parameters_group = copied._other_parameters_group.copy()
        else:
            self._width_group = BeamWidthGroup()
            self._position_and_orientation_group = BeamPositionAndOrientationGroup()
            self._other_parameters_group = BeamOtherParametersGroup()


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