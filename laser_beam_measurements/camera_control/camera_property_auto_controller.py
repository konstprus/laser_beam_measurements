# 
# Project: laser_beam_measurements
#
# File: camera_property_auto_controller.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import QObject, Signal, Slot, Qt
from enum import Enum
import numpy
from .camera_property_controller import CameraPropertyController
from typing import Optional, Union, List, Tuple


class ControllerStatus(Enum):
    STATUS_NONE = -1
    STATUS_OK = 0
    STATUS_NOT_OK = 1
    STATUS_HIGH = 2
    STATUS_LOW = 3
    STATUS_RUNNING = 4
    STATUS_BAD_LOW = 5
    STATUS_BAD_HIGH = 7


class ParameterBaseChecker:

    def check(self, *args, **kwargs) -> ControllerStatus:
        return ControllerStatus.STATUS_OK


class ParameterIntRangeChecker(ParameterBaseChecker):

    def __init__(self):
        self._min: int = 0
        self._max: int = 1

    @property
    def range(self) -> type[int, int]:
        return self._min, self._max

    @range.setter
    def range(self, range_t: tuple | list) -> None:
        self._min = range_t[0]
        self._max = range_t[1]

    def check(self, value: int, *args, **kwargs) -> ControllerStatus:
        if value < self._min:
            return ControllerStatus.STATUS_LOW
        if value > self._max:
            return ControllerStatus.STATUS_HIGH
        return ControllerStatus.STATUS_OK


class NumpyImageBaseChecker(ParameterIntRangeChecker):

    def _array_to_scalar(self, img: numpy.ndarray) -> int:
        raise NotImplementedError()

    def check(self, img: numpy.ndarray, *args, **kwargs) -> ControllerStatus:
        value = self._array_to_scalar(img)
        return super().check(value, *args, **kwargs)


class NumpyImageMaxPixelChecker(NumpyImageBaseChecker):

    def _array_to_scalar(self, img: numpy.ndarray) -> int:
        if img.size == 0:
            return 0
        return numpy.max(img)


Parameter = Union[int, float]
ParameterRange = Tuple[Parameter, Parameter]


class RangeAnalyzer:

    def __init__(self):
        self._number_of_ranges: int = 6
        self._control_points: List[Parameter] = list()
        self._current_range: Optional[Tuple] = None
        self._range_found: bool = False
        self._starting_bound_indexes: Optional[tuple] = None
        self._right_candidate: Optional[Parameter] = None
        self._left_candidate: Optional[Parameter] = None
        self._candidate: Optional[Parameter] = None

    @property
    def current_range(self) -> Optional[Tuple]:
        return self._current_range

    def init_analyzer(self, property_range: ParameterRange, property_value: Parameter) -> None:
        self._fill_ranges(property_range)
        self._find_starting_range(property_value)
        self._left_candidate = None
        self._right_candidate = None
        self._candidate = None
        self._range_found = False

    def _fill_ranges(self, property_range: ParameterRange) -> None:
        self._control_points.clear()
        self._control_points = numpy.linspace(property_range[0], property_range[1], self._number_of_ranges, True).tolist()

    def _find_starting_range(self, property_value: Parameter) -> None:
        for i in range(self._number_of_ranges - 1):
            if self._control_points[i] <= property_value <= self._control_points[i+1]:
                self._starting_bound_indexes = (i, i+1)
                return
        self._starting_bound_indexes = (self._number_of_ranges - 2, self._number_of_ranges - 1)

    @property
    def candidate(self) -> Optional[Parameter]:
        return self._candidate

    def find_range(self, property_value: Parameter, status: ControllerStatus) -> bool:
        if self._left_candidate and self._right_candidate:
            self._current_range = (self._left_candidate, self._right_candidate)
            self._range_found = True
            return True
        i0, i1 = self._starting_bound_indexes
        if status == ControllerStatus.STATUS_OK:
            self._range_found = True
            self._current_range = (self._control_points[i0], self._control_points[i1])

        elif status == ControllerStatus.STATUS_LOW:
            self._left_candidate = property_value
            self._candidate = self._control_points[i1]
            if i1 == self._number_of_ranges - 1:
                self._current_range = (self._left_candidate, self._candidate)
                self._range_found = True
            self._starting_bound_indexes = (i1, i1 + 1)

        elif status == ControllerStatus.STATUS_HIGH:
            self._right_candidate = property_value
            # self._left_candidate = self._control_points[i0]
            self._candidate = self._control_points[i0]
            if i0 == 0:
                self._current_range = (self.candidate, self._right_candidate)
                self._range_found = True
            self._starting_bound_indexes = (i0 - 1, i0)
        return self._range_found


