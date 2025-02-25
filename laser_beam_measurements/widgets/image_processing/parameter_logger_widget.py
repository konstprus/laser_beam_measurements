# 
# Project: laser_beam_measurements
#
# File: parameter_logger_widget.py
#
# Author: Konstantin Prusakov
#
# Copyright 2025 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

# pyside6-uic laser_beam_measurements/widgets/image_processing/parameter_logger_widget.ui -o laser_beam_measurements/widgets/image_processing/ui_parameter_logger_widget.py


from PySide6.QtWidgets import QTableWidgetItem, QTableWidget, QWidget
from laser_beam_measurements.image_processing.parameter_logger import ParameterLogger
from laser_beam_measurements.image_processing.parameter_logger_widget_base import ParameterLoggingWidgetBase
from .ui_parameter_logger_widget import Ui_Form

class ParameterLoggerWidget(ParameterLoggingWidgetBase):


    def __init__(self, parent=None):
        super(ParameterLoggerWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def _logger_state_changed(self, state: bool) -> None:
        pass
