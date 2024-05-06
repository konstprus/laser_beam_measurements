# 
# Project: laser_beam_measurements
#
# File: beam_profiler_widget.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

# pyside6-uic laser_beam_measurements/widgets/image_processing/beam_profiler_widget.ui -o laser_beam_measurements/widgets/image_processing/ui_beam_profiler_widget.py


from laser_beam_measurements.image_processing.image_processor_viewer_base import ImageProcessorViewerBase
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QPen, QFont
from PySide6.QtWidgets import QTableWidgetItem, QTableWidget
from .ui_beam_profiler_widget import Ui_Form
from laser_beam_measurements.image_processing.beam_profiler import BeamProfiler
from laser_beam_measurements.image_processing import beam_profiler
import numpy
import pyqtgraph as pg


__all__ = ["BeamProfilerWidget"]


def _create_table_item(text: str,
                       color: Qt.GlobalColor | None = None,
                       flags: Qt.ItemFlag = Qt.ItemFlag.ItemIsEnabled,
                       bold: bool = False,
                       alignment: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter) -> QTableWidgetItem:
    item = QTableWidgetItem(text)
    if color:
        item.setBackground(color)
    if flags:
        item.setFlags(flags)
    if bold:
        font = QFont()
        font.setBold(bold)
        item.setFont(font)
    if alignment:
        item.setTextAlignment(alignment)
    return item


def _create_table_header(
        table_widget: QTableWidget,
        row_number: int,
        title: str = '',
        sub_titles: list | tuple | None = None) -> int:
    number = 1
    if sub_titles is not None:
        number = 2
    table_widget.setRowCount(row_number + number)
    table_widget.setSpan(row_number, 0, 1, 4)
    table_widget.setItem(row_number, 0, _create_table_item(title, Qt.GlobalColor.lightGray, bold=True))
    if isinstance(sub_titles, (list, tuple)):
        for index, value in enumerate(sub_titles):
            table_widget.setItem(row_number + 1, index, _create_table_item(value, Qt.GlobalColor.lightGray, bold=True))
    return table_widget.rowCount()


