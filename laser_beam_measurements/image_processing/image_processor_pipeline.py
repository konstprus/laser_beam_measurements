#
# Project: laser_beam_measurements
#
# File: image_processor_pipeline.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from .image_processor_base import ImageProcessorBase
from PySide6.QtCore import Slot, QMutexLocker
import numpy


class ImageProcessorPipeline(ImageProcessorBase):

    def __init__(self, *args, **kwargs):
        kwargs.update({"create_thread": True})
        super(ImageProcessorPipeline, self).__init__(*args, **kwargs)

        self._first_processor: ImageProcessorBase | None = None
        self._last_processor: ImageProcessorBase | None = None
        self._enable_add_processors: bool = True

    def add_processor(self, processor: ImageProcessorBase | None) -> None:
        self.blockSignals(True)
        with QMutexLocker(self._mutex):
            if not self._enable_add_processors:
                self.blockSignals(False)
                return
            if self._first_processor is None:
                self._first_processor = processor
                self._first_processor.setParent(self)
                self._first_processor.signal_processed_done.connect(self.set_processed_image)
            else:
                if self._last_processor is None:
                    self._first_processor.signal_processed_done.disconnect(self.set_processed_image)
                    self._last_processor = processor
                    self._first_processor.set_next_processor(self._last_processor)
                    self._last_processor.setParent(self)
                    self._last_processor.signal_processed_done.connect(self.set_processed_image)
                else:
                    self._last_processor.set_next_processor(processor)
                    self._last_processor.signal_processed_done.disconnect(self.set_processed_image)
                    self._last_processor = processor
                    self._last_processor.setParent(self)
                    self._last_processor.signal_processed_done.connect(self.set_processed_image)
        self.blockSignals(False)

    @Slot()
    def set_processed_image(self) -> None:
        if self._last_processor is not None:
            self._processed_image = self._last_processor.processed_image
        else:
            if self._first_processor is not None:
                self._processed_image = self._first_processor.processed_image

    def process(self, image: numpy.ndarray) -> bool | None:
        if self._first_processor is None:
            return False
        self._first_processor.on_new_image(image)
        return True

    @Slot(str, str, object)
    def set_processor_parameter_value(self, processor_name: str, parameter_name: str, value: object) -> None:
        processor = self._first_processor
        while processor is not self._last_processor:
            if type(self).__name__ == processor_name:
                processor.set_parameter_value(parameter_name, value)
            processor = processor.get_next_processor()
