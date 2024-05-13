# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'beam_profiler_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGroupBox,
    QHBoxLayout, QHeaderView, QSizePolicy, QSpacerItem,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)

from ..utils.custom_graphics_view import CustomGraphicsView
from pyqtgraph import PlotWidget

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(934, 616)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setFlat(False)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.enable_check_box = QCheckBox(self.groupBox)
        self.enable_check_box.setObjectName(u"enable_check_box")

        self.verticalLayout.addWidget(self.enable_check_box)

        self.colormap_groub_box = QGroupBox(self.groupBox)
        self.colormap_groub_box.setObjectName(u"colormap_groub_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.colormap_groub_box.sizePolicy().hasHeightForWidth())
        self.colormap_groub_box.setSizePolicy(sizePolicy1)
        self.colormap_groub_box.setMinimumSize(QSize(120, 48))
        self.colormap_groub_box.setMaximumSize(QSize(120, 48))
        self.colormap_combo_box = QComboBox(self.colormap_groub_box)
        self.colormap_combo_box.setObjectName(u"colormap_combo_box")
        self.colormap_combo_box.setGeometry(QRect(10, 18, 100, 20))

        self.verticalLayout.addWidget(self.colormap_groub_box)

        self.verticalSpacer = QSpacerItem(20, 210, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout_2.addWidget(self.groupBox)

        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.output_beam_view = CustomGraphicsView(Form)
        self.output_beam_view.setObjectName(u"output_beam_view")

        self.horizontalLayout.addWidget(self.output_beam_view)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.cs_plot_x = PlotWidget(Form)
        self.cs_plot_x.setObjectName(u"cs_plot_x")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cs_plot_x.sizePolicy().hasHeightForWidth())
        self.cs_plot_x.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.cs_plot_x)

        self.cs_plot_y = PlotWidget(Form)
        self.cs_plot_y.setObjectName(u"cs_plot_y")

        self.verticalLayout_2.addWidget(self.cs_plot_y)


        self.horizontalLayout.addLayout(self.verticalLayout_2)


        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.tableWidget = QTableWidget(Form)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setShowGrid(True)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setMinimumSectionSize(20)
        self.tableWidget.verticalHeader().setDefaultSectionSize(20)

        self.verticalLayout_3.addWidget(self.tableWidget)


        self.horizontalLayout_2.addLayout(self.verticalLayout_3)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Controls", None))
        self.enable_check_box.setText(QCoreApplication.translate("Form", u"Enable", None))
        self.colormap_groub_box.setTitle(QCoreApplication.translate("Form", u"Colormap", None))
    # retranslateUi

