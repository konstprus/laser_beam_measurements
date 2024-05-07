# 
# Project: laser_beam_measurements
#
# File: settings_bool_reader.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import QSettings


def read_boolean_value(settings: QSettings, name: str, default_value: bool) -> bool:
    if settings.contains(name):
        value = settings.value(name)
        if isinstance(value, str):
            if value == "true":
                return True
            elif value == "false":
                return False
    return default_value
