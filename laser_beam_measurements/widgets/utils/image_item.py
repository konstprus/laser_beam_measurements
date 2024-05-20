# 
# Project: laser_beam_measurements
#
# File: image_item.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtWidgets import QGraphicsObject
from PySide6.QtGui import QImage, QPainter, QPixmap
from PySide6.QtCore import QRectF
import numpy
from laser_beam_measurements.utils.numpy2qimage import ImageConverter


__all__ = ["ImageItem"]


class ImageItem(QGraphicsObject):

    def __init__(self, parent=None, image: numpy.ndarray | None = None):
        super(ImageItem, self).__init__(parent)
        self.qimage: QImage | None = None
        self.image: numpy.ndarray | None = None
        self._colormap: list | None = None

        self._render_required = True
        self._unrenderable = False
        self.set_image(image)

    @property
    def raw_image(self):
        return self.image

    @property
    def colormap(self):
        return self._colormap

    def set_image(self, image: numpy.ndarray) -> None:
        self.image = image

    def paint(self, painter: QPainter, *args, **kwargs) -> None:
        if self.image is None:
            return
        if self._render_required:
            self.render()
        if self._unrenderable:
            return
        if self.qimage.format() == QImage.Format.Format_Indexed8:
            painter.drawPixmap(0, 0, QPixmap.fromImage(self.qimage))
        else:
            shape = self.image.shape[:2]
            painter.drawImage(QRectF(0, 0, shape[1], shape[0]), self.qimage)

    def render(self):
        self._unrenderable = True
        if self.image is None or self.image.size == 0:
            return
        qimage = ImageConverter.to_qimage(self.image, self._colormap)
        if qimage is not None:
            self.qimage = qimage
            self._unrenderable = False
        scene = self.scene()
        if scene:
            shape = self.image.shape[:2]
            scene.setSceneRect(0, 0, float(shape[1]), float(shape[0]))

    def set_colormap(self, colormap: list | None) -> None:
        self._colormap = colormap

    def boundingRect(self):
        if self.image is None:
            return QRectF(0., 0., 0., 0.)
        shape = self.image.shape[:2]
        return QRectF(0., 0., float(shape[1]), float(shape[0]))
