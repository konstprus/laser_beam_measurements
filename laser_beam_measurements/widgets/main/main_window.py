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
from PySide6.QtCore import Signal, Slot, Qt

from .ui_main_window import Ui_MainWindow

from laser_beam_measurements.widgets.camera_control.camera_display import CameraDisplay
from laser_beam_measurements.widgets.camera_control.camera_select_dialog import CameraSelectDialog
from laser_beam_measurements.widgets.image_processing.beam_finder_widget import BeamFinderWidget
from laser_beam_measurements.widgets.image_processing.beam_profiler_widget import BeamProfilerWidget
from laser_beam_measurements.main.main_object import MainObject
from laser_beam_measurements.camera_control.camera_listener import CameraListener
from laser_beam_measurements.camera_control.camera_listener_base import CameraState

import laser_beam_measurements.icons.rc_icons


class Icons:
    start = QIcon(u":/icons/svg/play-button.svg")
    stop = QIcon(u":/icons/svg/stop-button.svg")
    pause = QIcon(u":/icons/svg/pause-button.svg")
    camera = QIcon(u":/icons/svg/camera.svg")
    display = QIcon(u":/icons/svg/display-button.svg")


class MainWindow(QMainWindow):

    signal_camera_grabber_status = Signal(bool)
    signal_camera_close = Signal()

    def __init__(self, main_object: MainObject, parent=None):
        super().__init__(parent)
        widget = QWidget()
        self.setCentralWidget(widget)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._main_object: MainObject = main_object
        self._icons = Icons()
        self._camera_display: CameraDisplay | None = None
        self._beam_finder_widget: BeamFinderWidget | None = None
        self._beam_profiler_widget: BeamProfilerWidget | None = None

        self._set_icons()
        self._connect_signals()

    def _set_icons(self):
        self.ui.camera_section_label.setPixmap(self._icons.camera.pixmap(25, 25, QIcon.Mode.Normal, QIcon.State.On))
        self.ui.start_button.setIcon(self._icons.start)
        self.ui.stop_button.setIcon(self._icons.stop)
        self.ui.pause_button.setIcon(self._icons.pause)
        self.ui.show_display_button.setIcon(self._icons.display)

    def _connect_signals(self):
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

    @Slot(bool)
    def _slot_camera_state_changed(self, state: CameraState) -> None:
        if state == CameraState.STARTED:
            self.ui.start_button.setEnabled(False)
            self.ui.pause_button.setEnabled(True)
            self.ui.stop_button.setEnabled(True)

            self.ui.statusbar.showMessage("Active", -1)

            if self._camera_display is None:
                self._camera_display = CameraDisplay(self)
                self._main_object.set_display(self._camera_display)
                self._camera_display.setWindowIcon(self._icons.display)
                self._create_sub_window(self._camera_display, True)

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
    def start_button_clicked(self):
        if not self._main_object.camera_grabber.is_camera_opened:
            self._show_camera_select_dialog()
        self.signal_camera_grabber_status.emit(True)

    @Slot()
    def stop_button_clicked(self):
        self.signal_camera_close.emit()

    @Slot()
    def pause_button_clicked(self):
        self.signal_camera_grabber_status.emit(False)

    @Slot()
    def show_camera_display(self):
        if self._camera_display is None:
            self._camera_display = CameraDisplay(self)
            self._main_object.set_display(self._camera_display)
            self._camera_display.setWindowIcon(self._icons.display)
        sub = self._create_sub_window(self._camera_display, False)
        if sub.isHidden():
            sub.show()
        else:
            sub.setHidden(True)

    @Slot()
    def show_beam_finder_widget(self):
        if self._beam_finder_widget is None:
            self._beam_finder_widget = BeamFinderWidget(self)
            self._main_object.set_widget_for_beam_finder(self._beam_finder_widget)
        sub = self._create_sub_window(self._beam_finder_widget, False)
        if sub.isHidden():
            sub.show()
        else:
            sub.setHidden(True)

    @Slot()
    def show_beam_profiler_widget(self):
        if self._beam_profiler_widget is None:
            self._beam_profiler_widget = BeamProfilerWidget(self)
            self._main_object.set_widget_for_beam_profiler(self._beam_profiler_widget)
        sub = self._create_sub_window(self._beam_profiler_widget, False)
        if sub.isHidden():
            sub.show()
        else:
            sub.setHidden(True)

    def _show_camera_select_dialog(self):
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
        self.ui.mdiArea.addSubWindow(sub)
        if show:
            sub.show()
        return sub
