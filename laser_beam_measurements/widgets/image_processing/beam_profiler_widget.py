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
from PySide6.QtCore import Slot, Qt, QSettings
from PySide6.QtGui import QPen, QFont
from PySide6.QtWidgets import QTableWidgetItem, QTableWidget
from .ui_beam_profiler_widget import Ui_Form
from laser_beam_measurements.image_processing.beam_profiler import BeamProfiler, CROSS_SECTION_AUTO
from laser_beam_measurements.image_processing import beam_profiler
import numpy
import pyqtgraph as pg
from laser_beam_measurements.utils.colormap import COLORMAPS
from laser_beam_measurements.widgets.utils.custom_graphics_scene_with_cross import CustomGraphicsSceneWithCross
from .beam_profiler_parameter_select_widget import BeamProfilerParameterSelectWidget


__all__ = ["BeamProfilerWidget"]


def _configure_plot(plot_widget: pg.PlotWidget) -> None:
    styles = {'color': 'b', }#'font-size': '8px'}
    plot_widget.setBackground("w")
    plot_widget.setYRange(0, 250)
    plot_widget.setLabel("left", "Intensity", "a.u.", **styles)
    plot_widget.setLabel("bottom", "Dimension", "mkm", **styles)
    plot_widget.showGrid(x=True, y=True)
    plot_widget.addLegend(offset=(1, 1), labelTextColor=[0, 0, 0], labelTextSize='8pt')


class BeamProfilerWidget(ImageProcessorViewerBase):

    DEFAULT_COLORMAP = "Seismic"

    def __init__(self, parent=None):
        super(BeamProfilerWidget, self).__init__(parent, configure_output_scene=True)
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._output_image_scene = CustomGraphicsSceneWithCross(self)
        self.ui.output_beam_view.setScene(self._output_image_scene)
        self._output_image_scene.sceneRectChanged.connect(self.ui.output_beam_view.slot_scene_rect_changed)
        self.setWindowTitle("Beam Profiler")
        self.setObjectName("Beam Profiler")
        self.ui.colormap_combo_box.currentTextChanged.connect(self.slot_set_colormap_for_output)
        self.curve_x: pg.ScatterPlotItem | None = None
        self.curve_y: pg.ScatterPlotItem | None = None
        self.curve_line_x: pg.PlotDataItem | None = None
        self.curve_line_y: pg.PlotDataItem | None = None
        self.flag_gauss_apr: bool = True
        self._configure_plots()
        self._configure_curves()
        self.table_widget_items: dict[str, QTableWidgetItem | tuple[QTableWidgetItem, QTableWidgetItem]] = dict()
        self._fill_colormap_combobox()

        self.ui.show_cross_check_box.toggled.connect(self._slot_show_cross)
        self.ui.auto_cross_check_box.toggled.connect(self._slot_set_cross_auto)
        self.ui.show_cross_check_box.setChecked(True)
        self.ui.auto_cross_check_box.setChecked(True)

        self._connect_signals()

    def _connect_signals(self):
        self.ui.selectParametersPushButton.clicked.connect(self._show_parameter_select_widget)

    @Slot()
    def _show_parameter_select_widget(self) -> None:
        bp_selector = self._image_processor.parameter_selector
        parameter_select_widget = BeamProfilerParameterSelectWidget(bp_selector, parent=self)
        parameter_select_widget.exec_()

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

    def _configure_plots(self):
        _configure_plot(self.ui.cs_plot_x)
        _configure_plot(self.ui.cs_plot_y)

    def _update_parameters(self) -> None:
        pass

    def _fill_colormap_combobox(self) -> None:
        for name in COLORMAPS.get_names():
            self.ui.colormap_combo_box.addItem(name)
        self.ui.colormap_combo_box.setCurrentText(self.DEFAULT_COLORMAP)

    def _connect_processor_signal(self):
        super(BeamProfilerWidget, self)._connect_processor_signal()
        if isinstance(self._image_processor, BeamProfiler):
            self._image_processor.signal_cross_section_updated.connect(self.show_cross_sections)
            self._image_processor.signal_gauss_approximation_updated.connect(self.show_gauss_approximation)
            # self._image_processor.signal_beam_parameters_updated.connect(self.show_beam_parameters)
            self._image_processor.signal_beam_parameters_updated_2.connect(self.ui.tableWidget.show_beam_parameters)
            self._image_processor.parameter_selector.signal_selected.connect(self.ui.tableWidget.update_table)
            self._image_processor.signal_beam_center_updated.connect(self._output_image_scene.cross.slot_set_pos)
            self._output_image_scene.cross.signal_point_changed.connect(self._image_processor.slot_set_center)

    def _disconnect_processor_signal(self):
        super(BeamProfilerWidget, self)._connect_processor_signal()
        if isinstance(self._image_processor, BeamProfiler):
            self._image_processor.signal_cross_section_updated.disconnect(self.show_cross_sections)
            self._image_processor.signal_gauss_approximation_updated.disconnect(self.show_gauss_approximation)
            # self._image_processor.signal_beam_parameters_updated.disconnect(self.show_beam_parameters)
            self._image_processor.signal_beam_parameters_updated_2.disconnect(self.ui.tableWidget.show_beam_parameters)
            self._image_processor.parameter_selector.signal_selected.disconnect(self.ui.tableWidget.update_table)
            self._image_processor.signal_beam_center_updated.disconnect(self._output_image_scene.cross.slot_set_pos)
            self._output_image_scene.cross.signal_point_changed.disconnect(self._image_processor.slot_set_center)

    @Slot(numpy.ndarray, numpy.ndarray, numpy.ndarray, numpy.ndarray)
    def show_cross_sections(self, xx: numpy.ndarray, im_x: numpy.ndarray, yy: numpy.ndarray, im_y: numpy.ndarray) -> None:
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

    def load_widget_settings(self, settings: QSettings) -> None:
        if settings.contains("OutputColormap"):
            colormap_name = str(settings.value("OutputColormap"))
            self.ui.colormap_combo_box.setCurrentText(colormap_name)
        super().load_widget_settings(settings)

    @Slot(bool)
    def _slot_show_cross(self, value: bool) -> None:
        self._output_image_scene.set_cross_visible(value)

    @Slot(bool)
    def _slot_set_cross_auto(self, value: bool) -> None:
        self.signal_parameter_changed.emit(CROSS_SECTION_AUTO, value)
        self._output_image_scene.cross.slot_set_flag_move_enabled(not value)
