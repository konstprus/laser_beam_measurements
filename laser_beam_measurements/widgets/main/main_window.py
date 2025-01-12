# 
# Project: laser_beam_measurements
#
# File: main_window.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

# pyside6-uic laser_beam_measurements/widgets/main/main_window.ui -o laser_beam_measurements/widgets/main/ui_main_window.py

from PySide6.QtWidgets import QMainWindow, QWidget, QMdiSubWindow
from PySide6.QtGui import QIcon
from PySide6.QtCore import Signal, Slot, QSettings

from .ui_main_window import Ui_MainWindow

from laser_beam_measurements.widgets.camera_control.camera_display import CameraDisplay
from laser_beam_measurements.widgets.camera_control.camera_select_dialog import CameraSelectDialog
from laser_beam_measurements.widgets.camera_control.camera_property_controller_widget import (
    CameraPropertyControllerWidget)
from laser_beam_measurements.widgets.image_processing.beam_finder_widget import BeamFinderWidget
from laser_beam_measurements.widgets.image_processing.beam_profiler_widget import BeamProfilerWidget
from laser_beam_measurements.main.main_object import MainObject
from laser_beam_measurements.camera_control.camera_listener import CameraListener
from laser_beam_measurements.camera_control.camera_listener_base import CameraState
from laser_beam_measurements.utils.settings_bool_reader import read_boolean_value

from laser_beam_measurements.icons import Icon


class Icons:
    start = Icon("play.svg")
    stop = Icon("stop.svg")
    pause = Icon("pause.svg")
    camera = Icon("camera.svg")
    display = Icon("display.svg")
    save = Icon("save.svg")
    settings = Icon("settings.svg")
    beam_find = Icon("beam_find.svg")
    beam_analyze = Icon("beam_analyze.svg")
    beam_profiler = Icon("beam_profiler.svg")
    main = Icon("main.svg")


