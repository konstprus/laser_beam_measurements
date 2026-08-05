# 
# Project: laser_beam_measurements
#
# File: camera_selector_dialog_base.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#
from typing import Optional

from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Slot, Signal
from .camera_selector import CameraSelector, CameraParameters


class CameraSelectorDialogBase(QDialog):

    signal_select_camera = Signal(CameraParameters)
    signal_select_camera_id = Signal(str, str)

    def __init__(self, parent=None, *args, **kwargs):
        super(CameraSelectorDialogBase, self).__init__(parent,  *args, **kwargs)
        self.accepted.connect(self.slot_accept_camera)
        self._selector: CameraSelector | None = None
        selector = kwargs.get("camera_selector", None)
        if isinstance(selector, CameraSelector):
            self.set_selector(selector)

    def set_selector(self, camera_selector: CameraSelector) -> None:
        if self._selector:
            self._selector.signal_factory_selected.disconnect(self.fill_available_cameras)
            self._selector.signal_pixel_formats_selected.disconnect(self.fill_available_pixel_formats)
            self.signal_select_camera.disconnect(self._selector.slot_select_camera)
            self.signal_select_camera_id.disconnect(self._selector.slot_select_camera_id)
            self._disconnect_signals()
        self._selector = camera_selector
        self._selector.signal_factory_selected.connect(self.fill_available_cameras)
        self._selector.signal_pixel_formats_selected.connect(self.fill_available_pixel_formats)
        self.signal_select_camera.connect(self._selector.slot_select_camera)
        self.signal_select_camera_id.connect(self._selector.slot_select_camera_id)
        self._connect_signals()
        self.fill_available_camera_types()

    def fill_available_camera_types(self):
        if self._selector is None:
            return
        camera_types = self._selector.get_available_factories()
        if len(camera_types) == 0:
            return
        self._fill_available_camera_types(camera_types)

    @Slot(list)
    def fill_available_cameras(self, camera_list: list) -> None:
        self._fill_available_cameras(camera_list)

    @Slot(list)
    def fill_available_pixel_formats(self, pf_list: list[str]) -> None:
        self._fill_available_pixel_formats(pf_list)

    def _disconnect_signals(self):
        pass

    def _connect_signals(self):
        pass

    def _fill_available_camera_types(self, camera_types: list) -> None:
        raise NotImplementedError()

    def _fill_available_cameras(self, camera_list: list) -> None:
        raise NotImplementedError()

    def _fill_available_pixel_formats(self, pf_list: list[str]) -> None:
        raise NotImplementedError()

    def _get_selected_camera_type(self) -> str:
        raise NotImplementedError()

    def _get_selected_camera(self) -> str:
        raise NotImplementedError()

    def _get_pixel_size(self) -> str:
        raise NotImplementedError()

    def _get_selected_camera_pixel_format(self) -> Optional[str]:
        raise NotImplementedError()

    @Slot()
    def slot_accept_camera(self):
        camera_type = self._get_selected_camera_type()
        camera_id = self._get_selected_camera()
        pixel_size = float(self._get_pixel_size())
        pf = self._get_selected_camera_pixel_format()
        cp : CameraParameters = CameraParameters(camera_type, camera_id , pixel_size, pf)
        self.signal_select_camera.emit(cp)
