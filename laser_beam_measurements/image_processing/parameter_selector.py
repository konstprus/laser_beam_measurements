# 
# Project: laser_beam_measurements
#
# File: parameter_selector.py
#
# Author: Konstantin Prusakov
#
# Copyright 2025 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from PySide6.QtWidgets import QWidget


class ParameterSelector(QWidget):

    def __init__(self, parent=None):
        super(ParameterSelector, self).__init__(parent)
