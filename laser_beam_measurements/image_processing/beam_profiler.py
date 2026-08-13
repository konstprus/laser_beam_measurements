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
# from enum import StrEnum
from .utils.denoising import find_noise_level_from_histogram, threshold
from .utils import beam_width as bm
from .utils.sub_image import get_cross_section
from .parameter_logger import ParameterLogger
from typing import Optional
from .beam_parameters import BeamParameters
from .beam_parameters.beam_parameters_selector import BeamParametersSelector


CROSS_SECTION_AUTO = "Cross section auto"
CROSS_SECTION_CENTER = "Cross section center"


class BeamProfiler(ImageProcessorBase):

    signal_cross_section_updated = Signal(numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray)
    signal_gauss_approximation_updated = Signal(numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray)
    signal_beam_center_updated = Signal(float, float)
    signal_beam_parameters_updated = Signal(BeamParameters)

    def __init__(self, *args, **kwargs):
        super(BeamProfiler, self).__init__(*args, **kwargs)

        self._flag_cross_sections_auto: bool = True
        self._bp : BeamParameters = BeamParameters(parent=self)
        self._bp.moveToThread(self.thread())
        self._bp_selector = BeamParametersSelector(self._bp, parent=self)
        self._bp_selector.moveToThread(self.thread())
        self._center: tuple[float, float] = (0.0, 0.0)
        self._pixel_size: float = 1.0
        self._parameter_logger: Optional[ParameterLogger] = None

        self._connect_signals()

    @property
    def parameter_logger(self) -> Optional[ParameterLogger]:
        return self._parameter_logger

    @parameter_logger.setter
    def parameter_logger(self, logger: ParameterLogger) -> None:
        if self._parameter_logger:
            self.signal_beam_parameters_updated.disconnect(self._parameter_logger.slot_set_data)
        self._parameter_logger = logger
        self._parameter_logger.setParent(self)
        self._parameter_logger.moveToThread(self.thread())
        self.signal_beam_parameters_updated.connect(self._parameter_logger.slot_set_data)
        self.update_available_parameters()

    @property
    def parameter_selector(self) -> Optional[BeamParametersSelector]:
        return self._bp_selector

    def _connect_signals(self) -> None:
        self._bp_selector.signal_selected.connect(self._slot_stat_updated)

    @Slot(BeamParameters)
    def _slot_stat_updated(self, _):
        self.update_available_parameters()

    def update_available_parameters(self) -> None:
        if self._parameter_logger is None:
            return
        if self._parameter_logger.is_active:
            return
        available_parameters = list()
        # Width methods
        width_group = self._bp.width
        for p in width_group:
            if p.enabled:
                available_parameters.append(f"{width_group.name}: {p.verbose_name}")

        # Position and orientation
        po_group = self._bp.position_and_orientation
        for p in po_group:
            if p.enabled:
                available_parameters.append(f"{po_group.name}: {p.verbose_name}")

        # Other parameters
        op_group = self._bp.other_parameters
        for p in op_group:
            if p.enabled:
                available_parameters.append(f"{op_group.name}: {p.verbose_name}")

        self._parameter_logger.slot_update_available_parameters(available_parameters)

    def process(self, image: numpy.ndarray) -> bool | None:
        if len(image.shape) != 2:
            return False
        noise_level = find_noise_level_from_histogram(image)
        denoised_image = threshold(image, noise_level)

        ps = self._pixel_size

        width_group = self._bp.width
        four_sigma = width_group.four_sigma()
        if four_sigma.enabled:
            cx, cy, d_4sigma_x, d_4sigma_y, _ = bm.width_by_moments(denoised_image, False)
            four_sigma.update((d_4sigma_x*ps, d_4sigma_y*ps))
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

        gauss_appr = width_group.gauss_appr()
        if gauss_appr.enabled:
            d0_x, d0_y = four_sigma.value() if four_sigma.enabled else (len(im_x)/2, len(im_y)/2)
            d_gauss_x, model_x = bm.width_by_gauss_approximation(im_x, xx, d0_x)
            d_gauss_y, model_y = bm.width_by_gauss_approximation(im_y, yy, d0_y)
            gauss_appr.update((d_gauss_x, d_gauss_y))
            self.signal_gauss_approximation_updated.emit(xx, model_x, yy, model_y)
        leveled_135 = width_group.leveled_135()
        if leveled_135.enabled:
            d_135_x = bm.width_by_level(im_x, level=0.135)
            d_135_y = bm.width_by_level(im_y, level=0.135)
            leveled_135.update((d_135_x*ps, d_135_y*ps))

        power_86 = width_group.power_86()
        other_parameters = self._bp.other_parameters
        power_parameter = other_parameters.power()
        area_parameter = other_parameters.area()
        if power_86.enabled:
            power = None
            area = None
            if power_parameter.enabled or area_parameter.enabled:
                power, area = bm.power_area(denoised_image)
            d_power = bm.width_by_power_level(denoised_image, level=0.86, power=power)
            power_86.update(d_power*ps)
            if power_parameter.enabled:
                power_parameter.update(power)
            if area_parameter.enabled:
                area_parameter.update(area)

        else:
            if power_parameter.enabled or area_parameter.enabled:
                power, area = bm.power_area(denoised_image)
                if power_parameter.enabled:
                    power_parameter.update(power)
                if area_parameter.enabled:
                    area_parameter.update(area)

        position_and_orientation = self._bp.position_and_orientation
        angle = position_and_orientation.angle()
        if angle.enabled:
            if BeamState.ANGLE in self._extra_context.keys():
                angle.update(self._extra_context[BeamState.ANGLE])

        global_position = position_and_orientation.global_position()
        if global_position.enabled:
            if BeamState.POS in self._extra_context.keys():
                pos = self._extra_context[BeamState.POS]
                global_position.update((pos[0]*ps, pos[1]*ps))

        local_position = position_and_orientation.local_position()
        if local_position.enabled:
            local_position.update((self._center[0]*ps, self._center[1]*ps))

        self._processed_image = denoised_image
        self.signal_beam_parameters_updated.emit(self._bp)
        return True

    def save_settings(self, settings: QSettings) -> None:
        settings.beginGroup("BeamProfiler")
        self._bp.save_settings(settings)
        settings.endGroup()

    def load_settings(self, settings: QSettings) -> None:
        settings.beginGroup("BeamProfiler")
        self._bp.load_settings(settings)
        settings.endGroup()

        self.update_available_parameters()

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
