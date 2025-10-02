#
# Project: laser_beam_measurements
#
# File: beam_width.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


import cv2
import numpy
from math import sqrt, pi, atan
from scipy.optimize import curve_fit
from time import time


def width_by_moments(image: numpy.ndarray, with_rotation: bool = True) -> tuple[float, float, float, float, float]:
    moment = cv2.moments(image)
    m00 = moment['m00']
    if m00 == 0.0:
        h, w = image.shape
        return w/2, h/2, 0.0, 0.0, 0.0
    else:
        mu20 = moment['mu20']
        mu02 = moment['mu02']
        mu11 = moment['mu11']
        center_of_mass_x = moment['m10'] / m00
        center_of_mass_y = moment['m01'] / m00
        if with_rotation:
            if (mu20 - mu02) > 0.0:
                d_x = 2 * sqrt(2 / m00) * sqrt(mu20 + mu02 + sqrt((mu20 - mu02) * (mu20 - mu02) + 4 * mu11 * mu11))
                d_y = 2 * sqrt(2 / m00) * sqrt(abs(mu20 + mu02 - sqrt((mu20 - mu02) * (mu20 - mu02) + 4 * mu11 * mu11)))
                angle = 1.0 / 2.0 * atan(2.0 * mu11 / (mu20 - mu02))
            elif (mu20 - mu02) < 0.0:
                d_x = 2 * sqrt(2 / m00) * sqrt(abs(mu20 + mu02 - sqrt((mu20 - mu02) * (mu20 - mu02) + 4 * mu11 * mu11)))
                # d_x = 2 * sqrt(2 / m00) * sqrt(mu20 + mu02 - sqrt((mu20 - mu02) * (mu20 - mu02) + 4 * mu11 * mu11))
                d_y = 2 * sqrt(2 / m00) * sqrt(abs(mu20 + mu02 + sqrt((mu20 - mu02) * (mu20 - mu02) + 4 * mu11 * mu11)))
                angle = 1.0 / 2.0 * atan(2.0 * mu11 / (mu20 - mu02))
            else:
                d_x = 2 * sqrt(2 / m00) * sqrt(abs(mu20 + mu02 + sqrt(4 * mu11 * mu11)))
                d_y = 2 * sqrt(2 / m00) * sqrt(abs(mu20 + mu02 - sqrt(4 * mu11 * mu11)))
                if mu11 == 0:
                    angle = 0.0
                else:
                    angle = pi / 4 * numpy.sign(mu20)
            return center_of_mass_x, center_of_mass_y, d_x, d_y, angle
        else:
            d_x = 4 * sqrt(mu20 / m00)
            d_y = 4 * sqrt(mu02 / m00)
            return center_of_mass_x, center_of_mass_y, d_x, d_y, 0.0


def _func_linear_interp(x1, x2, y1, y2, y):
    return (int(x2) - int(x1)) / (int(y2) - int(y1)) * (int(y) - int(y1)) + int(x1)


def width_by_level(img: numpy.ndarray | list, level: float = 0.135) -> float:
    assert len(img.shape) == 1
    if len(img) > 0:
        max_value = numpy.max(img)
        indexes = numpy.argwhere(img >= max_value * level).transpose()[0]
        if indexes[0] <= 0:
            left_index = indexes[0]
        else:
            left_index = _func_linear_interp(
                indexes[0] - 1,
                indexes[0],
                img[indexes[0] - 1],
                img[indexes[0]],
                max_value*level)

        if indexes[-1] >= img.shape[0] - 1:
            right_index = indexes[-1]
        else:
            right_index = _func_linear_interp(
                indexes[-1],
                indexes[-1] + 1,
                img[indexes[-1]],
                img[indexes[-1] + 1],
                max_value*level)

        return right_index - left_index
    return 0

def _func_gauss(x: numpy.ndarray, a: float, b: float, c: float) -> numpy.ndarray:
    if a == 0.0:
        return x
    return 2*c/(pi*a*a)*numpy.exp(-2*(x - b) ** 2 / a ** 2)


def width_by_gauss_approximation(img: numpy.ndarray, xx: numpy.ndarray, d0: float = None) -> tuple[float, numpy.ndarray]:
    # x = numpy.arange(-len(img) / 2, len(img) / 2)
    if d0 is not None:
        p0 = (d0 / 2.0, 0.0, pi * d0 * d0 / 32.0)
    else:
        p0 = None
    try:
        # max_im = float(numpy.max(img))
        # im = img / max_im if max_im > 0 else img
        res, _ = curve_fit(_func_gauss, xx, img, p0=p0, maxfev=100)
    except (RuntimeError, ValueError, RuntimeWarning):
        if d0 is not None:
            res = p0
        else:
            res = (img.shape[0] / 4, img.shape[0] / 2, 1.0)

    model = _func_gauss(xx, res[0], res[1], res[2])
    d = abs(2 * res[0])
    return d, model


def power_area(img: numpy.ndarray) -> tuple[float, float]:
    power = float(numpy.sum(img))
    a = numpy.sum(img*img)
    if a <= 0:
        area = 0.0
    else:
        area = power*power/a
    return power, area


def width_by_power_level(
            img: numpy.ndarray,
            level: float = 0.86,
            center=None,
            power=None,
            initial_radius=None) -> float:
    if power is None:
        power = float(numpy.sum(img))
    if center is None:
        center = (int(img.shape[1] / 2), int(img.shape[0] / 2))
    if initial_radius is None:
        initial_radius = int(min(img.shape)/2)

    if power <= 1.0:
        return 0.0

    h, w = img.shape
    yy, xx = numpy.ogrid[:h, :w]
    dist_from_center = numpy.sqrt((xx - center[0]) ** 2 + (yy - center[1]) ** 2)
    res_power = 0.0
    aim_power_range = (0.99 * level * power, 1.01 * level * power)
    radius = initial_radius
    t0 = time()
    while res_power < aim_power_range[0] or res_power > aim_power_range[1]:
        im_ = img.copy()
        numpy.place(im_, dist_from_center >= radius, 0)
        res_power = float(numpy.sum(im_))
        if 1.0 < res_power/aim_power_range[0] < 1.05:
            radius -= radius*0.02
        elif 0.95 < res_power / aim_power_range[1] < 1.0:
            radius += radius*0.02

        else:
            if res_power > aim_power_range[1]:
                radius -= radius*0.1
            elif res_power < aim_power_range[0]:
                radius += radius*0.1
        if time() - t0 > 0.1:
            break
    return 2*radius
