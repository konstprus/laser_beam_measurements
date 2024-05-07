#
# Project: laser_beam_measurements
#
# File: beam_profiler.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


import numpy

from PySide6.QtCore import Signal, QSettings
from .image_processor_base import ImageProcessorBase
from .beam_finder import BeamState
from enum import StrEnum
from .utils.denoising import find_noise_level_from_histogram, threshold
from .utils import beam_width as bm
from .utils.sub_image import get_cross_section


class BeamWidthMethods(StrEnum):
    FOUR_SIGMA = "4 Sigma"
    LEVELED_135 = "13.5% level"
    GAUSS_APPR = "Gauss approximation"
    POWER_86 = "86% Power"


BEAM_WIDTH_METHODS = "Beam Width"


class BeamPositionAndOrientation(StrEnum):
    GLOBAL = "Global position"
    LOCAL = "Local position"
    ANGLE = "Angle"


BEAM_POSITION_AND_ORIENTATION = "Beam Position And Orientation"


class OtherParameters(StrEnum):
    AREA = "Area"
    POWER = "Power"


OTHER_PARAMETERS = "Other Parameters"


class BeamProfiler(ImageProcessorBase):

    signal_cross_section_updated = Signal(numpy.ndarray, numpy.ndarray)
    signal_gauss_approximation_updated = Signal(numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray)
    signal_beam_parameters_updated = Signal(dict)
    signal_beam_center_updated = Signal(float, float)

    def __init__(self, *args, **kwargs):
        super(BeamProfiler, self).__init__(*args, **kwargs)

        self._flag_cross_sections_auto: bool = True

        self._calculation_flags: dict[str, bool] = {
            BeamWidthMethods.FOUR_SIGMA: True,
            BeamWidthMethods.LEVELED_135: True,
            BeamWidthMethods.GAUSS_APPR: True,
            BeamWidthMethods.POWER_86: True,
            BeamPositionAndOrientation.GLOBAL: True,
            BeamPositionAndOrientation.LOCAL: True,
            BeamPositionAndOrientation.ANGLE: True,
            OtherParameters.AREA: True,
            OtherParameters.POWER: True
        }

        self._center: tuple[float, float] = (0.0, 0.0)
        # self._beam_parameters: dict[str, tuple[float, float] | float] = dict()
        self._beam_parameters: dict[str, dict[str, tuple[float, float] | float]] = dict()

    def process(self, image: numpy.ndarray) -> bool | None:
        if len(image.shape) != 2:
            return False
        noise_level = find_noise_level_from_histogram(image)
        denoised_image = threshold(image, noise_level)

        beam_parameters = dict()

        beam_width = dict()
        beam_position_and_orientation = dict()
        beam_other_parameters = dict()

        if self._calculation_flags[BeamWidthMethods.FOUR_SIGMA]:
            cx, cy, d_4sigma_x, d_4sigma_y, _ = bm.width_by_moments(denoised_image, False)
            # beam_parameters.update({BeamWidthMethods.FOUR_SIGMA: (d_4sigma_x, d_4sigma_y)})
            beam_width.update({BeamWidthMethods.FOUR_SIGMA: (d_4sigma_x, d_4sigma_y)})
            if self._flag_cross_sections_auto:
                self._center = (cx, cy)
                self.signal_beam_center_updated.emit(self._center[1], self._center[0])
        else:
            if self._flag_cross_sections_auto:
                self._center = (denoised_image.shape[1] / 2.0, denoised_image.shape[0] / 2.0)
                self.signal_beam_center_updated.emit(self._center[1], self._center[0])

        im_x, im_y = get_cross_section(denoised_image, self._center[0], self._center[1])
        self.signal_cross_section_updated.emit(im_x, im_y)

        if self._calculation_flags[BeamWidthMethods.GAUSS_APPR]:
            d0_x, d0_y = beam_parameters.get(BeamWidthMethods.FOUR_SIGMA, (len(im_x)/2, len(im_y)/2))
            d_gauss_x, xx, model_x = bm.width_by_gauss_approximation(im_x, d0_x)
            d_gauss_y, yy, model_y = bm.width_by_gauss_approximation(im_y, d0_y)
            # beam_parameters.update({BeamWidthMethods.GAUSS_APPR: (d_gauss_x, d_gauss_y)})
            beam_width.update({BeamWidthMethods.GAUSS_APPR: (d_gauss_x, d_gauss_y)})
            self.signal_gauss_approximation_updated.emit(xx, model_x, yy, model_y)

        if self._calculation_flags[BeamWidthMethods.LEVELED_135]:
            d_135_x = bm.width_by_level(im_x, level=0.135)
            d_135_y = bm.width_by_level(im_y, level=0.135)
            # beam_parameters.update({BeamWidthMethods.LEVELED_135: (d_135_x, d_135_y)})
            beam_width.update({BeamWidthMethods.LEVELED_135: (d_135_x, d_135_y)})

        if self._calculation_flags[BeamWidthMethods.POWER_86]:
            power = None
            area = None
            if self._calculation_flags[OtherParameters.POWER] or self._calculation_flags[OtherParameters.AREA]:
                power, area = bm.power_area(denoised_image)

            d_power = bm.width_by_power_level(denoised_image, level=0.86, power=power)
            # beam_parameters.update({
            #     BeamWidthMethods.POWER_86: d_power,
            # })
            beam_width.update({
                BeamWidthMethods.POWER_86: d_power,
            })

            if self._calculation_flags[OtherParameters.POWER]:
                # beam_parameters.update({
                #     OtherParameters.POWER: power
                # })
                beam_other_parameters.update({
                    OtherParameters.POWER: power
                })
            if self._calculation_flags[OtherParameters.AREA]:
                # beam_parameters.update({
                #     OtherParameters.AREA: area
                # })
                beam_other_parameters.update({
                    OtherParameters.AREA: area
                })
        else:
            if self._calculation_flags[OtherParameters.POWER] or self._calculation_flags[OtherParameters.AREA]:
                power, area = bm.power_area(denoised_image)
                if self._calculation_flags[OtherParameters.POWER]:
                    # beam_parameters.update({
                    #     OtherParameters.POWER: power
                    # })
                    beam_other_parameters.update({
                        OtherParameters.POWER: power
                    })
                if self._calculation_flags[OtherParameters.AREA]:
                    # beam_parameters.update({
                    #     OtherParameters.AREA: area
                    # })
                    beam_other_parameters.update({
                        OtherParameters.AREA: area
                    })

        if self._calculation_flags[BeamPositionAndOrientation.ANGLE]:
            if BeamState.ANGLE in self._extra_context.keys():
                # beam_parameters.update({
                #     BeamPositionAndOrientation.ANGLE: self._extra_context[BeamPositionAndOrientation.ANGLE]
                # })
                beam_position_and_orientation.update({
                    BeamPositionAndOrientation.ANGLE: self._extra_context[BeamState.ANGLE]
                })

        if self._calculation_flags[BeamPositionAndOrientation.GLOBAL]:
            if BeamState.POS in self._extra_context.keys():
                # beam_parameters.update({
                #     BeamPositionAndOrientation.GLOBAL: self._extra_context[BeamPositionAndOrientation.GLOBAL]
                # })
                beam_position_and_orientation.update({
                    BeamPositionAndOrientation.GLOBAL: self._extra_context[BeamState.POS]
                })

        if self._calculation_flags[BeamPositionAndOrientation.LOCAL]:
            # beam_parameters.update({
            #     BeamPositionAndOrientation.LOCAL: self._center
            # })
            beam_position_and_orientation.update({
                BeamPositionAndOrientation.LOCAL: self._center
            })

        self._processed_image = denoised_image

        self._beam_parameters.clear()

        if beam_width:
            beam_parameters.update({BEAM_WIDTH_METHODS: beam_width})

        if beam_position_and_orientation:
            beam_parameters.update({BEAM_POSITION_AND_ORIENTATION: beam_position_and_orientation})

        if beam_other_parameters:
            beam_parameters.update({OTHER_PARAMETERS: beam_other_parameters})

        self._beam_parameters.update(beam_parameters)
        self.signal_beam_parameters_updated.emit(self._beam_parameters)

        return True

    def save_settings(self, settings: QSettings) -> None:
        settings.beginGroup("BeamFinder")
        settings.endGroup()
