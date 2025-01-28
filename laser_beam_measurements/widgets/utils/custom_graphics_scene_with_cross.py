# 
# Project: laser_beam_measurements
#
# File: custom_graphics_scene_with_cross.py
#
# Author: Konstantin Prusakov
#
# Copyright 2025 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from .custom_graphics_scene import CustomGraphicsScene
from .cross import Cross
from PySide6.QtCore import QSizeF, Slot
import numpy

_all__ = ['CustomGraphicsSceneWithCross']


class CustomGraphicsSceneWithCross(CustomGraphicsScene):

    def __init__(self, parent=None):
        super(CustomGraphicsSceneWithCross, self).__init__(parent)
        self._cross = Cross()
        self.addItem(self._cross)

    @property
    def cross(self) -> Cross:
        return self._cross

    @Slot(bool)
    def set_cross_visible(self, value: bool) -> None:
        self._cross.setVisible(value)

    def mousePressEvent(self, event):
        if self.image_item.raw_image is not None and self._cross.isVisible():
            self._cross.mouse_press_event(event.scenePos())
        super(CustomGraphicsSceneWithCross, self).mousePressEvent(event)

    def update_image(self, image: numpy.ndarray) -> None:
        if self._cross.isVisible():
            self._cross.set_size(image.shape)
        super(CustomGraphicsSceneWithCross, self).update_image(image)