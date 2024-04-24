# 
# Project: laser_beam_measurements
#
# File: camera_grabber.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtCore import QObject, QThread, QMutex, QMutexLocker, QCoreApplication, Slot, Signal

from .camera_listener_base import CameraListenerBase
from .camera_listener import CameraListener
from .camera_base import CameraBase
from .camera_property_controller import CameraPropertyController

__all__ = ["CameraGrabber"]


class CameraGrabber(QObject):

    # signal_property_changed = Signal(str, object)

    def __init__(self, parent=None, **kwargs):
        super(CameraGrabber, self).__init__(parent)
        self._camera: CameraBase | None = None
        self._listener: CameraListenerBase | None = kwargs.get("listener", CameraListener(self))
        self._own_thread: bool = False
        self._thread: QThread | None = kwargs.get("thread", None)
        self._mutex: QMutex = kwargs.get("mutex", QMutex())
        self._timer_interval: int = 30
        self._timer_id: int = -1

        self._update_fps: bool = False
        self._auto_grabbing_enabled: bool = True
        self._property_controller: CameraPropertyController = CameraPropertyController(self)

        if self._thread is None:
            self._thread = QThread()
            self._own_thread = True
        self.moveToThread(self._thread)
        if not self._thread.isRunning():
            self._thread.start()

    def __del__(self):
        self.stop()
        if self._camera:
            self._camera.close()
        if self._own_thread:
            self._thread.quit()
            # self._thread.msleep(1000)
            self._thread.wait(10000)
            del self._thread

    def set_camera(self, camera: CameraBase) -> None:
        with QMutexLocker(self._mutex):
            self._camera = camera
            self._property_controller.set_camera(self._camera)
            if self._listener is not None:
                self._listener.reset()

    @property
    def auto_grabbing_enabled(self) -> bool:
        with QMutexLocker(self._mutex):
            return self._auto_grabbing_enabled

    @property
    def listener(self) -> CameraListenerBase | None:
        with QMutexLocker(self._mutex):
            return self._listener

    @listener.setter
    def listener(self, listener: CameraListener) -> None:
        with QMutexLocker(self._mutex):
            self._listener = listener
            self._listener.setParent(self)

    @property
    def property_controller(self) -> CameraPropertyController:
        with QMutexLocker(self._mutex):
            return self._property_controller

    # @Slot()
    # def enable_auto_grabbing(self) -> None:
    #     with QMutexLocker(self._mutex):
    #         self._auto_grabbing_enabled = True
    #         if self._timer_id <= 0:
    #             self.start()
    #
    # @Slot()
    # def disable_auto_grabbing(self) -> None:
    #     with QMutexLocker(self._mutex):
    #         self._auto_grabbing_enabled = False
    #         if self._timer_id > 0:
    #             self.stop()

    @Slot(bool)
    def set_auto_grabbing_flag(self, value: bool) -> None:
        with QMutexLocker(self._mutex):
            self._auto_grabbing_enabled = value
            if not self._auto_grabbing_enabled and self._timer_id > 0:
                self.stop()

    def start(self) -> None:
        if self._timer_id > 0:
            self.stop()
        if self._camera is None:
            return
        else:

            if self._listener is None:
                self._listener = CameraListener(parent=self)
            if self._camera.is_opened:
                self._camera.start()
                self._update_timer_interval()
                self._timer_id = self.startTimer(self._timer_interval)
                self._listener.on_camera_state_changed(True)

    def stop(self) -> None:
        if self._timer_id > 0:
            self.killTimer(self._timer_id)
            self._timer_id = -1
            self._camera.stop()
            self._listener.on_camera_state_changed(False)

    @Slot(bool)
    def run_status_changed(self, started: bool) -> None:
        with QMutexLocker(self._mutex):
            if started and self._auto_grabbing_enabled:
                self.start()
            else:
                self.stop()

    # @Slot(str, object)
    # def set_property_value(self, name: str, value: object) -> None:
    #     with QMutexLocker(self._mutex):
    #         try:
    #             if self._camera is None:
    #                 return
    #             if not self._camera.has_property(name):
    #                 return
    #             last_value = self._camera.get_property(name)
    #             if last_value != value:
    #                 self._camera.set_property_value(name, value)
    #                 self.signal_property_changed.emit(name, value)
    #                 if name == "fps":
    #                     self._update_timer_interval()
    #                     self._change_interval(self._timer_interval)
    #         except Exception as ex:
    #             if self._listener:
    #                 self._listener.on_error(str(ex))

    def has_property(self, name: str) -> bool:
        with QMutexLocker(self._mutex):
            if self._camera is None:
                return False
            if self._camera.has_property(name):
                prop = self._camera.get_property(name)
                return prop.available

    def _change_interval(self, value: int) -> None:
        if self._timer_interval == value:
            return
        self._timer_interval = value
        if self._timer_id <= 0:
            self.killTimer(self._timer_id)
            self._timer_id = self.startTimer(self._timer_interval)

    def _update_timer_interval(self) -> None:
        if isinstance(self._camera, CameraBase) and self._camera.has_property('fps'):
            fps = self._camera.get_property_value('fps')
            if isinstance(fps, (int, float)):
                if fps > 0:
                    self._timer_interval = int(1000 / float(fps))

    def timerEvent(self, *args, **kwargs):
        QCoreApplication.sendPostedEvents(self, 0)
        self._acquire()
        if self._update_fps:
            self._update_timer_interval()
            self._change_interval(self._timer_interval)
        super().timerEvent(*args, **kwargs)

    def _acquire(self):
        try:
            img = self._camera.query_frame()
            if img is not None:
                self._listener.on_new_image(img)
        except Exception as ex:
            self._listener.on_error(str(ex))
