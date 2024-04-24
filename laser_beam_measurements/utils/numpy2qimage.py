#
# Project: laser_beam_measurements
#
# File: numpy2qimage.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


import numpy
import cv2
from PySide6.QtGui import QImage


class ImageConverter(object):

    @staticmethod
    def to_grey(img: numpy.ndarray) -> numpy.ndarray:
        if len(img.shape) == 2:
            return img
        return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    @staticmethod
    def to_qimage(img: numpy.ndarray, color_table: list or None = None, copy: bool = True) -> QImage:
        _img: numpy.ndarray = img
        if color_table is not None:
            _img = ImageConverter.to_grey(img)

        qim = QImage()
        if len(_img.shape) == 3:
            if _img.shape[2] == 3:
                qim = QImage(_img.data, _img.shape[1], _img.shape[0], _img.strides[0], QImage.Format.Format_RGB888)
            elif _img.shape[2] == 4:
                qim = QImage(_img.data, _img.shape[1], _img.shape[0], _img.strides[0], QImage.Format.Format_ARGB32)
            elif _img.shape[2] == 1:
                qim = QImage(_img.data, _img.shape[1], _img.shape[0], _img.strides[0], QImage.Format.Format_Indexed8)
                qim.setColorTable(color_table)

        elif len(_img.shape) == 2:
            if _img.dtype == numpy.uint8:
                # qim = QImage(_img.data, _img.shape[1], _img.shape[0], _img.strides[0], QImage.Format.Format_Indexed8)
                if color_table:
                    qim = QImage(_img.data, _img.shape[1], _img.shape[0], _img.strides[0],
                                 QImage.Format.Format_Indexed8)
                    qim.setColorTable(color_table)
                else:
                    qim = QImage(_img.data, _img.shape[1], _img.shape[0], _img.strides[0],
                                 QImage.Format.Format_Grayscale8)
            elif _img.dtype == numpy.uint16:
                # im = (im / 16)
                # im = numpy.require(im, dtype=numpy.uint8, requirements='C')
                qim = QImage(_img.data, _img.shape[1], _img.shape[0], _img.strides[0], QImage.Format.Format_Grayscale16)
                if color_table:
                    qim.setColorTable(color_table)
            else:
                raise TypeError("Unsupported data type")

        else:
            raise TypeError("Wrong image shape {}".format(_img.shape))

        return qim.copy() if copy else qim
