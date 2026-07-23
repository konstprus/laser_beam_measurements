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
from ...image_processing.beam_parameters import BeamParameters


class BeamProfilerParameterSelectWidget(QDialog):

    signal_set_average_control = Signal(bool, int)

    def __init__(self, selector: BeamParametersSelector, parent=None):
        super(BeamProfilerParameterSelectWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._selector = selector
        self._connect_signals()
        self.ui.parameters_select_widget.fill_table(self._selector.bp)
        self._fill_average_control(self._selector.bp)
        self.setWindowTitle("Select Beam Parameters")

    def _disconnect_signals(self) -> None:
        self.ui.parameters_select_widget.signal_stat_updated.disconnect(self._selector.slot_select)
        self.signal_set_average_control.disconnect(self._selector.slot_set_average_control)

    def _fill_average_control(self, bp: BeamParameters) -> None:
        average_control = bp.average_control
        self.ui.average_enable_cb.setChecked(average_control.enabled)
        self.ui.average_number_sb.setValue(average_control.number)

    def _update_average_control(self) -> None:
        self.signal_set_average_control.emit(
            self.ui.average_enable_cb.isChecked(),
            self.ui.average_number_sb.value())

    @Slot()
    def accept(self) -> None:
        self.ui.parameters_select_widget.update_stat()
        self._update_average_control()
        self._disconnect_signals()
        super().accept()

    @Slot()
    def reject(self) -> None:
        self._disconnect_signals()
        super().reject()

    @Slot()
    def apply(self):
        self.ui.parameters_select_widget.update_stat()
        self._update_average_control()

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
        self.signal_set_average_control.connect(self._selector.slot_set_average_control)
