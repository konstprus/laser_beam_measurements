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

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_Left:
                roi_state = self._roi.get_state()
                x, y = roi_state['size'].toTuple()
                roi_state['size'] = QSizeF(x - 10, y)
                self._roi.set_state(roi_state)
            if event.key() == Qt.Key_Right:
                roi_state = self._roi.get_state()
                x, y = roi_state['size'].toTuple()
                roi_state['size'] = QSizeF(x + 10, y)
                self._roi.set_state(roi_state)
            if event.key() == Qt.Key_Up:
                roi_state = self._roi.get_state()
                x, y = roi_state['size'].toTuple()
                roi_state['size'] = QSizeF(x, y + 10)
                self._roi.set_state(roi_state)
            if event.key() == Qt.Key_Down:
                roi_state = self._roi.get_state()
                x, y = roi_state['size'].toTuple()
                roi_state['size'] = QSizeF(x, y - 10)
                self._roi.set_state(roi_state)
        if event.modifiers() == Qt.ShiftModifier:
            if event.key() == Qt.Key_Up:
                roi_state = self._roi.get_state()
                angle = roi_state['angle']
                roi_state['angle'] = angle + 1
                self._roi.set_state(roi_state)
            if event.key() == Qt.Key_Down:
                roi_state = self._roi.get_state()
                angle = roi_state['angle']
                roi_state['angle'] = angle - 1
                self._roi.set_state(roi_state)
        else:
            if event.key() == Qt.Key_Left:
                roi_state = self._roi.get_state()
                x, y = roi_state['pos'].toTuple()
                roi_state['pos'] = QPointF(x - 10, y)
                self._roi.set_state(roi_state)
            elif event.key() == Qt.Key_Right:
                roi_state = self._roi.get_state()
                x, y = roi_state['pos'].toTuple()
                roi_state['pos'] = QPointF(x + 10, y)
                self._roi.set_state(roi_state)
            elif event.key() == Qt.Key_Up:
                roi_state = self._roi.get_state()
                x, y = roi_state['pos'].toTuple()
                roi_state['pos'] = QPointF(x, y - 10)
                self._roi.set_state(roi_state)
            elif event.key() == Qt.Key_Down:
                roi_state = self._roi.get_state()
                x, y = roi_state['pos'].toTuple()
                roi_state['pos'] = QPointF(x, y + 10)
                self._roi.set_state(roi_state)
        print(f'{event} from qgraphicsscene')
        super().keyPressEvent(event)
