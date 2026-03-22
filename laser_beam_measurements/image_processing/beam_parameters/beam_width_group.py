#
# Project: laser_beam_measurements
#
# File: beam_width_group.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from .parameter_group import ParameterGroup
from .parameter import Parameter
from . import define

from typing import Optional, Self


class BeamWidthGroup(ParameterGroup):

    def __init__(self) -> None:
        super().__init__(group_name=define.BEAM_WIDTH_GROUP_NAME)
        self.add_parameter(Parameter(name=define.BW_FOUR_SIGMA))
        self.add_parameter(Parameter(name=define.BW_LEVELED_135))
        self.add_parameter(Parameter(name=define.BW_GAUSS_APPR))
        self.add_parameter(Parameter(name=define.BW_POWER_86))
        self.finish_to_add()

    def four_sigma(self) -> Parameter:
        return self._parameters[define.BW_FOUR_SIGMA]

    def leveled_135(self) -> Parameter:
        return self._parameters[define.BW_LEVELED_135]

    def gauss_appr(self) -> Parameter:
        return self._parameters[define.BW_GAUSS_APPR]

    def power_86(self) -> Parameter:
        return self._parameters[define.BW_POWER_86]

    # def __copy__(self) -> Self:
    #     return BeamWidthGroup()