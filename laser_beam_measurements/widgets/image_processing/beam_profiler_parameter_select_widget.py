# 
# Project: laser_beam_measurements
#
# File: beam_profiler_parameter_select_widget.py
#
# Author: Konstantin Prusakov
#
# Copyright 2025 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

# pyside6-uic laser_beam_measurements/widgets/image_processing/beam_profiler_parameter_select_widget.ui -o laser_beam_measurements/widgets/image_processing/ui_beam_profiler_parameter_select_widget.py

from .ui_beam_profiler_parameter_select_widget import Ui_Form
from PySide6.QtWidgets import QDialog, QDialogButtonBox
from PySide6.QtCore import Slot, Signal

from laser_beam_measurements.image_processing.beam_parameters.beam_parameters_selector import BeamParametersSelector


class BeamProfilerParameterSelectWidget(QDialog):

    def __init__(self, selector: BeamParametersSelector, parent=None):
        super(BeamProfilerParameterSelectWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._selector = selector
        self._connect_signals()
        self.ui.parameters_select_widget.fill_table(self._selector.bp)
        self.setWindowTitle("Select Beam Parameters")

    def _disconnect_signals(self) -> None:
        self.ui.parameters_select_widget.signal_stat_updated.disconnect(self._selector.slot_select)

    @Slot()
    def accept(self) -> None:
        self.ui.parameters_select_widget.update_stat()
        self._disconnect_signals()
        super().accept()

    @Slot()
    def reject(self) -> None:
        self._disconnect_signals()
        super().reject()

    @Slot()
    def apply(self):
        self.ui.parameters_select_widget.update_stat()

    @Slot()
    def reset(self):
        self.ui.parameters_select_widget.reset()
        self.ui.parameters_select_widget.update_stat()

    def _connect_signals(self) -> None:
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(self.reset)
        self.ui.parameters_select_widget.signal_stat_updated.connect(self._selector.slot_select)
