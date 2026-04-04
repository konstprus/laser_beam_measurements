# 
# Project: laser_beam_measurements
#
# File: beam_parameters_selector.py.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#
from PySide6.QtCore import QObject, Slot, Signal

from laser_beam_measurements.image_processing.beam_parameters import BeamParameters, BeamParametersStat
from laser_beam_measurements.image_processing.beam_parameters.parameter_group import ParameterGroup
from laser_beam_measurements.image_processing.beam_parameters.parameter import ParameterStat
from laser_beam_measurements.image_processing.beam_parameters.define import *

class BeamParametersSelector(QObject):

    signal_show_bp_stat = Signal(BeamParametersStat)
    signal_selected = Signal(BeamParameters)

    def __init__(self, bp: BeamParameters, parent=None):
        super(BeamParametersSelector, self).__init__(parent)
        self._bp: BeamParameters = bp

    @property
    def bp(self) ->BeamParameters:
        return self._bp

    def _show_current(self):
        self.signal_show_bp_stat.emit(self._bp.stat)

    def _select_group(self, stat: list[ParameterStat], group: ParameterGroup):
        for name, verbose, enabled in stat:
            p = group.get_parameter(name)
            if p is None:
                continue
            p.verbose_name = verbose
            p.enabled = enabled

    @Slot(list)
    def slot_select(self, stat: BeamParametersStat):
        for name, group_stat in stat:
            if name == BEAM_WIDTH_GROUP_NAME:
                self._select_group(group_stat, self._bp.width)
            elif name == BEAM_POSITION_AND_ORIENTATION_GROUP_NAME:
                self._select_group(group_stat, self._bp.position_and_orientation)
            elif name == BEAM_OTHER_PARAMETERS_GROUP_NAME:
                self._select_group(group_stat, self._bp.other_parameters)
        self.signal_selected.emit(self._bp)

