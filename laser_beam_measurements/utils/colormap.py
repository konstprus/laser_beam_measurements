#
# Project: laser_beam_measurements
#
# File: colormap.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtGui import qRgb
import numpy
from inspect import getmembers
from .colormaps import cet_tables
from .colormaps.seismic_data import _seismic_data256


class ColorMap(object):

    def __init__(self):
        self._maps: dict[str, list[int]] = {}

    @staticmethod
    def _to_rgb(colormap: list | numpy.ndarray) -> list[int]:
        colormap = numpy.array(colormap)
        result = []
        for color in colormap:
            result.append(qRgb(color[0], color[1], color[2]))
        return result

    @staticmethod
    def _generate_colormap(minvalue, maxvalue, colormap):
        return ColorMap._to_rgb(colormap[minvalue:maxvalue+1])

    @staticmethod
    def _generate_colormap_interp(minvalue, maxvalue, color_map):
        points = numpy.array(color_map)
        interp = numpy.empty((maxvalue + 1 - minvalue, 3))
        x = numpy.linspace(minvalue, maxvalue, interp.shape[0])
        for c in range(points.shape[1]):
            interp[:, c] = numpy.interp(x, numpy.linspace(0, points.shape[0], points.shape[0]), points[:, c])
        return ColorMap._to_rgb(interp)

    def add_colormap(self, colormap_name: str, colormap: list | None) -> None:
        if colormap is None:
            self._maps.update({colormap_name: None})
        else:
            if len(colormap) == 0:
                return
            first_element = colormap[0]
            if isinstance(first_element, int):
                self._maps.update({colormap_name: colormap})
            elif isinstance(first_element, list):
                self._maps.update({colormap_name: ColorMap._generate_colormap_interp(0, 255, colormap)})

    def get_colormap(self, colormap_name: str) -> list | None:
        if colormap_name in self._maps.keys():
            return self._maps[colormap_name]
        return None

    def get_names(self):
        return list(self._maps.keys())


COLORMAPS = ColorMap()

COLORMAPS.add_colormap("None", None)
COLORMAPS.add_colormap("Seismic", _seismic_data256)
COLORMAPS.add_colormap("Grey", [qRgb(i, i, i) for i in range(256)])


def _my_getmembers(oo):
    return [o for o in getmembers(oo) if not o[0].startswith('__')]


for name, table in _my_getmembers(cet_tables):
    COLORMAPS.add_colormap(name, table)

# del ColorMap
