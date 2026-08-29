# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'beam_profiler_parameter_select_widget.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QAbstractItemView, QApplication, QCheckBox,
    QDialogButtonBox, QGridLayout, QGroupBox, QHBoxLayout,
    QHeaderView, QLabel, QSizePolicy, QSpacerItem,
    QSpinBox, QTableWidgetItem, QWidget)

from laser_beam_measurements.widgets.utils.parameters_select_table_widget import ParametersSelectTableWidget

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(545, 480)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 2, 2, 2)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.parameters_select_widget = ParametersSelectTableWidget(Form)
        self.parameters_select_widget.setObjectName(u"parameters_select_widget")
        self.parameters_select_widget.setEditTriggers(QAbstractItemView.AllEditTriggers)
        self.parameters_select_widget.horizontalHeader().setMinimumSectionSize(40)
        self.parameters_select_widget.horizontalHeader().setStretchLastSection(True)
        self.parameters_select_widget.verticalHeader().setMinimumSectionSize(20)
        self.parameters_select_widget.verticalHeader().setDefaultSectionSize(20)

        self.gridLayout.addWidget(self.parameters_select_widget, 1, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(Form)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply|QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.Reset)
        self.buttonBox.setCenterButtons(False)

        self.gridLayout.addWidget(self.buttonBox, 1, 1, 1, 1)

        self.average_gb = QGroupBox(Form)
        self.average_gb.setObjectName(u"average_gb")
        self.average_gb.setMinimumSize(QSize(20, 50))
        self.horizontalLayout = QHBoxLayout(self.average_gb)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.average_enable_cb = QCheckBox(self.average_gb)
        self.average_enable_cb.setObjectName(u"average_enable_cb")

        self.horizontalLayout.addWidget(self.average_enable_cb)

        self.horizontalSpacer_2 = QSpacerItem(154, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.average_number_label = QLabel(self.average_gb)
        self.average_number_label.setObjectName(u"average_number_label")

        self.horizontalLayout.addWidget(self.average_number_label)

        self.average_number_sb = QSpinBox(self.average_gb)
        self.average_number_sb.setObjectName(u"average_number_sb")
        self.average_number_sb.setMinimumSize(QSize(50, 0))
        self.average_number_sb.setMinimum(1)
        self.average_number_sb.setMaximum(10)

        self.horizontalLayout.addWidget(self.average_number_sb)

        self.horizontalSpacer = QSpacerItem(154, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.gridLayout.addWidget(self.average_gb, 2, 0, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Select parameters", None))
        self.average_gb.setTitle(QCoreApplication.translate("Form", u"Average Control", None))
        self.average_enable_cb.setText(QCoreApplication.translate("Form", u"Enable", None))
        self.average_number_label.setText(QCoreApplication.translate("Form", u"Count", None))
    # retranslateUi

