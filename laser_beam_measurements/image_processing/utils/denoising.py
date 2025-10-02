#
# Project: laser_beam_measurements
#
# File: denoising.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#



import cv2
import numpy


def threshold(image: numpy.ndarray, th_level: float = 0.0) -> numpy.ndarray:
    if th_level != 0:
        max_level = numpy.max(image)
        _, th = cv2.threshold(image, th_level, max_level, cv2.THRESH_TOZERO)
        return th
    else:
        return image


def find_noise_level_from_histogram(img):
    bins = numpy.bincount(img.ravel())
    if numpy.shape(bins) != (0,):
        return numpy.nanargmax(bins)
    return 0
