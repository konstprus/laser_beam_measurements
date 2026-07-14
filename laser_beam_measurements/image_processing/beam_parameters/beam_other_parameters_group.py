#
# Project: laser_beam_measurements
#
# File: beam_other_parameters_group.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from laser_beam_measurements.image_processing.beam_parameters.define import BOP_AREA, BOP_POWER
from .parameter_group import ParameterGroup
from .parameter import Parameter
from . import define


class BeamOtherParametersGroup(ParameterGroup):

    def __init__(self):
        super().__init__(group_name=define.BEAM_OTHER_PARAMETERS_GROUP_NAME)
        self.add_parameter(Parameter(name=BOP_AREA))
        self.add_parameter(Parameter(name=BOP_POWER))
        self.finish_to_add()

    def area(self) -> Parameter:
        return self._parameters[define.BOP_AREA]

    def power(self) -> Parameter:
        return self._parameters[define.BOP_POWER]