#
# Project: laser_beam_measurements
#
# File: item_model.py
#
# Author: Konstantin Prusakov
#
# Copyright 2026 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from PySide6.QtCore import QObject, QAbstractTableModel, QModelIndex
from PySide6.QtCore import Qt
from typing import Any, Optional, Union

from .parameter_group import ParameterGroup

class ParameterGroupItemModel(QAbstractTableModel):

    def __init__(self,
                 group : ParameterGroup,
                 vertical_headers: Union[list, tuple] = ("Axis X", "Axis Y"),
                 parent: Optional[QObject] = None):
        super().__init__(parent)
        self._enabled_parameters: list[str] = []
        self._vertical_headers: list[str] = list(vertical_headers)
        self._group: ParameterGroup = group
        for p in self._group:
            if p.enabled:
                self._enabled_parameters.append(p.name)

    def rowCount(self, parent = None) -> int:
        return len(self._enabled_parameters)

    def columnCount(self, parent = None) -> int:
        return len(self._vertical_headers)

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole = Qt.ItemDataRole.DisplayRole) -> Any:
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            if section < len(self._enabled_parameters):
                return self._group.get_parameter(self._enabled_parameters[section]).verbose_name
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            if section < len(self._vertical_headers):
                return self._vertical_headers[section]
        return None

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid():
            if role == Qt.ItemDataRole.DisplayRole:
                r, c = index.row(), index.column()
                parameter = self._group.get_parameter(self._enabled_parameters[r])
                return parameter.value(axis=c)

        return None

    def update(self) -> None:
        self._enabled_parameters.clear()
        [self._enabled_parameters.append(p.name) for p in self._group if p.enabled]
        # for p in self._group:
        #     if p.enabled:
        #         self._enabled_parameters.append(p.name)
        self.layoutChanged.emit()

    def flags(self, index: QModelIndex):
        return Qt.ItemFlag.ItemIsEnabled