# 
# Project: laser_beam_measurements
#
# File: beam_profiler_parameters_model.py
#
# Author: Konstantin Prusakov
#
# Copyright 2025 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import QObject, QAbstractItemModel


class BeamProfilerParametersModel(QAbstractItemModel):

    def __init__(self, parent=None):
        super(BeamProfilerParametersModel, self).__init__(parent)
