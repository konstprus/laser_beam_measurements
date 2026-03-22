# 
# Project: laser_beam_measurements
#
# File: __init__.py.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtCore import QObject
from .beam_width_group import BeamWidthGroup
from .beam_position_and_orientation_group import BeamPositionAndOrientationGroup
from .beam_other_parameters_group import BeamOtherParametersGroup
from .parameter_group import ParameterGroup
from .item_model import ParameterGroupItemModel


class BeamParameters(QObject):

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