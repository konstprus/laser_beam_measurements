# 
# Project: laser_beam_measurements
#
# File: image_saver.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtCore import QObject, QRunnable, QThreadPool
from PySide6.QtWidgets import QFileDialog
from PySide6.QtGui import QImage
import numpy
from .numpy2qimage import ImageConverter


class ImageSaverRunnable(QRunnable):

    def __init__(self, image: numpy.ndarray | QImage, path: str):
        super(ImageSaverRunnable, self).__init__()
        self._image: numpy.ndarray | QImage = image
        self._path: str = path

    def run(self):
        if isinstance(self._image, numpy.ndarray) and self._path.endswith('csv'):
            numpy.savetxt(self._path, self._image, fmt="%i", delimiter=";")
        elif isinstance(self._image, QImage):
            if self._path.endswith("png"):
                self._image.save(self._path, "PNG")
            elif self._path.endswith("jpg"):
                self._image.save(self._path, "JPG")
            elif self._path.endswith("jpeg"):
                self._image.save(self._path, "JPEG")
            elif self._path.endswith("bmp"):
                self._image.save(self._path, "BMP")
            else:
                self._image.save(self._path, "PNG")

    def save(self):
        thread_pool = QThreadPool.globalInstance()
        thread_pool.start(self)


class ImageSaver(QObject):

    filters = [
        "Images (*.png *.jpg *.bmp *.jpeg)",
        "Raw images (*.csv)",
        "All files (*.*)"
    ]

    def __init__(self, parent=None):
        super(ImageSaver, self).__init__(parent)
        self._image: numpy.ndarray | None = None
        self._colormap: list | None = None

    def set_image(self, image: numpy.ndarray | None) -> None:
        if image is None:
            return
        self._image = image.copy()

    def set_colormap(self, colormap: list) -> None:
        self._colormap = colormap

    def save(self, path: str) -> None:
        if path.endswith(".csv"):
            self.save_raw(path)
        else:
            self.save_q_image(path)

    def save_raw(self, path: str) -> None:
        runnable = ImageSaverRunnable(self._image, path)
        runnable.save()

    def save_q_image(self, path: str) -> None:
        qimage = ImageConverter.to_qimage(self._image, self._colormap)
        runnable = ImageSaverRunnable(qimage, path)
        runnable.save()

    def show_save_dialog(self):
        if self._image is None:
            return
        filters = ";;".join(self.filters)
        filename, _ = QFileDialog.getSaveFileName(self.parent(), "Save image", filter=filters)
        if filename != "":
            self.save(filename)