class CameraPropertyAutoController(QObject):

    signal_check_result = Signal(ControllerStatus)

    def __init__(self, parent=None, controller: CameraPropertyController | None=None):
        super(CameraPropertyAutoController, self).__init__(parent)
        self._checker: NumpyImageBaseChecker | None = NumpyImageMaxPixelChecker()
        self._range_analyzer: RangeAnalyzer = RangeAnalyzer()
        self._controller: CameraPropertyController | None = controller
        self._flag_active: bool = True
        self._flag_control_on: bool = False
        self._flag_control_always: bool = False
        self._flag_bad_signal: bool = False
        self._property_name: str = "exposure"
        self._checker.range = (190, 240)
        self._current_bounds: list = list()
        self._step = 1e-1
        self._prop_range: tuple = (0.0, 1.0)
        self._counter: int = 0
        self._max_counter: int = 3
        self._number_of_steps_for_small_range: int = 10
        self._range_analyzer_available: bool = True

    def set_controller(self, controller: CameraPropertyController) -> None:
        self._controller = controller

    def set_active(self, value: bool) -> None:
        self._flag_active = value
        if not self._flag_active:
            self.signal_check_result.emit(ControllerStatus.STATUS_NONE)

    @Slot()
    def slot_control_change(self) -> None:
        if self._flag_control_on:
            self.stop_control()
        else:
            self.start_control()

    @Slot(bool)
    @Slot(Qt.CheckState)
    def set_control_always(self, value: bool | Qt.CheckState) -> None:
        if not self._flag_active:
            return
        if isinstance(value, Qt.CheckState):
            if value == Qt.CheckState.Checked:
                value = True
            else:
                value = False
        self._flag_control_always = value
        if self._flag_control_always and not self._flag_control_on:
            self.start_control()

    @Slot()
    def slot_control_always_change(self) -> None:
        self.set_control_always(not self._flag_control_always)

    def check_image(self, img: numpy.ndarray) -> None:
        if not self._flag_active:
            return
        check_result = ControllerStatus.STATUS_NONE
        if self._checker:
            check_result = self._checker.check(img)
        if self._flag_control_on:
            result = self._correct(check_result)
            if result:
                # if check_result != ControllerStatus.STATUS_OK:
                #     self._flag_bad_signal = True
                #     check_result = self._specify_status(check_result)
                self._flag_control_on = False
            else:
                check_result = ControllerStatus.STATUS_RUNNING
        else:
            if self._flag_control_always:
                result = self._small_correct(check_result)
                if not result:
                    check_result = ControllerStatus.STATUS_RUNNING
        self.signal_check_result.emit(check_result)

    def _check_counter(self):
        if self._counter > self._max_counter:
            self._counter = 0
            return True
        else:
            self._counter += 1
            return False

    def _specify_status(self, check_result: ControllerStatus) -> ControllerStatus:
        if self._flag_bad_signal:
            if check_result == ControllerStatus.STATUS_LOW:
                check_result = ControllerStatus.STATUS_BAD_LOW
            elif check_result == ControllerStatus.STATUS_HIGH:
                check_result = ControllerStatus.STATUS_BAD_HIGH
        return check_result

    def set_range(self, min_value: int, max_value: int) -> None:
        self._checker.range = (min_value, max_value)

    def _small_correct(self, check_result: ControllerStatus) -> bool:
        value = self._controller.get_property_value(self._property_name)
        if abs(value - self._prop_range[0]) < self._step or abs(value - self._prop_range[1]) < self._step:
            return True
        if check_result == ControllerStatus.STATUS_OK:
            return True
        if check_result == ControllerStatus.STATUS_LOW:
            self._controller.set_property_value(self._property_name, value+self._step)
        elif check_result == ControllerStatus.STATUS_HIGH:
            self._controller.set_property_value(self._property_name, value-self._step)
        return False


    def _correct(self, check_result: ControllerStatus) -> bool:
        value = self._controller.get_property_value(self._property_name)
        if self._range_analyzer_available and (self._current_bounds is None or len(self._current_bounds) == 0):
            range_found = self._range_analyzer.find_range(value, check_result)
            if range_found:
                self._current_bounds = list(self._range_analyzer.current_range)
                self._controller.set_property_value(self._property_name, sum(self._current_bounds)/2.0)
            else:
                self._controller.set_property_value(self._property_name, self._range_analyzer.candidate)
            return False
        if abs(self._current_bounds[1] - self._current_bounds[0]) < self._number_of_steps_for_small_range*self._step:
            result = self._small_correct(check_result)
            if result:
                return self._check_counter()
            else:
                return False
        if check_result == ControllerStatus.STATUS_OK:
            return self._check_counter()
        elif check_result == ControllerStatus.STATUS_LOW:
            if value > self._current_bounds[1]:
                return self._check_counter()
            else:
                self._current_bounds[0] = value
        elif check_result == ControllerStatus.STATUS_HIGH:
            if value < self._current_bounds[0]:
                return self._check_counter()
            else:
                self._current_bounds[1] = value
        self._counter = 0
        self._controller.set_property_value(self._property_name, sum(self._current_bounds)/2)
        return False

    @Slot()
    def change_state(self) -> None:
        if self._flag_active:
            self.stop_control()
        else:
            self.start_control()

    @Slot()
    def start_control(self) -> None:
        if not self._flag_active:
            return
        prop = self._controller.get_property(self._property_name)
        self._prop_range = tuple(prop.range)
        if self._range_analyzer_available:
            self._current_bounds = None
            self._range_analyzer.init_analyzer(prop.range, prop.value)
        else:
            self._current_bounds = list(prop.range)
        self._step = float(prop.step)
        self._flag_bad_signal = False
        self._flag_control_on = True

    @Slot()
    def stop_control(self) -> None:
        self._flag_control_on = False
        self._counter = 0

    @property
    def available(self) -> bool:
        if self._controller is None:
            return False
        if self._controller.available:
            if self._controller.has_property(self._property_name):
                return self._controller.get_property(self._property_name).available
            return False
        return False
