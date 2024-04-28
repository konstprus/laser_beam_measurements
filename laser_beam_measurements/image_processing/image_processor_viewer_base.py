#
# Project: laser_beam_measurements
#
# File: image_processor_viewer_base.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QWidget
from .image_processor_base import ImageProcessorBase
from laser_beam_measurements.widgets.utils.custom_graphics_scene import CustomGraphicsScene
from laser_beam_measurements.utils.colormap import COLORMAPS
import numpy


class ImageProcessorViewerBase(QWidget):

    signal_parameter_changed = Signal(str, object)
    signal_enable_changed = Signal(bool)

    def __init__(self, parent=None, **kwargs):
        super(ImageProcessorViewerBase, self).__init__(parent)
        self._image_processor: ImageProcessorBase | None = None
        self._flag_show_input_image: bool = False
        self._flag_show_processed_image: bool = False
        self._input_image_scene: CustomGraphicsScene | None = None
        self._output_image_scene: CustomGraphicsScene | None = None

        configure_input_scene = kwargs.get("configure_input_scene", False)
        if configure_input_scene:
            self._input_image_scene = CustomGraphicsScene(self)
            self._flag_show_input_image = True

        configure_output_scene = kwargs.get("configure_output_scene", False)
        if configure_output_scene:
            self._output_image_scene = CustomGraphicsScene(self)
            self._flag_show_processed_image = True

    def set_image_processor(self, image_processor: ImageProcessorBase) -> None:
        if self._image_processor:
            self._disconnect_processor_signal()
        self._image_processor = image_processor
        self._connect_processor_signal()
        self._update_parameters()

    def _update_parameters(self) -> None:
        raise NotImplementedError()

    def _connect_processor_signal(self):
        self.signal_enable_changed.connect(self._image_processor.set_enable)
        self.signal_parameter_changed.connect(self._image_processor.set_parameter_value)
        if self._flag_show_input_image:
            self._image_processor.signal_input_image.connect(self.slot_show_input_image)
        if self._flag_show_processed_image:
            self._image_processor.signal_processed_image.connect(self.slot_show_processed_image)

    def _disconnect_processor_signal(self):
        self.signal_enable_changed.disconnect(self._image_processor.set_enable)
        self.signal_parameter_changed.disconnect(self._image_processor.set_parameter_value)
        if self._flag_show_input_image:
            self._image_processor.signal_input_image.disconnect(self.slot_show_input_image)
        if self._flag_show_processed_image:
            self._image_processor.signal_processed_image.disconnect(self.slot_show_processed_image)

    @Slot(numpy.ndarray)
    def slot_show_input_image(self, input_image: numpy.ndarray) -> None:
        if self._flag_show_input_image:
            self._slot_show_input_image(input_image)

    def _slot_show_input_image(self, input_image: numpy.ndarray) -> None:
        # raise NotImplementedError()
        if self._input_image_scene is not None:
            self._input_image_scene.update_image(input_image)

    @Slot(numpy.ndarray)
    def slot_show_processed_image(self, input_image: numpy.ndarray) -> None:
        if self._flag_show_processed_image:
            self._slot_show_processed_image(input_image)

    def _slot_show_processed_image(self, input_image: numpy.ndarray) -> None:
        # raise NotImplementedError()
        if self._output_image_scene is not None:
            self._output_image_scene.update_image(input_image)

    @Slot(str)
    def slot_set_colormap_for_input(self, name: str) -> None:
        if self._input_image_scene is not None:
            self._input_image_scene.set_colormap(COLORMAPS.get_colormap(name))

    @Slot(str)
    def slot_set_colormap_for_output(self, name: str) -> None:
        if self._output_image_scene is not None:
            self._output_image_scene.set_colormap(COLORMAPS.get_colormap(name))

    # @Slot(str, object)
    # def set_parameter_value(self, parameter_name: str, value: object) -> None:
    #     pass
    #
    # def _set_parameter_value(self, parameter_name: str, value: object) -> None:
