# 
# Project: laser_beam_measurements
#
# File: custom_graphics_scene.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from .custom_graphics_scene import CustomGraphicsScene
from PySide6.QtCore import Slot, Qt
from .ROI import ROI
from laser_beam_measurements.image_processing.beam_finder import BeamState

__all__ = ["CustomGraphicsSceneWithROI"]


class CustomGraphicsSceneWithROI(CustomGraphicsScene):

    def __init__(self, parent=None):
        super(CustomGraphicsSceneWithROI, self).__init__(parent)
        self._roi = ROI()
        self.addItem(self._roi)

    @property
    def roi(self) -> ROI:
        return self._roi
    
    @Slot(bool)
    def set_roi_visible(self, value: bool) -> None:
        self._roi.setVisible(value)

    def keyPressEvent(self, event) -> None:
        if not self._roi.move_enabled:
            return
        
        pressed_key = event.key()
        if pressed_key not in (Qt.Key.Key_Left, Qt.Key.Key_Up, Qt.Key.Key_Right, Qt.Key.Key_Down):
            return
        
        modifiers = event.modifiers()
        roi_state = self._roi.get_state()
        
        if modifiers == Qt.KeyboardModifier.ControlModifier:
            size = roi_state[BeamState.SIZE]
            if pressed_key == Qt.Key.Key_Left:
                size.setWidth(size.width() - self._roi.size_step)
            elif pressed_key == Qt.Key.Key_Right:
                size.setWidth(size.width() + self._roi.size_step)
            elif pressed_key == Qt.Key.Key_Up:
                size.setHeight(size.height() + self._roi.size_step)
            elif pressed_key == Qt.Key.Key_Down:
                size.setHeight(size.height() - self._roi.size_step)
            roi_state[BeamState.SIZE] = size

        elif modifiers == Qt.KeyboardModifier.ShiftModifier:
            if not self._roi.rotate_enabled:
                return
            if pressed_key == Qt.Key.Key_Up:
                roi_state[BeamState.ANGLE] += self._roi.angle_step
            elif pressed_key == Qt.Key.Key_Down:
                roi_state[BeamState.ANGLE] -= self._roi.angle_step
        else:
            pos = roi_state[BeamState.POS]
            if pressed_key == Qt.Key.Key_Left:
                pos.setX(pos.x() - self._roi.pos_step)
            elif pressed_key == Qt.Key.Key_Right:
                pos.setX(pos.x() + self._roi.pos_step)
            elif pressed_key == Qt.Key.Key_Up:
                pos.setY(pos.y() - self._roi.pos_step)
            elif pressed_key == Qt.Key.Key_Down:
                pos.setY(pos.y() + self._roi.pos_step)
            roi_state[BeamState.POS] = pos

        self._roi.slot_set_state_from_roi_controls(roi_state)
        super().keyPressEvent(event)