class MainWindow(QMainWindow):

    signal_camera_grabber_status = Signal(bool)
    signal_camera_close = Signal()

    def __init__(self, main_object: MainObject, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Laser Beam Measurements")

        self._main_object: MainObject = main_object
        self._icons = Icons()
        self._camera_display: CameraDisplay | None = None
        self._beam_finder_widget: BeamFinderWidget | None = None
        self._beam_profiler_widget: BeamProfilerWidget | None = None
        self._property_controller_widget: CameraPropertyControllerWidget | None = None

        self._set_icons()
        self._connect_signals()

        self._load_settings()

    def _set_icons(self) -> None:
        self.ui.camera_section_label.setPixmap(self._icons.camera.pixmap(25, 25, QIcon.Mode.Normal, QIcon.State.On))
        self.ui.start_button.setIcon(self._icons.start)
        self.ui.stop_button.setIcon(self._icons.stop)
        self.ui.pause_button.setIcon(self._icons.pause)
        self.ui.show_display_button.setIcon(self._icons.display)
        self.ui.show_settings_button.setIcon(self._icons.settings)
        self.ui.save_image_button.setIcon(self._icons.save)
        self.ui.save_processed_image_button.setIcon(self._icons.save)
        self.ui.show_beam_finder.setIcon(self._icons.beam_find)
        self.ui.show_beam_profiler.setIcon(self._icons.beam_profiler)
        self.ui.beam_analyzing_section_label.setPixmap(
            self._icons.beam_analyze.pixmap(25, 25, QIcon.Mode.Normal, QIcon.State.On))
        self.setWindowIcon(self._icons.main)

    def _connect_signals(self) -> None:
        self.signal_camera_grabber_status.connect(self._main_object.camera_grabber.run_status_changed)
        self.signal_camera_close.connect(self._main_object.camera_grabber.close)
        listener = self._main_object.camera_grabber.listener
        if isinstance(listener, CameraListener):
            listener.signal_camera_state_changed.connect(self._slot_camera_state_changed)

        self.ui.start_button.clicked.connect(self.start_button_clicked)
        self.ui.stop_button.clicked.connect(self.stop_button_clicked)
        self.ui.pause_button.clicked.connect(self.pause_button_clicked)
        self.ui.show_display_button.clicked.connect(self.show_camera_display)
        self.ui.show_beam_finder.clicked.connect(self.show_beam_finder_widget)
        self.ui.show_beam_profiler.clicked.connect(self.show_beam_profiler_widget)
        self.ui.show_settings_button.clicked.connect(self.show_property_controller_widget)

    @Slot(bool)
    def _slot_camera_state_changed(self, state: CameraState) -> None:
        if state == CameraState.STARTED:
            self.ui.start_button.setEnabled(False)
            self.ui.pause_button.setEnabled(True)
            self.ui.stop_button.setEnabled(True)

            self.ui.statusbar.showMessage("Active", -1)

            if self._camera_display is None:
                sub = self._create_camera_display_sub_window()
                sub.show()

            if self._property_controller_widget is None:
                sub = self._create_property_controller_widget_sub_window()
                sub.setHidden(True)
        elif state == CameraState.STOPPED:
            self.ui.start_button.setEnabled(True)
            self.ui.pause_button.setEnabled(False)
            self.ui.stop_button.setEnabled(True)

            self.ui.statusbar.showMessage("Paused", -1)

        elif state == CameraState.CLOSED:
            self.ui.start_button.setEnabled(True)
            self.ui.pause_button.setEnabled(False)
            self.ui.stop_button.setEnabled(False)

            self.ui.statusbar.showMessage("Stopped", -1)

    @Slot()
    def start_button_clicked(self) -> None:
        if not self._main_object.camera_grabber.is_camera_opened:
            self._show_camera_select_dialog()
        self.signal_camera_grabber_status.emit(True)

    @Slot()
    def stop_button_clicked(self) -> None:
        self.signal_camera_close.emit()

    @Slot()
    def pause_button_clicked(self) -> None:
        self.signal_camera_grabber_status.emit(False)

    @Slot()
    def show_camera_display(self) -> None:
        sub = self._create_camera_display_sub_window()
        self._show_sub_window(sub)

    def _create_camera_display_sub_window(self) -> QMdiSubWindow:
        if self._camera_display is None:
            self._camera_display = CameraDisplay(self)
            self.ui.save_image_button.clicked.connect(self._camera_display.save)
            self._main_object.set_display(self._camera_display)
            self._camera_display.setWindowIcon(self._icons.display)
        return self._create_sub_window(self._camera_display, False)

    @Slot()
    def show_beam_finder_widget(self) -> None:
        sub = self._create_beam_finder_widget_sub_window()
        self._show_sub_window(sub)

    def _create_beam_finder_widget_sub_window(self) -> QMdiSubWindow:
        if self._beam_finder_widget is None:
            self._beam_finder_widget = BeamFinderWidget(self)
            self._main_object.set_widget_for_beam_finder(self._beam_finder_widget)
            self._beam_finder_widget.setWindowIcon(self._icons.beam_find)
        return self._create_sub_window(self._beam_finder_widget, False)

    @Slot()
    def show_beam_profiler_widget(self) -> None:
        sub = self._create_beam_profiler_widget_sub_window()
        self._show_sub_window(sub)

    def _create_beam_profiler_widget_sub_window(self) -> QMdiSubWindow:
        if self._beam_profiler_widget is None:
            self._beam_profiler_widget = BeamProfilerWidget(self)
            self.ui.save_processed_image_button.clicked.connect(self._beam_profiler_widget.slot_save_save_output_image)
            self._main_object.set_widget_for_beam_profiler(self._beam_profiler_widget)
            self._beam_profiler_widget.setWindowIcon(self._icons.beam_profiler)
        return self._create_sub_window(self._beam_profiler_widget, False)

    @Slot()
    def show_property_controller_widget(self) -> None:
        sub = self._create_property_controller_widget_sub_window()
        self._show_sub_window(sub)

    def _create_property_controller_widget_sub_window(self) -> QMdiSubWindow:
        if self._property_controller_widget is None:
            self._property_controller_widget = CameraPropertyControllerWidget(self)
            self._main_object.set_widget_for_property_controller(self._property_controller_widget)
            self._main_object.set_widget_for_camera_control_status(self._property_controller_widget)
            self._property_controller_widget.setWindowIcon(self._icons.settings)
        return self._create_sub_window(self._property_controller_widget, False)

    def _show_camera_select_dialog(self) -> None:
        camera_select_dialog = CameraSelectDialog(self)
        camera_select_dialog.set_selector(self._main_object.camera_selector)
        camera_select_dialog.exec()

    def _create_sub_window(self, widget: QWidget, show: bool = True) -> QMdiSubWindow:
        sub_windows = self.ui.mdiArea.subWindowList()
        for sub in sub_windows:
            if sub.widget() == widget:
                return sub
        sub = QMdiSubWindow()
        sub.setWidget(widget)
        sub.setObjectName(widget.objectName())
        sub.setWindowIcon(widget.windowIcon())
        sub.setWindowTitle(widget.windowTitle())
        sub.resize(widget.size())
        self.ui.mdiArea.addSubWindow(sub)
        if show:
            sub.show()
        return sub

    def _show_sub_window(self, sub_window: QMdiSubWindow) -> None:
        if sub_window.isHidden() and sub_window.widget() is not None:
            sub_window.show()
            sub_window.widget().show()
        else:
            sub_window.setHidden(True)

    def closeEvent(self, event) -> None:
        self._main_object.closeEvent(event)
        self.save_settings(self._main_object.settings_file)
        super().closeEvent(event)

    def _save_widget_settings(self, widget: QWidget, settings: QSettings, group_name: str) -> None:
        if widget is None:
            return
        sub_window = self._create_sub_window(widget, False)
        settings.beginGroup(group_name)
        settings.setValue("IsHidden", sub_window.isHidden())
        pos = sub_window.pos()
        settings.setValue("PosX", pos.x())
        settings.setValue("PosY", pos.y())
        size = sub_window.size()
        settings.setValue("Width", size.width())
        settings.setValue("Height", size.height())
        if hasattr(widget, "save_widget_settings"):
            widget.save_widget_settings(settings)
        settings.endGroup()

    def save_settings(self, settings: QSettings) -> None:
        settings.beginGroup("MainWindow")
        if self.isMaximized():
            settings.setValue("IsMaximized", True)
        else:
            pos = self.pos()
            settings.setValue("PosX", pos.x())
            settings.setValue("PosY", pos.y())
            size = self.size()
            settings.setValue("Width", size.width())
            settings.setValue("Height", size.height())
        settings.endGroup()
        self._save_widget_settings(self._camera_display, settings, "CameraDisplayWidget")
        self._save_widget_settings(self._beam_finder_widget, settings, "BeamFinderWidget")
        self._save_widget_settings(self._beam_profiler_widget, settings, "BeamProfilerWidget")
        self._save_widget_settings(self._property_controller_widget, settings, "PropertyControllerWidget")

    def _load_setting_for_sub_window(self, sub_window: QMdiSubWindow, settings: QSettings) -> None:
        if settings.contains("IsHidden"):
            is_hidden = read_boolean_value(settings, "IsHidden", sub_window.isHidden())
            if not is_hidden:
                sub_window.show()
        if settings.contains("PosX") and settings.contains("PosY"):
            pos_x = int(settings.value("PosX"))
            pos_y = int(settings.value("PosY"))
            sub_window.move(pos_x, pos_y)
        if settings.contains("Width") and settings.contains("Height"):
            width = int(settings.value("Width"))
            height = int(settings.value("Height"))
            sub_window.resize(width, height)
        widget = sub_window.widget()
        if hasattr(widget, "load_widget_settings"):
            widget.load_widget_settings(settings)

    def _load_settings(self):
        settings = self._main_object.settings_file
        child_groups = settings.childGroups()
        for group in child_groups:
            if group == "MainWindow":
                settings.beginGroup(group)
                is_maximized = read_boolean_value(settings, "IsMaximized", False)
                if is_maximized:
                    self.showMaximized()
                else:
                    if settings.contains("PosX") and settings.contains("PosY"):
                        pos_x = int(settings.value("PosX"))
                        pos_y = int(settings.value("PosY"))
                        self.move(pos_x, pos_y)
                    if settings.contains("Width") and settings.contains("Height"):
                        width = int(settings.value("Width"))
                        height = int(settings.value("Height"))
                        self.resize(width, height)
                settings.endGroup()

            if group == "CameraDisplayWidget":
                settings.beginGroup(group)
                sub = self._create_camera_display_sub_window()
                self._load_setting_for_sub_window(sub, settings)
                settings.endGroup()

            if group == "BeamFinderWidget":
                settings.beginGroup(group)
                sub = self._create_beam_finder_widget_sub_window()
                self._load_setting_for_sub_window(sub, settings)
                settings.endGroup()

            if group == "BeamProfilerWidget":
                settings.beginGroup(group)
                sub = self._create_beam_profiler_widget_sub_window()
                self._load_setting_for_sub_window(sub, settings)
                settings.endGroup()

            if group == "PropertyControllerWidget":
                settings.beginGroup(group)
                sub = self._create_property_controller_widget_sub_window()
                self._load_setting_for_sub_window(sub, settings)
                settings.endGroup()
