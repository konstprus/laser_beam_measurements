# 
# Project: laser_beam_measurements
#
# File: cross.py
#
# Author: Konstantin Prusakov
#
# Copyright 2025 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtWidgets import QGraphicsObject
from PySide6.QtCore import QRectF, QPointF, Signal, Slot, QSizeF, QLineF
from PySide6.QtGui import QPen, QPainter, QColor


class Cross(QGraphicsObject):

    signal_point_changed = Signal(QPointF)

    def __init__(self,
                 parent=None,
                 pos: QPointF = QPointF(0, 0),
                 size: QSizeF = QSizeF(1, 1),
                 pen: QPen | None = None):
        super(Cross, self).__init__(parent)
        self._pos = pos
        self._size = size
        self._offset = 10.0
        self._pen: QPen | None = None
        self.set_pen(pen)
        self._flag_move_enabled: bool = False
        self.setPos(0.0, 0.0)


    def set_pen(self, pen: QPen | None) -> None:
        if pen is None:
            pen = QPen(QColor(255, 255, 0, 255), 2)
            # pen = QPen(QColor(255, 255, 255, 64), 2)
            pen.setDashPattern([4, 8])
            pen.setCosmetic(True)
        self._pen = pen
        self.update()

    def set_pos(self, pos: QPointF) -> None:
        self._pos = pos
        # self.setPos(0.0, 0.0)
        self.update()

    def set_size(self, size: QSizeF | tuple) -> None:
        if isinstance(size, tuple):
            self._size = QSizeF(size[1], size[0])
        elif isinstance(size, QSizeF):
            self._size = size
        # self.update()

    def paint(self, painter: QPainter, option, widget=None) -> None:
        if self.scene() is None:
            return
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(self._pen)
        x, y = self._pos.toTuple()
        left_h_line = QLineF(x - 10.0, y, self._offset, y)
        right_h_line = QLineF(x + 10.0, y, self._size.width() - self._offset, y)
        top_v_line = QLineF(x, y - 10.0, x, self._offset)
        down_v_line = QLineF(x, y + 10.0, x, self._size.height() - self._offset)
        for line in [left_h_line, right_h_line, top_v_line, down_v_line]:
            painter.drawLine(line)

    def mouse_press_event(self, pos: QPointF) -> None:
        if self._flag_move_enabled:
            self.set_pos(pos)
            self.signal_point_changed.emit(self._pos)

    def boundingRect(self) -> QRectF:
        return QRectF(
            self._offset,
            self._offset,
            self._size.width() - self._offset,
            self._size.height() - self._offset
        )

    @Slot(float, float)
    def slot_set_pos(self, pos_x: float, pos_y: float) -> None:
        if not self._flag_move_enabled:
            self.set_pos(QPointF(pos_y, pos_x))

    @Slot(bool)
    def slot_set_flag_move_enabled(self, value: bool) -> None:
        self._flag_move_enabled = value