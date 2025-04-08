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

from PySide6.QtCore import Signal, QSettings, Slot, QPointF, QMutexLocker
from .image_processor_base import ImageProcessorBase
from .beam_finder import BeamState
from enum import StrEnum
from .utils.denoising import find_noise_level_from_histogram, threshold
from .utils import beam_width as bm
from .utils.sub_image import get_cross_section
from .parameter_logger import ParameterLogger
from typing import Optional


CROSS_SECTION_AUTO = "Cross section auto"
CROSS_SECTION_CENTER = "Cross section center"

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

    signal_cross_section_updated = Signal(numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray)
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
        self._pixel_size: float = 1.0
        self._parameter_logger: Optional[ParameterLogger] = None

    @property
    def parameter_logger(self) -> Optional[ParameterLogger]:
        return self._parameter_logger

    @parameter_logger.setter
    def parameter_logger(self, logger: ParameterLogger) -> None:
        if self._parameter_logger:
            self.signal_beam_parameters_updated.disconnect(self._parameter_logger.slot_set_data)
        self._parameter_logger = logger
        self._parameter_logger.setParent(self)
        self.signal_beam_parameters_updated.connect(self._parameter_logger.slot_set_data)
        self.update_available_parameters()

    def update_available_parameters(self) -> None:
        if self._parameter_logger is None:
            return
        if self._parameter_logger.is_active:
            return
        available_parameters = list()
        # Width methods
        if self._calculation_flags[BeamWidthMethods.FOUR_SIGMA]:
            available_parameters.append(f"{BEAM_WIDTH_METHODS}: {BeamWidthMethods.FOUR_SIGMA}")
        if self._calculation_flags[BeamWidthMethods.LEVELED_135]:
            available_parameters.append(f"{BEAM_WIDTH_METHODS}: {BeamWidthMethods.LEVELED_135}")
        if self._calculation_flags[BeamWidthMethods.GAUSS_APPR]:
            available_parameters.append(f"{BEAM_WIDTH_METHODS}: {BeamWidthMethods.GAUSS_APPR}")
        if self._calculation_flags[BeamWidthMethods.POWER_86]:
            available_parameters.append(f"{BEAM_WIDTH_METHODS}: {BeamWidthMethods.POWER_86}")

        # Position and orientation
        if self._calculation_flags[BeamPositionAndOrientation.GLOBAL]:
            available_parameters.append(f"{BEAM_POSITION_AND_ORIENTATION}: {BeamPositionAndOrientation.GLOBAL}")
        if self._calculation_flags[BeamPositionAndOrientation.LOCAL]:
            available_parameters.append(f"{BEAM_POSITION_AND_ORIENTATION}: {BeamPositionAndOrientation.LOCAL}")
        if self._calculation_flags[BeamPositionAndOrientation.ANGLE]:
            available_parameters.append(f"{BEAM_POSITION_AND_ORIENTATION}: {BeamPositionAndOrientation.ANGLE}")

        # Other parameters
        if self._calculation_flags[OtherParameters.POWER]:
            available_parameters.append(f"{OTHER_PARAMETERS}: {OtherParameters.POWER}")
        if self._calculation_flags[OtherParameters.AREA]:
            available_parameters.append(f"{OTHER_PARAMETERS}: {OtherParameters.AREA}")

        self._parameter_logger.slot_update_available_parameters(available_parameters)

    def process(self, image: numpy.ndarray) -> bool | None:
        if len(image.shape) != 2:
            return False
        noise_level = find_noise_level_from_histogram(image)
        denoised_image = threshold(image, noise_level)

        beam_parameters = dict()

        beam_width = dict()
        beam_position_and_orientation = dict()
        beam_other_parameters = dict()
        ps = self._pixel_size

        if self._calculation_flags[BeamWidthMethods.FOUR_SIGMA]:
            cx, cy, d_4sigma_x, d_4sigma_y, _ = bm.width_by_moments(denoised_image, False)
            # beam_parameters.update({BeamWidthMethods.FOUR_SIGMA: (d_4sigma_x, d_4sigma_y)})
            beam_width.update({BeamWidthMethods.FOUR_SIGMA: (d_4sigma_x*ps, d_4sigma_y*ps)})
            if self._flag_cross_sections_auto:
                self._center = (cx, cy)
                self.signal_beam_center_updated.emit(self._center[1], self._center[0])
        else:
            if self._flag_cross_sections_auto:
                self._center = (denoised_image.shape[1] / 2.0, denoised_image.shape[0] / 2.0)
                self.signal_beam_center_updated.emit(self._center[1], self._center[0])

        im_x, im_y = get_cross_section(denoised_image, self._center[0], self._center[1])
        xx = numpy.arange(-len(im_x) / 2, len(im_x) / 2, dtype=numpy.float64) * ps
        yy = numpy.arange(-len(im_y) / 2, len(im_y) / 2, dtype=numpy.float64) * ps
        self.signal_cross_section_updated.emit(xx, im_x, yy, im_y)

        if self._calculation_flags[BeamWidthMethods.GAUSS_APPR]:
            d0_x, d0_y = beam_parameters.get(BeamWidthMethods.FOUR_SIGMA, (len(im_x)/2, len(im_y)/2))
            d_gauss_x, model_x = bm.width_by_gauss_approximation(im_x, xx, d0_x)
            d_gauss_y, model_y = bm.width_by_gauss_approximation(im_y, yy, d0_y)
            # beam_parameters.update({BeamWidthMethods.GAUSS_APPR: (d_gauss_x, d_gauss_y)})
            beam_width.update({BeamWidthMethods.GAUSS_APPR: (d_gauss_x, d_gauss_y)})
            self.signal_gauss_approximation_updated.emit(xx, model_x, yy, model_y)

        if self._calculation_flags[BeamWidthMethods.LEVELED_135]:
            d_135_x = bm.width_by_level(im_x, level=0.135)
            d_135_y = bm.width_by_level(im_y, level=0.135)
            # beam_parameters.update({BeamWidthMethods.LEVELED_135: (d_135_x, d_135_y)})
            beam_width.update({BeamWidthMethods.LEVELED_135: (d_135_x*ps, d_135_y*ps)})

        if self._calculation_flags[BeamWidthMethods.POWER_86]:
            power = None
            area = None
            if self._calculation_flags[OtherParameters.POWER] or self._calculation_flags[OtherParameters.AREA]:
                power, area = bm.power_area(denoised_image)

            d_power = bm.width_by_power_level(denoised_image, level=0.86, power=power)
            beam_width.update({BeamWidthMethods.POWER_86: d_power*ps})

            if self._calculation_flags[OtherParameters.POWER]:
                beam_other_parameters.update({OtherParameters.POWER: power})
            if self._calculation_flags[OtherParameters.AREA]:
                beam_other_parameters.update({OtherParameters.AREA: area})

        else:
            if self._calculation_flags[OtherParameters.POWER] or self._calculation_flags[OtherParameters.AREA]:
                power, area = bm.power_area(denoised_image)
                if self._calculation_flags[OtherParameters.POWER]:
                    beam_other_parameters.update({OtherParameters.POWER: power})
                if self._calculation_flags[OtherParameters.AREA]:
                    beam_other_parameters.update({OtherParameters.AREA: area})

        if self._calculation_flags[BeamPositionAndOrientation.ANGLE]:
            if BeamState.ANGLE in self._extra_context.keys():
                beam_position_and_orientation.update({BeamPositionAndOrientation.ANGLE: self._extra_context[BeamState.ANGLE]})

        if self._calculation_flags[BeamPositionAndOrientation.GLOBAL]:
            if BeamState.POS in self._extra_context.keys():
                beam_position_and_orientation.update({
                    BeamPositionAndOrientation.GLOBAL:
                        (self._extra_context[BeamState.POS][0]*ps,
                         self._extra_context[BeamState.POS][1]*ps)
                })

        if self._calculation_flags[BeamPositionAndOrientation.LOCAL]:
            beam_position_and_orientation.update({BeamPositionAndOrientation.LOCAL: (self._center[0]*ps, self._center[1]*ps)})

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

    def _set_init_parameters(self, parameters: dict) -> None:
        self._pixel_size = float(parameters.get("pixel_size", 1.0))


    def _set_parameter_value(self, parameter: str, value: object) -> None:
        with QMutexLocker(self._mutex):
            if parameter == CROSS_SECTION_CENTER and not self._flag_cross_sections_auto:
                if isinstance(value, tuple):
                    self._center = value
                elif isinstance(value, QPointF):
                    self._center = (value.x(), value.y())
            elif parameter == CROSS_SECTION_AUTO:
                self._flag_cross_sections_auto = bool(value)
        super()._set_parameter_value(parameter, value)

    def get_parameter_value(self, parameter: str) -> object | None:
        with QMutexLocker(self._mutex):
            if parameter == CROSS_SECTION_CENTER:
                return self._center
            elif parameter == CROSS_SECTION_AUTO:
                return self._flag_cross_sections_auto
        return super().get_parameter_value(parameter)

    @Slot(QPointF)
    @Slot(tuple)
    def slot_set_center(self, center: QPointF | tuple) -> None:
        if not self._flag_cross_sections_auto:
            if isinstance(center, tuple):
                self._center = center
            elif isinstance(center, QPointF):
                self._center = (center.x(), center.y())
