# 
# Project: laser_beam_measurements
#
# File: image_processor_sink.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import QObject, Signal, Slot, QMutex, QMutexLocker, QThread
import numpy
from .image_processor_base import ImageProcessorBase


class ImageProcessorSink(QObject):

    signal_on_new_image = Signal(numpy.ndarray)

    def __init__(self,
                 parent=None,
                 image_processor: ImageProcessorBase | None = None,
                 thread: QThread | None = None,
                 **kwargs):
        super(ImageProcessorSink, self).__init__(parent)
        self._mutex: QMutex = QMutex()
        self._processing_flag: bool = False
        self._image: numpy.ndarray | None = None
        self._image_processor: ImageProcessorBase | None = None
        if image_processor:
            self.set_image_processor(image_processor)
        if thread is not None and parent is None:
            self.moveToThread(thread)

    def set_image_processor(self, image_processor: ImageProcessorBase) -> None:
        if self._image_processor:
            self._image_processor.signal_processed_done.disconnect(self.stop_processing)
            self.signal_on_new_image.disconnect(self._image_processor.on_new_image)
        self._image_processor = image_processor
        self._image_processor.signal_processed_done.connect(self.stop_processing)
        self.signal_on_new_image.connect(self._image_processor.on_new_image)

    def is_processing(self) -> bool:
        with QMutexLocker(self._mutex):
            return self._processing_flag

    @Slot()
    def start_processing(self):
        self._set_processing_flag(True)

    @Slot()
    def stop_processing(self):
        self._set_processing_flag(False)

    def _set_processing_flag(self, value: bool) -> None:
        with QMutexLocker(self._mutex):
            self._processing_flag = value

    @Slot(numpy.ndarray)
    def slot_new_image(self, image: numpy.ndarray) -> None:
        with QMutexLocker(self._mutex):
            if not self._processing_flag:
                print(self._processing_flag)
                self._image = image
                self._processing_flag = True
                self.signal_on_new_image.emit(self._image)

    def get_image(self) -> numpy.ndarray:
        with QMutexLocker(self._mutex):
            return self._image
