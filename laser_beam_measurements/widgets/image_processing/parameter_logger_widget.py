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


from PySide6.QtWidgets import QTableWidgetItem, QTableWidget, QWidget, QListWidgetItem
from PySide6.QtCore import Qt, Slot
from laser_beam_measurements.image_processing.parameter_logger import ParameterLogger
from laser_beam_measurements.image_processing.parameter_logger_widget_base import ParameterLoggingWidgetBase
from .ui_parameter_logger_widget import Ui_Form
import pyqtgraph as pg
from typing import Optional, Iterable, Collection


def create_curves(curve_names: Collection) -> Optional[dict[str, pg.PlotDataItem]]:
    curves_dict = dict()
    if len(curve_names) == 2:
        curve_x = pg.PlotDataItem(name=curve_names[0])
        curve_x.setPen(pg.mkPen(color='#800000', width=2))
        curves_dict.update({curve_names[0]: curve_x})

        curve_y = pg.PlotDataItem(name=curve_names[1])
        curve_y.setPen(pg.mkPen(color='#000080', width=2))
        curves_dict.update({curve_names[1]: curve_y})
        return curves_dict

    elif len(curve_names) == 1:
        curve = pg.PlotDataItem(name=curve_names[0])
        curve.setPen(pg.mkPen(color='#800000', width=2))
        curves_dict.update({curve_names[0]: curve})
        return curves_dict

    else:
        return None

def set_curves_visibility(curves: dict[str, pg.PlotDataItem], is_visible: bool) -> None:
    [curve.setVisible(is_visible) for _, curve in curves.items()]

class ParameterLoggerWidget(ParameterLoggingWidgetBase):

    def __init__(self, parent=None):
        super(ParameterLoggerWidget, self).__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.start_stop_button.clicked.connect(self._slot_change_logger_state)
        self.ui.select_parameter.currentTextChanged.connect(self.slot_select_parameter_changed)
        self._configure_plot()
        self._curves: dict[str, dict[str, pg.PlotDataItem]] = dict()
        self._visible_curves_name: Optional[str] = None

    def _logger_state_changed(self, state: bool) -> None:
        if state:
            self._set_enabled(False)
            self._set_curves_visibility(False)
            self._curves.clear()
            self.slot_select_parameter_changed(self.ui.select_parameter.currentText())
            self.ui.start_stop_button.setText("Stop")
        else:
            self._set_enabled(True)
            self.ui.start_stop_button.setText("Start")

    def _show_available_parameters(self, parameters_list: list) -> None:
        self.ui.available_parameters.clear()
        for parameter in parameters_list:
            item = QListWidgetItem(str(parameter))
            item.setCheckState(Qt.CheckState.Unchecked)
            self.ui.available_parameters.addItem(item)

    @Slot()
    def _slot_change_logger_state(self) -> None:
        if self.ui.start_stop_button.text() == "Start":
            self._start_logging()
        elif self.ui.start_stop_button.text() == "Stop":
            self._stop_logging()

    def _start_logging(self) -> None:
        selected_parameters = self._collect_selected_parameters()
        self._fill_parameter_to_show(selected_parameters)
        # self._logger.slot_update_selected_parameters(selected_parameters)
        timer_interval = self._get_timer_interval()
        # self._logger.timer_interval = timer_interval
        self._logger.set_all_parameters(selected_parameters, timer_interval)
        self.signal_change_state.emit(True)

    def _stop_logging(self) -> None:
        # self._fill_parameter_to_show()
        self.signal_change_state.emit(False)

    def _collect_selected_parameters(self) -> list:
        selected_parameters = list()
        for i in range(self.ui.available_parameters.count()):
            item = self.ui.available_parameters.item(i)
            if item.checkState() == Qt.CheckState.Checked:
                selected_parameters.append(item.text())
        return selected_parameters

    def _get_timer_interval(self) -> int:
        try:
            value = float(self.ui.time_step.text())
            unit = self.ui.time_unit.currentText()
            if unit == "min":
                value *= 60000
            elif unit == "sec":
                value *= 1000
            return int(value)
        except Exception:
            return 1000

    def _set_enabled(self, value: bool) -> None:
        self.ui.available_parameters.setEnabled(value)
        self.ui.time_step.setEnabled(value)
        self.ui.time_unit.setEnabled(value)

    def _configure_plot(self) -> None:
        styles = {'color': 'b', }  # 'font-size': '8px'}
        plot_widget = self.ui.plot
        plot_widget.setBackground("w")
        # plot_widget.setYRange(0, 250)
        # plot_widget.setLabel("left", "Intensity", "a.u.", **styles)
        # plot_widget.setLabel("bottom", "Dimension", "mkm", **styles)
        plot_widget.showGrid(x=True, y=True)
        plot_widget.addLegend(offset=(1, 1), labelTextColor=[0, 0, 0], labelTextSize='8pt')

    def _fill_parameter_to_show(self, selected_parameters: Optional[list[str]] = None) -> None:
        self.ui.select_parameter.clear()
        if selected_parameters is None:
            return
        for parameter in selected_parameters:
            self.ui.select_parameter.addItem(str(parameter))

    def _slot_show_selected_parameter(self, group_name: str, logging_time: list, parameters: dict[str, list]) -> None:
        if self._visible_curves_name == group_name:
            visible_curves = self._curves[self._visible_curves_name]
            if len(visible_curves) != len(parameters):
                return
            for key, value in parameters:
                visible_curves[key].setData(logging_time, value)
        else:
            self._set_curves_visibility(False)
            if group_name not in self._curves.keys():
                self._create_curves_group(group_name, parameters)
            visible_curves = self._curves[group_name]
            set_curves_visibility(visible_curves, True)
            for key, value in parameters.items():
                curve = visible_curves[key]
                self.ui.plot.addItem(curve)
                curve.setData(logging_time, value)

    def _create_curves_group(self, group_name: str, parameters: dict[str, list]) -> None:
        curves = create_curves(list(parameters.keys()))
        self._curves[group_name] = curves
        for key, curve in curves.items():
            self.ui.plot.addItem(curve)

    def _set_curves_visibility(self, is_visible: bool = True) -> None:
        for group_name, group in self._curves.items():
            for curve_name, curve in group.items():
                if not is_visible:
                    self.ui.plot.removeItem(curve)
                curve.setVisible(is_visible)


    @Slot(str)
    def slot_select_parameter_changed(self, parameter_name: str) -> None:
        self.ui.plot.setLabel("left", parameter_name, "")
        self.ui.plot.setLabel("bottom", "Elapsed_time", "s")
        self.signal_set_parameter_to_show.emit(parameter_name)

    def _show_current_interval(self, counter: int, interval: float) -> None:
        status_text = f"Counts: {counter}, Actual interval: {round(interval, 2)} s"
        self.ui.status_label.setText(status_text)
