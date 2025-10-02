#
# Project: laser_beam_measurements
#
# File: sub_image.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


import cv2
import numpy
from math import cos, sin


MIN_ANGLE = 0.001


def sub_image(
        image: numpy.ndarray,
        center: tuple[float, float],
        width: float,
        height: float,
        copy: bool = True) -> numpy.ndarray:
    cx, cy = center
    pt11 = int(cy - height / 2) if cy > height / 2 else 0
    pt21 = int(cy + height / 2) if cy + height / 2 < image.shape[0] else image.shape[0]
    pt10 = int(cx - width / 2) if cx > width / 2 else 0
    pt20 = int(cx + width / 2) if cx + width / 2 < image.shape[1] else image.shape[1]
    return numpy.array(image[pt11:pt21, pt10:pt20], copy=copy)


def rotate_sub_image(
        image: numpy.ndarray,
        center: tuple[float, float],
        width: float,
        height: float,
        angle: float,
        copy: bool = True) -> numpy.ndarray:
    if abs(angle) < MIN_ANGLE:
        return sub_image(image, center, width, height, copy)
    v_x = (cos(angle), sin(angle))
    v_y = (-sin(angle), cos(angle))
    c0 = int(center[0])
    c1 = int(center[1])
    w = int(width)
    h = int(height)
    s_x = c0 - v_x[0] * ((w - 1) / 2) - v_y[0] * ((h - 1) / 2)
    s_y = c1 - v_x[1] * ((w - 1) / 2) - v_y[1] * ((h - 1) / 2)
    mapping = numpy.array([[v_x[0], v_y[0], s_x],
                           [v_x[1], v_y[1], s_y]])
    flags = cv2.WARP_INVERSE_MAP + cv2.INTER_LINEAR
    border_mode = cv2.BORDER_TRANSPARENT
    rotated_image = cv2.warpAffine(image, mapping, (w, h), flags=flags, borderMode=border_mode)
    return rotated_image.copy() if copy else rotated_image


def get_cross_section(img: numpy.ndarray, x: float, y: float, copy: bool = True) -> tuple[numpy.ndarray, numpy.ndarray]:
    try:
        imx = numpy.array(img[int(y), 0:], copy=copy)
        imy = numpy.array(img[0:, int(x)], copy=copy)
    except IndexError:
        imx = numpy.zeros(img.shape[0])
        imy = numpy.zeros(img.shape[1])
    return imx, imy
