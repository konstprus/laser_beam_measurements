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
from typing import Optional

BeamParametersStat = list[tuple[str, list[ParameterStat]]]


class BeamParameters(QObject):

    signal_stat_updated = Signal()

    def __init__(self, parent=None):
        super(BeamParameters, self).__init__(parent)
        self._width_group = BeamWidthGroup()
        self._position_and_orientation_group = BeamPositionAndOrientationGroup()
        self._other_parameters_group = BeamOtherParametersGroup()

        # self._width_model = ParameterGroupItemModel(self._width_group)
        # self._position_model = ParameterGroupItemModel(self._position_and_orientation_group)
        # self._other_model = ParameterGroupItemModel(self._other_parameters_group)

    @property
    def width(self) -> BeamWidthGroup:
        return self._width_group

    @property
    def position_and_orientation(self) -> BeamPositionAndOrientationGroup:
        return self._position_and_orientation_group

    @property
    def other_parameters(self) -> BeamOtherParametersGroup:
        return self._other_parameters_group

    # @property
    # def width_model(self) -> ParameterGroupItemModel:
    #     return self._width_model
    #
    # @property
    # def position_model(self) -> ParameterGroupItemModel:
    #     return self._position_model
    #
    # @property
    # def other_model(self) -> ParameterGroupItemModel:
    #     return self._other_model
    #
    # def model_changed(self):
    #     self._width_model.dataChanged.emit(QModelIndex(), QModelIndex())
    #     self._position_model.dataChanged.emit(QModelIndex(), QModelIndex())
    #     self._other_model.dataChanged.emit(QModelIndex(), QModelIndex())

    # @property
    # def stat(self) -> BeamParametersStat:
    #     return [
    #         (self._width_group.name, self._width_group.stat),
    #         (self._position_and_orientation_group.name, self._position_and_orientation_group.stat),
    #         (self._other_parameters_group.name, self._other_parameters_group.stat),
    #     ]

    @Slot(list)
    def update_stat(self, stat: BeamParametersStat) -> None:
        for stat_name, stat_value in stat:
            group: Optional[ParameterGroup] = None
            match stat_name:
                case self._width_group.name:
                    group = self._width_group
                case self._position_and_orientation_group.name:
                    group = self._position_and_orientation_group
                case self._other_parameters_group.name:
                    group = self._other_parameters_group
            if group is None:
                continue
            for parameter_stat in stat_value:
                param = group.get_parameter(parameter_stat[0])
                if param is None:
                    continue
                param.verbose_name = parameter_stat[1]
                param.enabled = parameter_stat[2]

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