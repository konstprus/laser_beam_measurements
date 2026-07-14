# 
# Project: laser_beam_measurements
#
# File: parameters_select_table_widget.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView, QAbstractScrollArea
from PySide6.QtGui import QFont
from PySide6.QtCore import Slot, Qt, Signal

from laser_beam_measurements.image_processing.beam_parameters import BeamParameters, BeamParametersStat
from laser_beam_measurements.image_processing.beam_parameters.parameter import Parameter, ParameterStat
from laser_beam_measurements.image_processing.beam_parameters.parameter_group import ParameterGroup

def _create_table_item(text: str,
                       color: Qt.GlobalColor | None = None,
                       checkable: bool = False,
                       bold: bool = False,
                       alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter) -> QTableWidgetItem:
    item = QTableWidgetItem(text)
    if color:
        item.setBackground(color)
    if bold:
        font = QFont()
        font.setBold(bold)
        item.setFont(font)
        item.setFlags(Qt.ItemFlag.ItemIsEnabled)
    if checkable:
        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
    if not checkable and not bold:
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable | Qt.ItemFlag.ItemIsEnabled)
    if alignment:
        item.setTextAlignment(alignment)
    return item

def _check_state(value: bool) -> Qt.CheckState:
    if value:
        return Qt.CheckState.Checked
    else:
        return Qt.CheckState.Unchecked

class PairItem(object):

    def __init__(self, parameter: Parameter) -> None:
        item_name = _create_table_item(parameter.name, Qt.GlobalColor.lightGray, checkable=True, bold=True)
        item_name.setCheckState(_check_state(parameter.enabled))
        item_verbose_name = _create_table_item(parameter.verbose_name, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        self._name: QTableWidgetItem = item_name
        self._verbose_name: QTableWidgetItem = item_verbose_name

    def add_to_table(self, row: int, table: QTableWidget) -> None:
        table.setItem(row, 0, self._name)
        table.setItem(row, 1, self._verbose_name)

    def update(self, parameter: Parameter) -> None:
        self._name.setCheckState(_check_state(parameter.enabled))
        self._verbose_name.setText(parameter.verbose_name)

    @property
    def name(self) -> str:
        return self._name.text()

    @property
    def verbose_name(self) -> str:
        return self._verbose_name.text()

    @property
    def enabled(self) -> bool:
        return self._name.checkState() == Qt.CheckState.Checked

    @property
    def stat(self) -> ParameterStat:
        return self.name, self.verbose_name, self.enabled

    def reset(self):
        self._name.setCheckState(Qt.CheckState.Checked)
        self._verbose_name.setText(self._name.text())

class ParametersSelectTableWidget(QTableWidget):

    signal_stat_updated = Signal(list)

    def __init__(self, parent=None):
        super(ParametersSelectTableWidget, self).__init__(parent)
        self._items: dict[str, list[PairItem]] = {}
        self._number_of_columns: int = 2
        self._titles: list = ["Name", "Verbose Name"]
        self.verticalHeader().hide()
        self.setColumnCount(self._number_of_columns)
        self.setHorizontalHeaderLabels(self._titles)

    def fill_table(self, beam_parameters: BeamParameters) -> None:
        self._items.clear()
        self.clear()
        self.setColumnCount(self._number_of_columns)
        self.setHorizontalHeaderLabels(self._titles)
        self._add_group(beam_parameters.width)
        self._add_group(beam_parameters.position_and_orientation)
        self._add_group(beam_parameters.other_parameters)
        self.resizeColumnsToContents()
        self.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)

    @Slot(BeamParameters)
    def update_table(self, beam_parameters: BeamParameters) -> None:
        self._update_group(beam_parameters.width)
        self._update_group(beam_parameters.position_and_orientation)
        self._update_group(beam_parameters.other_parameters)

    def _update_group(self, group: ParameterGroup) -> None:
        if group.name not in self._items.keys():
            return
        group_items = self._items[group.name]
        for item in group_items:
            parameter = group.get_parameter(item.name)
            if parameter is None:
                continue
            item.update(parameter)

    def _add_group(self, group: ParameterGroup) -> None:
        self._create_header(group.name)
        group_items: list[PairItem] = []
        for parameter in group:
            group_items.append(self._add_parameter(parameter))
        self._items[group.name] = group_items

    def reset(self):
        for _, items in self._items.items():
            [item.reset() for item in items]
        # self.update_stat()


    def _create_header(self, title: str) -> None:
        row = self.rowCount()
        self.setRowCount(row+1)
        item = _create_table_item(title, Qt.GlobalColor.lightGray, bold=True)
        self.setSpan(row, 0, 1, self._number_of_columns)
        self.setItem(row, 0 , item)

    def _add_parameter(self, parameter: Parameter) -> PairItem:
        row = self.rowCount()
        self.setRowCount(row + 1)
        name_pair = PairItem(parameter)
        name_pair.add_to_table(row, self)
        return name_pair

    def update_stat(self):
        stat = BeamParametersStat()
        for name, items in self._items.items():
            # name, items = item_group
            group_stat = [item.stat for item in items]
            stat.append((name, group_stat))
        self.signal_stat_updated.emit(stat)