# 
# Project: laser_beam_measurements
#
# File: parameters_table_widget.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QAbstractItemView
from PySide6.QtGui import QFont
from PySide6.QtCore import Slot, Qt

from typing import Union

from laser_beam_measurements.image_processing.beam_parameters import BeamParameters
from laser_beam_measurements.image_processing.beam_parameters.parameter import Parameter
from laser_beam_measurements.image_processing.beam_parameters.parameter_group import ParameterGroup


def _create_table_item(text: str,
                       color: Qt.GlobalColor | None = None,
                       bold: bool = False,
                       alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter) -> QTableWidgetItem:
    item = QTableWidgetItem(text)
    if color:
        item.setBackground(color)
    if bold:
        font = QFont()
        font.setBold(bold)
        item.setFont(font)
    if alignment:
        item.setTextAlignment(alignment)
    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
    return item


class ParametersTableWidget(QTableWidget):

    def __init__(self, parent=None):
        super(ParametersTableWidget, self).__init__(parent)
        self._items: dict[str, Union[QTableWidgetItem, tuple[QTableWidgetItem, QTableWidgetItem]]] = dict()
        self._number_of_columns: int = 4
        self._sub_titles: tuple = ('', 'Axis X', 'Axis Y', '')
        self._round: int = 2
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.setColumnCount(self._number_of_columns)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

    @Slot(BeamParameters)
    def update_table(self, beam_parameters: BeamParameters) -> None:
        self._items.clear()
        self.clear()
        self.setRowCount(0)
        self._add_group(beam_parameters.position_and_orientation)
        self._add_group(beam_parameters.width)
        self._add_group(beam_parameters.other_parameters, False)
        self.resizeColumnToContents(0)

    def _add_sub_titles(self) -> None:
        row = self.rowCount()
        self.setRowCount(row+1)
        for index, value in enumerate(self._sub_titles):
            item = _create_table_item(value, Qt.GlobalColor.lightGray, bold=True)
            self.setItem(row, index, item)

    def _create_header(self, title: str, add_sub_titles: bool = True) -> None:
        row = self.rowCount()
        self.setRowCount(row+1)
        item = _create_table_item(title, Qt.GlobalColor.lightGray, bold=True)
        self.setSpan(row, 0, 1, self._number_of_columns)
        self.setItem(row, 0 , item)
        if add_sub_titles:
            self._add_sub_titles()

    def _add_parameter(self, parameter: Parameter) -> None:
        row = self.rowCount()
        self.setRowCount(row + 1)
        item_title = _create_table_item(parameter.verbose_name, Qt.GlobalColor.lightGray, bold=True)
        self.setItem(row, 0 , item_title)
        alignment =  Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        if parameter.count == 2:
            item_x = _create_table_item("", alignment=alignment)
            item_y = _create_table_item("", alignment=alignment)
            self.setItem(row, 1, item_x)
            self.setItem(row, 2, item_y)
            self._items[parameter.name] = (item_x, item_y)
        else:
            item = _create_table_item("", alignment=alignment)
            self.setItem(row, 1, item)
            self._items[parameter.name] = item

    def _add_group(self, group: ParameterGroup, add_sub_titles: bool = True) -> None:
        self._create_header(group.name, add_sub_titles)
        for parameter in group:
            if parameter.enabled:
                self._add_parameter(parameter)

    @Slot(BeamParameters)
    def show_beam_parameters(self, beam_parameters: BeamParameters) -> None:
        if len(self._items) == 0:
            self.update_table(beam_parameters)
        self._show_group(beam_parameters.position_and_orientation)
        self._show_group(beam_parameters.width)
        self._show_group(beam_parameters.other_parameters)

    def _show_group(self, group: ParameterGroup) -> None:
        [ self._show_parameter(parameter) for parameter in group ]

    def _show_parameter(self, parameter: Parameter) -> None:
        if parameter.enabled and parameter.name in self._items.keys():
            items = self._items[parameter.name]
            p_value = parameter.value()
            if isinstance(items, tuple) and isinstance(p_value, tuple):
                items[0].setText(str(round(p_value[0], self._round)))
                items[1].setText(str(round(p_value[1], self._round)))
            else:
                items.setText(str(round(p_value, self._round)))
