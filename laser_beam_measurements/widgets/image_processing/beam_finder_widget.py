# 
# Project: laser_beam_measurements
#
# File: beam_finder_widget.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

# pyside6-uic laser_beam_measurements/widgets/image_processing/beam_finder_widget.ui -o laser_beam_measurements/widgets/image_processing/ui_beam_finder_widget.py

from laser_beam_measurements.image_processing.image_processor_viewer_base import ImageProcessorViewerBase
from laser_beam_measurements.image_processing.beam_finder import BeamFinder, BeamFinderParameters
from .ui_beam_finder_widget import Ui_Form
from PySide6.QtCore import Slot
from laser_beam_measurements.widgets.utils.ROI import ROI

from laser_beam_measurements.utils.colormap import COLORMAPS


class BeamFinderWidget(ImageProcessorViewerBase):

    def __init__(self, parent=None):
        super(BeamFinderWidget, self).__init__(parent, configure_input_scene=True, configure_output_scene=False)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.input_beam_view.setScene(self._input_image_scene)
        self.setWindowTitle("Beam Finder")
        self.roi = ROI()
        self.roi.setVisible(False)
        self._input_image_scene.addItem(self.roi)
        self._connect_signals()
        self._fill_colormap_combobox()

    def _connect_signals(self) -> None:
        self.ui.enable_check_box.toggled.connect(self._slot_enabled_changed)
        self.ui.find_auto_check_box.toggled.connect(self._slot_set_find_auto)
        self.ui.noise_group_box.toggled.connect(self._slot_set_delete_noise)
        self.ui.rotation_group_box.toggled.connect(self._slot_set_rotation_enable)
        self.ui.rotation_auto_check_box.toggled.connect(self._slot_set_manual_rotation)
        self.ui.noise_value_spin_box.valueChanged.connect(self._slot_set_noise_level)
        self.ui.angle_value_spin_box.valueChanged.connect(self._slot_set_angle_value)
        self.ui.colormap_combo_box.currentTextChanged.connect(self.slot_set_colormap_for_input)

    def _connect_processor_signal(self) -> None:
        super(BeamFinderWidget, self)._connect_processor_signal()
        if isinstance(self._image_processor, BeamFinder):
            self._image_processor.signal_beam_state_updated.connect(self.roi.slot_set_state)
            self.roi.signal_region_changed.connect(self._image_processor.slot_set_beam_state)

    def _disconnect_processor_signal(self) -> None:
        super(BeamFinderWidget, self)._connect_processor_signal()
        if isinstance(self._image_processor, BeamFinder):
            self._image_processor.signal_beam_state_updated.disconnect(self.roi.slot_set_state)
            self.roi.signal_region_changed.disconnect(self._image_processor.slot_set_beam_state)

    def _change_parameter(self, name: str | BeamFinderParameters, value: object) -> None:
        self.signal_parameter_changed.emit(name, value)

    def _fill_colormap_combobox(self) -> None:
        for name in COLORMAPS.get_names():
            self.ui.colormap_combo_box.addItem(name)

    @Slot(bool)
    def _slot_enabled_changed(self, value: bool) -> None:
        self.ui.find_auto_check_box.setEnabled(value)
        self.ui.noise_group_box.setEnabled(value)
        self.ui.rotation_group_box.setEnabled(value)
        self.signal_enable_changed.emit(value)
        self.roi.setVisible(value)

    @Slot(bool)
    def _slot_set_find_auto(self, value: bool) -> None:
        self._change_parameter(BeamFinderParameters.FIND_AUTO, value)
        self.roi.set_manual_movable(not value)

    @Slot(bool)
    def _slot_set_delete_noise(self, value: bool) -> None:
        self._change_parameter(BeamFinderParameters.DELETE_NOISE_ENABLE, value)

    @Slot(bool)
    def _slot_set_rotation_enable(self, value: bool) -> None:
        self._change_parameter(BeamFinderParameters.ROTATION_ENABLE, value)

    @Slot(bool)
    def _slot_set_manual_rotation(self, value: bool) -> None:
        self.ui.angle_value_spin_box.setEnabled(not value)
        self._change_parameter(BeamFinderParameters.MANUAL_ROTATION_ENABLE, not value)
        self.roi.set_manual_rotation(not value)

    @Slot(float)
    def _slot_set_noise_level(self, value: float) -> None:
        self._change_parameter(BeamFinderParameters.NOISE_LEVEL, value)

    @Slot(float)
    def _slot_set_angle_value(self, value: float) -> None:
        self._change_parameter(BeamFinderParameters.ROTATION_ANGLE, value)

    def _update_parameters(self):
        self.roi.setVisible(self._image_processor.enabled)
        self.ui.enable_check_box.setChecked(self._image_processor.enabled)
        self.ui.find_auto_check_box.setChecked(
            self._image_processor.get_parameter_value(BeamFinderParameters.FIND_AUTO))
        self.ui.noise_group_box.setChecked(
            self._image_processor.get_parameter_value(BeamFinderParameters.DELETE_NOISE_ENABLE))
        self.ui.noise_value_spin_box.setValue(
            self._image_processor.get_parameter_value(BeamFinderParameters.NOISE_LEVEL))
        self.ui.rotation_group_box.setChecked(
            self._image_processor.get_parameter_value(BeamFinderParameters.ROTATION_ENABLE))
        self.ui.rotation_auto_check_box.setChecked(
            not self._image_processor.get_parameter_value(BeamFinderParameters.MANUAL_ROTATION_ENABLE))
        self.ui.angle_value_spin_box.setValue(
            self._image_processor.get_parameter_value(BeamFinderParameters.ROTATION_ANGLE))
