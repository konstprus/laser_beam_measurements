#
# Project: laser_beam_measurements
#
# File: __init__.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtGui import QIcon
import os


__all__ = ["Icon"]


DEFAULT_RELATIVE_ICON_DIR = "svg"


def get_icons_dir() -> str:
    return os.path.dirname(os.path.realpath(__file__)) + os.sep + DEFAULT_RELATIVE_ICON_DIR


class Icon(QIcon):
    def __init__(self, file_name: str):
        super().__init__(get_icons_dir() + os.sep + file_name)
