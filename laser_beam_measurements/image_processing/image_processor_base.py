#
# Project: laser_beam_measurements
#
# File: image_processor_base.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import QObject, Signal, Slot, QThread, QMutex, QMutexLocker, QSettings
import numpy


class ImageProcessorBase(QObject):
    signal_processed_done = Signal()
    signal_input_image = Signal(numpy.ndarray)
    signal_processed_image = Signal(numpy.ndarray)

    def __init__(self, parent=None, **kwargs):
        super(ImageProcessorBase, self).__init__(parent)
        self._thread: QThread | None = kwargs.get("thread", None)
        self._mutex: QMutex = kwargs.get("mutex", QMutex())
        self._own_thread: bool = False
        self._name: str = kwargs.get("name", type(self).__name__)
        self._next_processor: ImageProcessorBase | None = None
        self._processed_image: numpy.ndarray | None = None
        self._flag_enable: bool = True
        self._flag_transmit_context: bool = False
        self._extra_context: dict = {}
        create_thread = kwargs.get("create_thread", False)
        if self._thread is None and create_thread:
            self._thread = QThread()
            self._own_thread = True
            self.moveToThread(self._thread)
            if not self._thread.isRunning():
                self._thread.start()

    # def __del__(self):
    #     if self._own_thread:
    #         self._thread.quit()
    #         # self._thread.msleep(1000)
    #         self._thread.wait(10000)
    #         self._thread.deleteLater()

    def set_next_processor(self, processor: QObject | None) -> None:
        with QMutexLocker(self._mutex):
            if processor is None:
                return
            parent = self.parent()
            processor_parent = processor.parent()
            if parent is processor_parent and isinstance(processor, ImageProcessorBase):
                self._next_processor = processor

    def get_next_processor(self) -> QObject | None:
        with QMutexLocker(self._mutex):
            return self._next_processor

    def process(self, image: numpy.ndarray) -> bool | None:
        raise NotImplementedError()

    @property
    def name(self):
        return self._name

    @property
    def processed_image(self) -> numpy.ndarray | None:
        with QMutexLocker(self._mutex):
            return self._processed_image

    @Slot(bool)
    def set_enable(self, flag: bool) -> None:
        with QMutexLocker(self._mutex):
            self._flag_enable = flag

    @property
    def enabled(self) -> bool:
        with QMutexLocker(self._mutex):
            return self._flag_enable

    @Slot(numpy.ndarray)
    def on_new_image(self, image: numpy.ndarray) -> None:
        if self._flag_enable:
            self.signal_input_image.emit(image)
            if self.process(image):
                self.signal_processed_done.emit()
                if self._processed_image is not None:
                    self.signal_processed_image.emit(self._processed_image)
                    if self._next_processor is not None:
                        if self._flag_transmit_context:
                            extra_context = self.collect_context_for_transmission()
                            self._next_processor.set_extra_context(**extra_context)
                        self._next_processor.on_new_image(self._processed_image)

    def set_extra_context(self, **kwargs) -> None:
        self._extra_context.update(kwargs)

    def collect_context_for_transmission(self) -> dict:
        return dict()

    @Slot(str, object)
    def set_parameter_value(self, parameter: str, value: object) -> None:
        self._set_parameter_value(parameter, value)

    def _set_parameter_value(self, parameter: str, value: object) -> None:
        pass

    def get_parameter_value(self, parameter: str) -> object | None:
        return None

    def save_settings(self, settings: QSettings) -> None:
        pass

    def load_settings(self, settings: QSettings) -> None:
        pass

    def stop_thread(self) -> None:
        if self._own_thread:
            self._thread.quit()
            self._thread.wait(1000)
