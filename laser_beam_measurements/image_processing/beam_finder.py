#
# Project: laser_beam_measurements
#
# File: beam_finder.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

import numpy

from .image_processor_base import ImageProcessorBase

from .utils.sub_image import rotate_sub_image
from .utils.denoising import threshold
from .utils.beam_width import width_by_moments
from enum import StrEnum
import cv2
from math import pi
from PySide6.QtCore import Signal, Slot, QMutexLocker, QPointF, QSizeF, QSettings
from laser_beam_measurements.utils.settings_bool_reader import read_boolean_value


class BeamFinderParameters(StrEnum):
    SHAPE = "shape"
    POSITION = "position"
    ROTATION_ANGLE = "angle"
    SCALE = "scale"
    NOISE_LEVEL = "noise level"
    FIND_AUTO = "auto"
    ROTATION_ENABLE = "rotation enable"
    DELETE_NOISE_ENABLE = "delete noise"
    MANUAL_ROTATION_ENABLE = "manual rotation"


class BeamState(StrEnum):
    POS = 'pos'
    SIZE = 'size'
    ANGLE = 'angle'


class BeamFinder(ImageProcessorBase):

    signal_beam_state_updated = Signal(dict)

    def __init__(self, *args, **kwargs):
        super(BeamFinder, self).__init__(*args, **kwargs)
        self._flag_transmit_context = True
        self._shape: tuple[float, float] = (0.0, 0.0)
        self._position: tuple[float, float] = (0.0, 0.0)
        self._rotation_angle: float = 0.0
        self._scale_factor: float = 1.0
        self._noise_level: float = 0.0

        self._flag_find_auto: bool = True
        self._flag_delete_noise: bool = False
        self._flag_rotation_enable: bool = False
        self._flag_manual_rotation: bool = False

        self._beam_state = dict()

    def process(self, image: numpy.ndarray) -> bool | None:
        self._processed_image = self.roi_find(image)
        if self._flag_find_auto:
            self.signal_beam_state_updated.emit(self._beam_state)
        if self._processed_image is not None:
            return True
        return False

    @Slot(dict)
    def slot_set_beam_state(self, state: dict) -> None:
        if self._flag_find_auto:
            return
        pos = state.get(BeamState.POS, None)
        if pos is not None:
            if isinstance(pos, QPointF):
                self._position = (pos.x(), pos.y())
            elif isinstance(pos, tuple) and len(pos) == 2:
                self._position = tuple(pos)
        shape = state.get(BeamState.SIZE, None)
        if shape is not None:
            if isinstance(shape, QSizeF):
                self._shape = (shape.width(), shape.height())
            elif isinstance(shape, tuple) and len(shape) == 2:
                self._shape = tuple(shape)
        if self._flag_rotation_enable and self._flag_manual_rotation:
            angle = state.get(BeamState.ANGLE, None)
            if isinstance(angle, float):
                self._rotation_angle = angle * pi / 180

    def roi_find(self, image: numpy.ndarray | None) -> numpy.ndarray | None:
        _image = image
        if _image is None:
            return None
        if len(_image.shape) > 2:
            _image = cv2.cvtColor(_image, cv2.COLOR_RGB2GRAY)
        if self._flag_find_auto:
            beam_state = dict()
            if _image.shape[0] == 0 or _image.shape[1] == 0:
                # return numpy.array(_image, copy=True)
                return None
            if self._flag_delete_noise:
                _image = threshold(_image, self._noise_level)
            cx, cy, dx, dy, angle = width_by_moments(_image, self._flag_rotation_enable)
            self._position = (cx, cy)
            scaled_dx = 2 * self._scale_factor * dx
            scaled_dy = 2 * self._scale_factor * dy
            w = scaled_dx if scaled_dx < _image.shape[1] else _image.shape[1]
            h = scaled_dy if scaled_dy < _image.shape[0] else _image.shape[0]
            self._shape = (w, h)
            beam_state.update({
                BeamState.POS: self._position,
                BeamState.SIZE: self._shape
            })
            if self._flag_rotation_enable and not self._flag_manual_rotation:
                self._rotation_angle = angle
            if self._flag_rotation_enable:
                beam_state.update({
                    BeamState.ANGLE: self._rotation_angle * 180 / pi,
                })
            self._beam_state.clear()
            self._beam_state.update(beam_state)
        w, h = self._shape
        center = self._position
        if not self._flag_rotation_enable:
            self._rotation_angle = 0.0
        return rotate_sub_image(image, center, w, h, self._rotation_angle)

    def _set_parameter_value(self, parameter: BeamFinderParameters | str, value: object) -> None:
        with QMutexLocker(self._mutex):
            if parameter == BeamFinderParameters.SHAPE and not self._flag_find_auto:
                if isinstance(value, tuple) and len(value) == 2:
                    self._shape = value
            elif parameter == BeamFinderParameters.POSITION and not self._flag_find_auto:
                if isinstance(value, tuple) and len(value) == 2:
                    self._position = value
            elif parameter == BeamFinderParameters.ROTATION_ANGLE and self._flag_manual_rotation:
                if isinstance(value, (float, int)):
                    self._rotation_angle = value
            elif parameter == BeamFinderParameters.SCALE:
                if isinstance(value, (float, int)):
                    self._scale_factor = value
            elif parameter == BeamFinderParameters.NOISE_LEVEL:
                if isinstance(value, (float, int)):
                    self._noise_level = value
            elif parameter == BeamFinderParameters.FIND_AUTO:
                if isinstance(value, bool):
                    self._flag_find_auto = value
            elif parameter == BeamFinderParameters.ROTATION_ENABLE:
                if isinstance(value, bool):
                    self._flag_rotation_enable = value
            elif parameter == BeamFinderParameters.DELETE_NOISE_ENABLE:
                if isinstance(value, bool):
                    self._flag_delete_noise = value
            elif parameter == BeamFinderParameters.MANUAL_ROTATION_ENABLE:
                if isinstance(value, bool):
                    self._flag_manual_rotation = value

    def get_parameter_value(self, parameter: BeamFinderParameters | str) -> object | None:
        with QMutexLocker(self._mutex):
            if parameter == BeamFinderParameters.SHAPE:
                return self._shape
            elif parameter == BeamFinderParameters.POSITION:
                return self._position
            elif parameter == BeamFinderParameters.ROTATION_ANGLE:
                return self._rotation_angle
            elif parameter == BeamFinderParameters.SCALE:
                return self._scale_factor
            elif parameter == BeamFinderParameters.NOISE_LEVEL:
                return self._noise_level
            elif parameter == BeamFinderParameters.FIND_AUTO:
                return self._flag_find_auto
            elif parameter == BeamFinderParameters.ROTATION_ENABLE:
                return self._flag_rotation_enable
            elif parameter == BeamFinderParameters.DELETE_NOISE_ENABLE:
                return self._flag_delete_noise
            elif parameter == BeamFinderParameters.MANUAL_ROTATION_ENABLE:
                return self._flag_manual_rotation
            else:
                return None

    def collect_context_for_transmission(self) -> dict:
        return {
            BeamState.ANGLE: self._rotation_angle,
            BeamState.POS: self._position,
            BeamState.SIZE: self._shape
        }

    def save_settings(self, settings: QSettings) -> None:
        settings.beginGroup("BeamFinder")
        settings.setValue("Enabled", self._flag_enable)
        settings.setValue("FindAuto", self._flag_find_auto)
        settings.setValue("EnabledRotation", self._flag_rotation_enable)
        settings.setValue("ManualRotation", self._flag_manual_rotation)
        settings.setValue("DeleteNoise", self._flag_delete_noise)
        if self._flag_delete_noise:
            settings.setValue("NoiseLevel", self._noise_level)
        if not self._flag_find_auto:
            settings.setValue("PositionX", self._position[0])
            settings.setValue("PositionY", self._position[1])
            settings.setValue("ShapeX", self._shape[0])
            settings.setValue("ShapeY", self._shape[1])
            if self._flag_manual_rotation:
                settings.setValue("Angle", self._rotation_angle)
        settings.endGroup()

    def load_settings(self, settings: QSettings) -> None:
        settings.beginGroup("BeamFinder")
        self._flag_enable = read_boolean_value(settings, "Enabled", self._flag_enable)
        self._flag_find_auto = read_boolean_value(settings, "FindAuto", self._flag_find_auto)
        self._flag_rotation_enable = read_boolean_value(settings, "EnabledRotation", self._flag_rotation_enable)
        self._flag_manual_rotation = read_boolean_value(settings, "ManualRotation", self._flag_manual_rotation)
        self._flag_delete_noise = read_boolean_value(settings, "DeleteNoise", self._flag_delete_noise)
        if self._flag_delete_noise:
            self._noise_level = settings.value("NoiseLevel", self._noise_level)
        if not self._flag_find_auto:
            pos_x = settings.value("PositionX", self._position[0])
            pos_y = settings.value("PositionX", self._position[1])
            self._position = (pos_x, pos_y)
            shape_x = settings.value("ShapeX", self._shape[0])
            shape_y = settings.value("ShapeY", self._shape[1])
            self._shape = (shape_x, shape_y)
            if self._flag_manual_rotation:
                self._rotation_angle = settings.value("Angle", self._rotation_angle)
        settings.endGroup()
