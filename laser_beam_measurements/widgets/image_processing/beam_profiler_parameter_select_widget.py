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
from PySide6.QtCore import Slot


class BeamProfilerParameterSelectWidget(QDialog):

    def __init__(self, parent=None):
        super(BeamProfilerParameterSelectWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self._connect_signals()

    @Slot()
    def accept(self) -> None:
        print("Accepted")
        super().accept()

    @Slot()
    def reject(self) -> None:
        print("Rejected")
        super().reject()

    @Slot()
    def apply(self):
        print("Apply")

    def _connect_signals(self) -> None:
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.apply)
