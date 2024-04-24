#
# Project: laser_beam_measurements
#
# File: custom_graphics_view.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtWidgets import QGraphicsView
from PySide6.QtCore import Qt

__all__ = ["CustomGraphicsView"]


class CustomGraphicsView(QGraphicsView):

    def fit(self):
        if self.scene():
            rect = self.scene().itemsBoundingRect()
            self.resetTransform()
            self.fitInView(rect, Qt.KeepAspectRatio)
            self.centerOn(rect.center())

    def resizeEvent(self, event):
        self.fit()
        super(CustomGraphicsView, self).resizeEvent(event)
