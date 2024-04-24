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
from PySide6.QtWidgets import QGraphicsScene
from .image_item import ImageItem

__all__ = ["CustomGraphicsScene"]


class CustomGraphicsScene(QGraphicsScene):

    def __init__(self, parent=None):
        super(CustomGraphicsScene, self).__init__(parent)
        self.image_item = ImageItem()
        self.addItem(self.image_item)

    def update_image(self, image: numpy.ndarray) -> None:
        self.image_item.set_image(image)
        self.update()

    def set_colormap(self, colormap: list | None) -> None:
        self.image_item.set_colormap(colormap)
        self.update()