class BeamProfilerWidget(ImageProcessorViewerBase):

    def __init__(self, parent=None):
        super(BeamProfilerWidget, self).__init__(parent, configure_output_scene=True)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.output_beam_view.setScene(self._output_image_scene)
        self.setWindowTitle("Beam Profiler")
        self.setObjectName("Beam Profiler")

        self.curve_x = None
        self.curve_y = None
        self.curve_line_x = None
        self.curve_line_y = None
        self.flag_gauss_apr = True
        self._configure_curves()
        self.table_widget_items: dict[str, QTableWidgetItem | tuple[QTableWidgetItem, QTableWidgetItem]] = dict()

    def _configure_curves(self):
        self.curve_x = pg.ScatterPlotItem(name="X cross section")
        self.curve_x.setPen(QPen(Qt.GlobalColor.red, 0))
        self.curve_x.setBrush(pg.mkBrush(color='r'))
        self.curve_x.setSize(4)
        self.ui.cs_plot_x.addItem(self.curve_x)

        self.curve_line_x = pg.PlotDataItem(name="X gauss appr")
        self.curve_line_x.setPen(pg.mkPen(color='#800000', width=2))
        self.ui.cs_plot_x.addItem(self.curve_line_x)

        self.curve_y = pg.ScatterPlotItem(name="Y cross section")
        self.curve_y.setPen(QPen(Qt.GlobalColor.blue, 0))
        self.curve_y.setBrush(pg.mkBrush(color='b'))
        self.curve_y.setSize(4)
        self.ui.cs_plot_y.addItem(self.curve_y)

        self.curve_line_y = pg.PlotDataItem(name="Y gauss appr")
        self.curve_line_y.setPen(pg.mkPen(color='#000080', width=2))
        self.ui.cs_plot_y.addItem(self.curve_line_y)

    def _update_parameters(self) -> None:
        pass

    def _connect_processor_signal(self):
        super(BeamProfilerWidget, self)._connect_processor_signal()
        if isinstance(self._image_processor, BeamProfiler):
            self._image_processor.signal_cross_section_updated.connect(self.show_cross_sections)
            self._image_processor.signal_gauss_approximation_updated.connect(self.show_gauss_approximation)
            self._image_processor.signal_beam_parameters_updated.connect(self.show_beam_parameters)

    def _disconnect_processor_signal(self):
        super(BeamProfilerWidget, self)._connect_processor_signal()
        if isinstance(self._image_processor, BeamProfiler):
            self._image_processor.signal_cross_section_updated.disconnect(self.show_cross_sections)
            self._image_processor.signal_gauss_approximation_updated.disconnect(self.show_gauss_approximation)
            self._image_processor.signal_beam_parameters_updated.disconnect(self.show_beam_parameters)

    @Slot(numpy.ndarray, numpy.ndarray)
    def show_cross_sections(self, im_x: numpy.ndarray, im_y: numpy.ndarray) -> None:
        xx = numpy.arange(-len(im_x) / 2, len(im_x) / 2)
        yy = numpy.arange(-len(im_y) / 2, len(im_y) / 2)
        self._update_curves(xx, im_x, yy, im_y)

    def _update_curves(self,
                       xx: numpy.ndarray, curve_x: numpy.ndarray,
                       yy: numpy.ndarray, curve_y: numpy.ndarray) -> None:
        self.curve_x.setData(x=xx, y=curve_x)
        self.curve_y.setData(x=yy, y=curve_y)

    @Slot(numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray)
    def show_gauss_approximation(self, xx, model_x, yy, model_y):
        self._update_apr_curves(xx, model_x, yy, model_y)

    def _update_apr_curves(self,
                           xx: numpy.ndarray, curve_x: numpy.ndarray,
                           yy: numpy.ndarray, curve_y: numpy.ndarray) -> None:
        self.curve_line_x.setData(x=xx, y=curve_x)
        self.curve_line_y.setData(x=yy, y=curve_y)

    def configure_table_widget(self, parameters_dict: dict[str, dict[str, object]]) -> None:
        table_widget = self.ui.tableWidget

        self.ui.tableWidget.verticalHeader().hide()
        self.ui.tableWidget.horizontalHeader().hide()
        self.ui.tableWidget.setColumnCount(4)

        self.table_widget_items.clear()

        row_number = 0

        sub_titles = ('', 'Axis X', 'Axis Y', '')

        if beam_profiler.BEAM_POSITION_AND_ORIENTATION in parameters_dict.keys():
            row_number = _create_table_header(
                table_widget, row_number, beam_profiler.BEAM_POSITION_AND_ORIENTATION, sub_titles
            )
            position_and_orientation = parameters_dict[beam_profiler.BEAM_POSITION_AND_ORIENTATION]
            number_of_rows_to_add = len(position_and_orientation.keys())
            table_widget.setRowCount(row_number+number_of_rows_to_add)
            position_to_add = 0
            if beam_profiler.BeamPositionAndOrientation.GLOBAL in position_and_orientation.keys():
                item_title = _create_table_item(
                    beam_profiler.BeamPositionAndOrientation.GLOBAL, alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                table_widget.setItem(row_number + position_to_add, 0, item_title)
                item_x = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                item_y = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                table_widget.setItem(row_number + position_to_add, 1, item_x)
                table_widget.setItem(row_number + position_to_add, 2, item_y)
                self.table_widget_items.update({beam_profiler.BeamPositionAndOrientation.GLOBAL: (item_x, item_y)})
                position_to_add += 1

            if beam_profiler.BeamPositionAndOrientation.LOCAL in position_and_orientation.keys():
                item_title = _create_table_item(
                    beam_profiler.BeamPositionAndOrientation.LOCAL, alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                table_widget.setItem(row_number + position_to_add, 0, item_title)
                item_x = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                item_y = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )

                table_widget.setItem(row_number + position_to_add, 1, item_x)
                table_widget.setItem(row_number + position_to_add, 2, item_y)
                self.table_widget_items.update({beam_profiler.BeamPositionAndOrientation.LOCAL: (item_x, item_y)})
                position_to_add += 1

            if beam_profiler.BeamPositionAndOrientation.ANGLE in position_and_orientation.keys():
                item_title = _create_table_item(
                    beam_profiler.BeamPositionAndOrientation.ANGLE, alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                table_widget.setItem(row_number + position_to_add, 0, item_title)
                item = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )

                table_widget.setItem(row_number + position_to_add, 1, item)
                self.table_widget_items.update({beam_profiler.BeamPositionAndOrientation.ANGLE: item})
                position_to_add += 1

            row_number = table_widget.rowCount()

        if beam_profiler.BEAM_WIDTH_METHODS in parameters_dict.keys():
            row_number = _create_table_header(
                table_widget, row_number, beam_profiler.BEAM_WIDTH_METHODS, sub_titles
            )
            widths = parameters_dict[beam_profiler.BEAM_WIDTH_METHODS]
            number_of_rows_to_add = len(widths.keys())
            table_widget.setRowCount(row_number+number_of_rows_to_add)
            position_to_add = 0
            if beam_profiler.BeamWidthMethods.FOUR_SIGMA in widths.keys():
                item_title = _create_table_item(
                    beam_profiler.BeamWidthMethods.FOUR_SIGMA, alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                table_widget.setItem(row_number + position_to_add, 0, item_title)
                item_x = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                item_y = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )

                table_widget.setItem(row_number + position_to_add, 1, item_x)
                table_widget.setItem(row_number + position_to_add, 2, item_y)
                self.table_widget_items.update({beam_profiler.BeamWidthMethods.FOUR_SIGMA: (item_x, item_y)})
                position_to_add += 1

            if beam_profiler.BeamWidthMethods.GAUSS_APPR in widths.keys():
                item_title = _create_table_item(
                    beam_profiler.BeamWidthMethods.GAUSS_APPR, alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                table_widget.setItem(row_number + position_to_add, 0, item_title)
                item_x = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                item_y = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )

                table_widget.setItem(row_number + position_to_add, 1, item_x)
                table_widget.setItem(row_number + position_to_add, 2, item_y)
                self.table_widget_items.update({beam_profiler.BeamWidthMethods.GAUSS_APPR: (item_x, item_y)})
                position_to_add += 1

            if beam_profiler.BeamWidthMethods.LEVELED_135 in widths.keys():
                item_title = _create_table_item(
                    beam_profiler.BeamWidthMethods.LEVELED_135, alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                table_widget.setItem(row_number + position_to_add, 0, item_title)
                item_x = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                item_y = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )

                table_widget.setItem(row_number + position_to_add, 1, item_x)
                table_widget.setItem(row_number + position_to_add, 2, item_y)
                self.table_widget_items.update({beam_profiler.BeamWidthMethods.LEVELED_135: (item_x, item_y)})
                position_to_add += 1

            if beam_profiler.BeamWidthMethods.POWER_86 in widths.keys():
                item_title = _create_table_item(
                    beam_profiler.BeamWidthMethods.POWER_86, alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                table_widget.setItem(row_number + position_to_add, 0, item_title)
                item = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )

                table_widget.setItem(row_number + position_to_add, 1, item)
                self.table_widget_items.update({beam_profiler.BeamWidthMethods.POWER_86: item})
                position_to_add += 1

            row_number = table_widget.rowCount()

        if beam_profiler.OTHER_PARAMETERS in parameters_dict.keys():
            row_number = _create_table_header(
                table_widget, row_number, beam_profiler.OTHER_PARAMETERS
            )
            other_parameters = parameters_dict[beam_profiler.OTHER_PARAMETERS]
            number_of_rows_to_add = len(other_parameters.keys())
            table_widget.setRowCount(row_number + number_of_rows_to_add)
            position_to_add = 0
            if beam_profiler.OtherParameters.POWER in other_parameters.keys():
                item_title = _create_table_item(
                    beam_profiler.OtherParameters.POWER, alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                table_widget.setItem(row_number + position_to_add, 0, item_title)
                item = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )

                table_widget.setItem(row_number + position_to_add, 1, item)
                self.table_widget_items.update({beam_profiler.OtherParameters.POWER: item})
                position_to_add += 1

            if beam_profiler.OtherParameters.AREA in other_parameters.keys():
                item_title = _create_table_item(
                    beam_profiler.OtherParameters.AREA, alignment=Qt.AlignRight | Qt.AlignVCenter
                )
                table_widget.setItem(row_number + position_to_add, 0, item_title)
                item = _create_table_item(
                    "", alignment=Qt.AlignRight | Qt.AlignVCenter
                )

                table_widget.setItem(row_number + position_to_add, 1, item)
                self.table_widget_items.update({beam_profiler.OtherParameters.AREA: item})
                position_to_add += 1

    @Slot(dict)
    def show_beam_parameters(self, parameters_dict: dict[str, dict[str, float | tuple[float, float]]]) -> None:
        # print(parameters_dict)
        # tableWidget = self.ui.tableWidget
        if len(self.table_widget_items.keys()) == 0:
            self.configure_table_widget(parameters_dict)
        for _, value in parameters_dict.items():
            for key, p_value in value.items():
                # print(key, p_value)
                # print(self.table_widget_items.keys())
                if key in self.table_widget_items.keys():
                    item_or_items = self.table_widget_items[key]
                    if isinstance(item_or_items, tuple) and isinstance(p_value, tuple):
                        item_or_items[0].setText(str(round(p_value[0], 2)))
                        item_or_items[1].setText(str(round(p_value[1], 2)))
                    else:
                        item_or_items.setText(str(round(p_value, 2)))

    def _set_item_value(self, row, column, value):
        value_ = str(round(value, 2))
        if self.ui.tableWidget.item(row, column):
            self.ui.tableWidget.item(row, column).setText(value_)
        else:
            self.ui.tableWidget.setItem(row, column, QTableWidgetItem(value_))
