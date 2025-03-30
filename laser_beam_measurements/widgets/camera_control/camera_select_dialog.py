# 
# Project: laser_beam_measurements
#
# File: camera_select_dialog.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

# pyside6-uic laser_beam_measurements/widgets/camera_control/camera_select_dialog.ui -o laser_beam_measurements/widgets/camera_control/ui_camera_select_dialog.py
from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QDialogButtonBox

from laser_beam_measurements.camera_control.camera_selector_dialog_base import CameraSelectorDialogBase
from .ui_camera_select_dialog import Ui_Dialog

class PixelSizeValidator(QRegularExpressionValidator):
    def __init__(self, parent=None):
        rx = QRegularExpression(r'^[0-9]*[,.]?[0-9]*$')
        super().__init__(rx, parent)


class CameraSelectDialog(CameraSelectorDialogBase):

    def __init__(self, parent=None, *args, **kwargs):
        super(CameraSelectDialog, self).__init__(parent,  *args, **kwargs)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        val = PixelSizeValidator()
        self.ui.pixel_size_line_edit.setValidator(val)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
        self.ui.available_cameras_list_widget.currentItemChanged.connect(self._check_selection)


    def _fill_available_camera_types(self, camera_types: list) -> None:
        self.ui.camera_types_list_widget.clear()
        for camera_type in camera_types:
            self.ui.camera_types_list_widget.addItem(camera_type)

    def _fill_available_cameras(self, camera_list: list) -> None:
        self.ui.available_cameras_list_widget.clear()
        for camera_id in camera_list:
            self.ui.available_cameras_list_widget.addItem(str(camera_id))

    def _get_selected_camera_type(self) -> str:
        return self.ui.camera_types_list_widget.currentItem().text()

    def _get_selected_camera(self) -> str:
        return self.ui.available_cameras_list_widget.currentItem().text()

    def _get_pixel_size(self) -> str:
        return self.ui.pixel_size_line_edit.text().replace(',', '.')

    def _disconnect_signals(self):
        self.ui.camera_types_list_widget.currentTextChanged.disconnect(self._selector.slot_select_factory)

    def _connect_signals(self):
        self.ui.camera_types_list_widget.currentTextChanged.connect(self._selector.slot_select_factory)

    # def _check_selection(self, value):
    def _check_selection(self):
        current_item = self.ui.available_cameras_list_widget.currentItem()
        if current_item:
            self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(True)
        else:
            self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Ok).setEnabled(False)
            