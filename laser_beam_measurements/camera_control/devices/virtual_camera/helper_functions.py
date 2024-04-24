#
# Project: laser_beam_measurements
#
# File: helper_functions.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

import numpy


def generate_gauss(x, y, x0, y0, sigma, power) -> numpy.ndarray:
    center = (x - x0) ** 2 + (y - y0) ** 2
    exp_arg = -2.0*center/(sigma**2)
    return 2.0*power/(numpy.pi * sigma ** 2) * numpy.exp(exp_arg)
