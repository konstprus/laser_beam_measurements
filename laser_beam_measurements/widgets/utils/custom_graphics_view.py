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
from PySide6.QtCore import Qt, Slot, QRectF
from typing import Optional

__all__ = ["CustomGraphicsView"]


class CustomGraphicsView(QGraphicsView):

    @Slot(QRectF)
    def slot_scene_rect_changed(self, rect: QRectF) -> None:
        self.fit(rect)

    def fit(self, rect: Optional[QRectF] = None):
        _rect = rect
        if _rect is None:
            if self.scene():
                _rect = self.scene().itemsBoundingRect()
            else:
                return
        self.resetTransform()
        self.fitInView(_rect, Qt.AspectRatioMode.KeepAspectRatio)
        self.centerOn(_rect.center())

    def resizeEvent(self, event):
        self.fit()
        super(CustomGraphicsView, self).resizeEvent(event)
