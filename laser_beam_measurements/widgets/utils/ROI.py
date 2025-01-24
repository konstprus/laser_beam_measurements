#
# Project: laser_beam_measurements
#
# File: ROI.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtWidgets import QGraphicsObject
from PySide6.QtCore import QRectF, QPointF, Signal, Slot, QSizeF, Qt
from PySide6.QtGui import QPen, QPainter, QTransform
from laser_beam_measurements.image_processing.beam_finder import BeamState

from enum import Enum


__all__ = ["ROI"]


class ROI(QGraphicsObject):

    RESIZE_ZONE_SIZE = 40
    MIN_AREA_SIZE = 40

    class SelectorZone(Enum):
        NONE = 1
        MOVE_ZONE = 2
        RESIZE_TOP_LEFT_ZONE = 3
        RESIZE_TOP_RIGHT_ZONE = 4
        RESIZE_BOTTOM_LEFT_ZONE = 5
        RESIZE_BOTTOM_RIGHT_ZONE = 6
        ROTATION_ZONE = 7

    signal_region_changed = Signal(dict)
    signal_region_change_finished = Signal(dict)

    def __init__(self,
                 parent=None,
                 pos: QPointF = QPointF(0, 0),
                 size: QSizeF = QSizeF(1, 1),
                 angle: float = 0.0,
                 pen: QPen | None = None):
        super(ROI, self).__init__(parent)
        self.center_offset: QPointF = QPointF()

        self.hovered: bool = False
        self.move_enabled: bool = False
        self.rotate_enabled: bool = False
        self.press_move_button = Qt.MouseButton.LeftButton
        self.press_rotate_button = Qt.MouseButton.RightButton

        self.active_zone = self.SelectorZone.NONE
        self.paint_pen: QPen | None = None
        self.set_pen(pen)
        self.state: dict[str, float | QPointF | QSizeF] = {
            BeamState.POS: pos,
            BeamState.SIZE: size,
            BeamState.ANGLE: angle
        }
        self.last_state: dict | None = None
        self.set_pos(self.state[BeamState.POS])
        self.setAcceptHoverEvents(True)

    def set_pen(self, pen: QPen | None) -> None:
        if pen is None:
            pen = QPen(Qt.GlobalColor.yellow, 1)
            pen.setCosmetic(True)
            # pen.setWidth(1)
        self.paint_pen = pen
        self.update()

    @Slot(bool)
    def set_manual_movable(self, value: bool) -> None:
        self.move_enabled = value

    @Slot(bool)
    def set_manual_rotation(self, value: bool) -> None:
        self.rotate_enabled = value

    def get_state(self) -> dict:
        sc = {
            BeamState.POS: QPointF(self.state[BeamState.POS]),
            BeamState.SIZE: QSizeF(self.state[BeamState.SIZE]),
            BeamState.ANGLE: float(self.state[BeamState.ANGLE])
        }
        return sc

    @Slot(dict)
    def slot_set_state(self, state: dict) -> None:
        if self.move_enabled:
            return
        _state = {
            BeamState.POS: QPointF(state[BeamState.POS][0], state[BeamState.POS][1]),
            BeamState.SIZE: QSizeF(state[BeamState.SIZE][0], state[BeamState.SIZE][1]),
            BeamState.ANGLE: state.get(BeamState.ANGLE, 0.0)
        }
        self.set_state(_state, True)

    def set_state(self, state: dict, update: bool = True) -> None:
        self.set_pos(state[BeamState.POS], update=False)
        self.set_size(state[BeamState.SIZE], update=False)
        self.set_angle(state[BeamState.ANGLE], update=update)

    def set_pos(self, pos: QPointF, update: bool = True, finish: bool = True) -> None:
        self.state[BeamState.POS] = pos
        super(ROI, self).setPos(pos)
        if update:
            self.state_changed(finish)

    def set_angle(self,
                  angle: float,
                  update: bool = True,
                  finish: bool = True):
        self.state[BeamState.ANGLE] = angle
        tr = QTransform()
        tr.rotate(-angle)
        self.setTransform(tr)
        if update:
            self.state_changed(finish)

    def set_size(self,
                 size: QSizeF,
                 update: bool = True,
                 finish: bool = True):
        self.prepareGeometryChange()
        self.state[BeamState.SIZE] = size
        if update:
            self.state_changed(finish)

    def state_changed(self, finish: bool = True) -> None:
        changed = False
        if self.last_state is None:
            changed = True
        else:
            state = self.get_state()
            for key, value in state.items():
                if value != self.last_state[key]:
                    changed = True

        self.prepareGeometryChange()
        if changed:
            self.update()
            self.signal_region_changed.emit(self.get_state())

        self.last_state = self.get_state()
        if finish:
            self.signal_region_change_finished.emit(self.last_state)

    def size(self):
        return self.get_state()[BeamState.SIZE]

    def pos(self):
        return self.get_state()[BeamState.POS]

    def angle(self):
        return self.get_state()[BeamState.ANGLE]

    def _generates_zones(self):
        zone_rect = QRectF(0, 0, self.RESIZE_ZONE_SIZE, self.RESIZE_ZONE_SIZE)
        zone_centers = dict()
        size: QSizeF = self.state[BeamState.SIZE]
        # r = QRectF(0, 0, size.width(), size.height()).normalized()
        r = QRectF(-size.width()/2, -size.height()/2, size.width(), size.height()).normalized()
        zone_centers[self.SelectorZone.RESIZE_TOP_LEFT_ZONE] = r.topLeft()
        zone_centers[self.SelectorZone.RESIZE_TOP_RIGHT_ZONE] = r.topRight()
        zone_centers[self.SelectorZone.RESIZE_BOTTOM_LEFT_ZONE] = r.bottomLeft()
        zone_centers[self.SelectorZone.RESIZE_BOTTOM_RIGHT_ZONE] = r.bottomRight()
        ans = dict()
        for key in zone_centers.keys():
            rect = QRectF(zone_rect)
            rect.moveCenter(zone_centers[key])
            ans[key] = rect
        return ans

    def paint(self, painter: QPainter, option, widget=None) -> None:
        size: QSizeF = self.state[BeamState.SIZE]
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(self.paint_pen)
        r = QRectF(-size.width()/2, -size.height()/2, size.width(), size.height()).normalized()
        painter.drawRect(r)
        # painter.translate(r.left(), r.top())
        # painter.drawRect(QRectF(0, 0, size.width(), size.height()).normalized())
        if self.hovered:
            zones = self._generates_zones()
            for i in zones:
                painter.fillRect(zones[i], self.paint_pen.color())
                painter.drawRect(zones[i])

    def boundingRect(self) -> QRectF:
        size = self.size()
        return QRectF(
            -size.width()/2 - self.RESIZE_ZONE_SIZE/2,
            -size.height()/2 - self.RESIZE_ZONE_SIZE/2,
            size.width() + self.RESIZE_ZONE_SIZE,
            size.height() + self.RESIZE_ZONE_SIZE).normalized()

    def state_rect(self, state: dict | None = None) -> QRectF:
        if state is None:
            state = self.state
        rect = self.boundingRect()
        tr = QTransform()
        tr.rotate(-state[BeamState.ANGLE])
        rect = tr.mapRect(rect)
        print(state[BeamState.POS])
        rect.moveCenter(state[BeamState.POS])
        return rect

    def inner_rect(self, state: dict | None = None, centered=True) -> QRectF:
        if state is None:
            state = self.state
        size: QSizeF = state[BeamState.SIZE]
        r = QRectF(-size.width() / 2, -size.height() / 2, size.width(), size.height()).normalized()
        if centered:
            r.moveCenter(state[BeamState.POS])
        return r

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.update()

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.update()

    def mousePressEvent(self, event):
        if not self.move_enabled:
            return
        if event.button() == self.press_move_button:
            pos = event.pos()
            zones = self._generates_zones()
            for i in zones:
                if zones[i].contains(pos):
                    self.active_zone = i
                    break
            if self.active_zone == self.SelectorZone.NONE and self.boundingRect().contains(pos):
                self.active_zone = self.SelectorZone.MOVE_ZONE
                self.center_offset = pos
        elif event.button() == self.press_rotate_button:
            if not self.rotate_enabled:
                return
            pos = event.pos()
            zones = self._generates_zones()
            for i in zones:
                if zones[i].contains(pos):
                    self.active_zone = self.SelectorZone.ROTATION_ZONE
                    self.center_offset = pos
                    break

    def mouseReleaseEvent(self, event):
        self.active_zone = self.SelectorZone.NONE

    def mouseMoveEvent(self, event):
        if not self.move_enabled:
            return
        scene = self.scene()
        if scene is None:
            return
        pos = event.pos()  # + self.state[BeamState.POS]
        new_state = dict()
        new_state.update(self.get_state())
        scene_rect = scene.sceneRect()
        if self.active_zone == self.SelectorZone.MOVE_ZONE:
            new_pos = pos - self.center_offset + self.state[BeamState.POS]
            state_rect = self.state_rect()
            d = QPointF(0, 0)
            if state_rect.left() < scene_rect.left():
                d.setX(scene_rect.left() - state_rect.left())
            elif state_rect.right() > scene_rect.right():
                d.setX(scene_rect.right() - state_rect.right())
            if state_rect.top() < scene_rect.top():
                d.setY(scene_rect.top() - state_rect.top())
            elif state_rect.bottom() > scene_rect.bottom():
                d.setY(scene_rect.bottom() - state_rect.bottom())
            new_pos += d
            # self.set_pos(new_pos, update=True, finish=True)
            new_state.update({BeamState.POS: new_pos})

        elif self.active_zone == self.SelectorZone.RESIZE_TOP_LEFT_ZONE:
            bounding_rect = self.inner_rect(centered=False)
            # bounding_rect.moveCenter(self.state[BeamState.POS])
            bounding_rect.setTopLeft(pos)
            new_size = bounding_rect.size()
            # self.set_size(new_size, update=True, finish=True)
            new_state.update({BeamState.SIZE: new_size})

        elif self.active_zone == self.SelectorZone.RESIZE_TOP_RIGHT_ZONE:
            bounding_rect = self.inner_rect(centered=False)
            # bounding_rect.moveCenter(self.state[BeamState.POS])
            bounding_rect.setTopRight(pos)
            new_size = bounding_rect.size()
            # self.set_size(new_size, update=True, finish=True)
            new_state.update({BeamState.SIZE: new_size})

        elif self.active_zone == self.SelectorZone.RESIZE_BOTTOM_LEFT_ZONE:
            bounding_rect = self.inner_rect(centered=False)
            # bounding_rect.moveCenter(self.state[BeamState.POS])
            bounding_rect.setBottomLeft(pos)
            new_size = bounding_rect.size()
            # self.set_size(new_size, update=True, finish=True)
            new_state.update({BeamState.SIZE: new_size})

        elif self.active_zone == self.SelectorZone.RESIZE_BOTTOM_RIGHT_ZONE:
            bounding_rect = self.inner_rect(centered=False)
            # bounding_rect.moveCenter(self.state[BeamState.POS])
            bounding_rect.setBottomRight(pos)
            new_size = bounding_rect.size()
            # self.set_size(new_size, update=True, finish=True)
            new_state.update({BeamState.SIZE: new_size})

        elif self.active_zone == self.SelectorZone.ROTATION_ZONE:
            if not self.rotate_enabled:
                return
            angle = self.state[BeamState.ANGLE]
            diff_angle = 0.1*(event.pos() - event.buttonDownPos(self.press_rotate_button)).x()
            # diff_angle = 0.5*(event.scenePos() - event.buttonDownScenePos(self.press_rotate_button)).x()
            new_angle = angle + diff_angle

            if new_angle > 45:
                new_angle = 45
            elif new_angle < -45:
                new_angle = -45
            new_state.update({BeamState.ANGLE: new_angle})

        # bounding_rect = self.boundingRect()
        # bounding_rect.moveCenter(self.state[BeamState.POS])
        # state_rect = self.state_rect()
        # inner_rect = self.inner_rect(centered=True)
        # if self.active_zone != self.SelectorZone.NONE:
        #     if state_rect.left() < scene_rect.left():
        #         self.m_innerRect.setLeft(sRect.left())
        #
        #     if self.m_innerRect.top() < sRect.top():
        #         self.m_innerRect.setTop(sRect.top())
        #
        #     if sRect.right() < self.m_innerRect.right():
        #         self.m_innerRect.setRight(sRect.right())
        #
        #     if sRect.bottom() < self.m_innerRect.bottom():
        #         self.m_innerRect.setBottom(sRect.bottom())

        inner_rect = self.inner_rect(state=new_state)
        min_size_achieved: bool = False
        if inner_rect.width() < self.MIN_AREA_SIZE:
            inner_rect.setWidth(self.MIN_AREA_SIZE)
            min_size_achieved = True

        if inner_rect.height() < self.MIN_AREA_SIZE:
            inner_rect.setHeight(self.MIN_AREA_SIZE)
            min_size_achieved = True

        if min_size_achieved:
            new_state.update({BeamState.SIZE: inner_rect.size()})

        self.set_state(new_state, True)
