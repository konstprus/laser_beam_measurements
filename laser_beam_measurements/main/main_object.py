# 
# Project: laser_beam_measurements
#
# File: main_object.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtCore import QObject, QSettings
from PySide6.QtWidgets import QWidget
from laser_beam_measurements.camera_control.camera_grabber import CameraGrabber
from laser_beam_measurements.camera_control.camera_selector import CameraSelector
from laser_beam_measurements.image_processing.beam_analyzer import BeamAnalyzer
from laser_beam_measurements.image_processing.image_processor_sink import ImageProcessorSink
from laser_beam_measurements.image_processing.parameter_logger import ParameterLogger


class MainObject(QObject):

    def __init__(self, parent=None):
        super(MainObject, self).__init__(parent)
        self._camera_grabber: CameraGrabber = CameraGrabber()
        self._camera_selector: CameraSelector = CameraSelector(self._camera_grabber)

        self._beam_analyzer: BeamAnalyzer = BeamAnalyzer()
        self._sink = ImageProcessorSink(image_processor=self._beam_analyzer, thread=self._camera_grabber.thread())
        # self._camera_grabber.listener.signal_new_image_received.connect(self._beam_analyzer.on_new_image)
        self._camera_grabber.listener.signal_new_image_received.connect(self._sink.slot_new_image)
        self._camera_selector.signal_camera_selected.connect(self._beam_analyzer.slot_set_init_parameters)

        self._logger = ParameterLogger()
        self._beam_analyzer.beam_profiler.parameter_logger = self._logger

        self._settings_name = "settings.conf"

        self._load_settings()

    @property
    def camera_grabber(self) -> CameraGrabber:
        return self._camera_grabber

    @property
    def camera_selector(self) -> CameraSelector:
        return self._camera_selector

    @property
    def settings_file(self) -> QSettings:
        settings = QSettings(self._settings_name, QSettings.Format.IniFormat)
        return settings

    def set_display(self, display_widget: QWidget) -> bool:
        if hasattr(display_widget, "set_camera_listener"):
            display_widget.set_camera_listener(self._camera_grabber.listener)
            return True
        return False

    def set_widget_for_beam_finder(self, widget: QWidget) -> bool:
        if hasattr(widget, "set_image_processor"):
            widget.set_image_processor(self._beam_analyzer.beam_finder)
            return True
        return False

    def set_widget_for_beam_profiler(self, widget: QWidget) -> bool:
        if hasattr(widget, "set_image_processor"):
            widget.set_image_processor(self._beam_analyzer.beam_profiler)
            return True
        return False

    def set_widget_for_property_controller(self, widget: QWidget) -> bool:
        if hasattr(widget, "set_controller"):
            widget.set_controller(self._camera_grabber.property_controller)
            return True
        return False

    def set_widget_for_camera_control_status(self, widget: QWidget) -> bool:
        if hasattr(widget, "set_auto_controller"):
            widget.set_auto_controller(self._camera_grabber.auto_controller)
            return True
        return False

    def set_widget_for_parameter_logger(self, widget: QWidget) -> bool:
        if hasattr(widget, "set_logger"):
            widget.set_logger(self._logger)
            return True
        return False

    def closeEvent(self, event) -> None:
        self._camera_grabber.run_status_changed(False)
        self._save_settings()
        self._camera_grabber.stop_thread()
        self._beam_analyzer.stop_thread()

    def _save_settings(self):
        settings = QSettings(self._settings_name, QSettings.Format.IniFormat)
        settings.clear()
        self._camera_selector.save_settings(settings)
        self._beam_analyzer.save_settings(settings)

    def _load_settings(self):
        settings = QSettings(self._settings_name, QSettings.Format.IniFormat)
        self._camera_selector.load_settings(settings)
        self._beam_analyzer.load_settings(settings)
