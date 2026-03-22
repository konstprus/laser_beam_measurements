#
# Project: laser_beam_measurements
#
# File: beam_position_and_orientation_group.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from .parameter_group import ParameterGroup
from .parameter import Parameter
from . import define


class BeamPositionAndOrientationGroup(ParameterGroup):

    def __init__(self):
        super().__init__(group_name=define.BEAM_OTHER_PARAMETERS_GROUP_NAME)
        self.add_parameter(Parameter(name=define.BPO_GLOBAL))
        self.add_parameter(Parameter(name=define.BPO_LOCAL))
        self.add_parameter(Parameter(name=define.BPO_ANGLE))
        self.finish_to_add()

    def global_position(self) -> Parameter:
        return self._parameters[define.BPO_GLOBAL]

    def local_position(self) -> Parameter:
        return self._parameters[define.BPO_LOCAL]

    def angle(self) -> Parameter:
        return self._parameters[define.BPO_ANGLE]
