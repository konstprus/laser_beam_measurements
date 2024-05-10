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


class MainObject(QObject):

    def __init__(self, parent=None):
        super(MainObject, self).__init__(parent)
        self._camera_grabber: CameraGrabber = CameraGrabber()
        self._camera_selector: CameraSelector = CameraSelector(self._camera_grabber)

        self._beam_analyzer: BeamAnalyzer = BeamAnalyzer()
        self._camera_grabber.listener.signal_new_image_received.connect(self._beam_analyzer.on_new_image)

        self._settings_name = "settings.conf"

        self._load_settings()

    @property
    def camera_grabber(self) -> CameraGrabber:
        return self._camera_grabber

    @property
    def camera_selector(self) -> CameraSelector:
        return self._camera_selector

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
