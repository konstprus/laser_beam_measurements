#
# Project: laser_beam_measurements
#
# File: beam_profiler_parameters.py
#
# Author: Konstantin Prusakov
#
# Copyright 2025 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from image_processor_parameters import Parameter, Section, ImageProcessorParameters


CROSS_SECTION_AUTO = "Cross section auto"
CROSS_SECTION_CENTER = "Cross section center"

class BeamWidthMethods:
    FOUR_SIGMA = "4 Sigma"
    LEVELED_135 = "13.5% level"
    GAUSS_APPR = "Gauss approximation"
    POWER_86 = "86% Power"


BEAM_WIDTH_METHODS = "Beam Width"


class BeamPositionAndOrientation:
    GLOBAL = "Global position"
    LOCAL = "Local position"
    ANGLE = "Angle"


BEAM_POSITION_AND_ORIENTATION = "Beam Position And Orientation"


class OtherParameters:
    AREA = "Area"
    POWER = "Power"


OTHER_PARAMETERS = "Other Parameters"


class BeamProfilerParameters(ImageProcessorParameters):

    def __init__(self) -> None:
        super(BeamProfilerParameters, self).__init__("beam profiler parameters")

        width_4_sigma = Parameter(BeamWidthMethods.FOUR_SIGMA,True)
        width_leveled_135 = Parameter(BeamWidthMethods.LEVELED_135, True, default_extra_value=13.5, mask="{}% level")
        width_gauss = Parameter(BeamWidthMethods.GAUSS_APPR, True)
        width_power = Parameter(BeamWidthMethods.POWER_86, True)
        width_section = Section(BEAM_WIDTH_METHODS,
                                [width_4_sigma, width_leveled_135, width_gauss,width_power],
                                True)
        self.add_section(width_section)

        pos_global = Parameter(BeamPositionAndOrientation.GLOBAL,True)
        pos_local = Parameter(BeamPositionAndOrientation.LOCAL, True)
        angle = Parameter(BeamPositionAndOrientation.ANGLE, True)
        pos_angle_section = Section(BEAM_POSITION_AND_ORIENTATION,
                                [pos_global, pos_local, angle,width_power],
                                True)
        self.add_section(pos_angle_section)

        area = Parameter(BeamPositionAndOrientation.GLOBAL,True)
        power = Parameter(BeamPositionAndOrientation.LOCAL, True)
        other_section = Section(OTHER_PARAMETERS,
                                [area, power],
                                True)
        self.add_section(other_section)





