# 
# Project: laser_beam_measurements
#
# File: custom_graphics_scene.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

import numpy
from .custom_graphics_scene import CustomGraphicsScene
from PySide6.QtCore import Slot, Qt, QPointF, QSizeF
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

    # def update_image(self, image: numpy.ndarray) -> None:
    #     self.image_item.set_image(image)
    #     self.update()

    def keyPressEvent(self, event) -> None:
        if event.key() not in [Qt.Key_Left, Qt.Key_Up, Qt.Key_Right, Qt.Key_Down]:
            return
        roi_state = self._roi.get_state()
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_Left:
                roi_state[BeamState.SIZE].setWidth(
                    roi_state[BeamState.SIZE].width() - self._roi.size_step
                )
            if event.key() == Qt.Key_Right:
                roi_state[BeamState.SIZE].setWidth(
                    roi_state[BeamState.SIZE].width() + self._roi.size_step
                )
            if event.key() == Qt.Key_Up:
                roi_state[BeamState.SIZE].setHeight(
                    roi_state[BeamState.SIZE].height() + self._roi.size_step
                )
            if event.key() == Qt.Key_Down:
                roi_state[BeamState.SIZE].setHeight(
                    roi_state[BeamState.SIZE].height() - self._roi.size_step
                )
        elif event.modifiers() == Qt.ShiftModifier:
            if event.key() == Qt.Key_Up:
                roi_state[BeamState.ANGLE] += 1
            if event.key() == Qt.Key_Down:
                roi_state[BeamState.ANGLE] -= 1
        else:
            print(event)
            if event.key() == Qt.Key_Left:
                roi_state[BeamState.POS].setX(
                    roi_state[BeamState.POS].x() - self._roi.pos_step
                )
            elif event.key() == Qt.Key_Right:
                roi_state[BeamState.POS].setX(
                    roi_state[BeamState.POS].x() + self._roi.pos_step
                )
            elif event.key() == Qt.Key_Up:
                roi_state[BeamState.POS].setY(
                    roi_state[BeamState.POS].y() - self._roi.pos_step
                )
            elif event.key() == Qt.Key_Down:
                roi_state[BeamState.POS].setY(
                    roi_state[BeamState.POS].y() + self._roi.pos_step
                )
        self._roi.slot_set_state_new(roi_state)
        # print(f'{event} from qgraphicsscene')
        super().keyPressEvent(event)
