# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'parameter_logger_widget.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(815, 386)
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(5, 5, 5, 5)
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(200, 0))
        self.groupBox.setMaximumSize(QSize(200, 16777215))
        self.available_parameters = QListWidget(self.groupBox)
        self.available_parameters.setObjectName(u"available_parameters")
        self.available_parameters.setGeometry(QRect(10, 20, 181, 192))
        self.start_stop_button = QPushButton(self.groupBox)
        self.start_stop_button.setObjectName(u"start_stop_button")
        self.start_stop_button.setGeometry(QRect(10, 220, 75, 24))
        self.time_step = QLineEdit(self.groupBox)
        self.time_step.setObjectName(u"time_step")
        self.time_step.setGeometry(QRect(10, 250, 81, 22))
        self.time_unit = QComboBox(self.groupBox)
        self.time_unit.addItem("")
        self.time_unit.addItem("")
        self.time_unit.setObjectName(u"time_unit")
        self.time_unit.setGeometry(QRect(100, 250, 69, 22))

        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.plot = PlotWidget(Form)
        self.plot.setObjectName(u"plot")

        self.verticalLayout.addWidget(self.plot)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.select_parameter = QComboBox(Form)
        self.select_parameter.setObjectName(u"select_parameter")
        self.select_parameter.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.select_parameter)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 1, 1)

        self.status_label = QLabel(Form)
        self.status_label.setObjectName(u"status_label")
        self.status_label.setMinimumSize(QSize(0, 20))
        self.status_label.setMaximumSize(QSize(16777215, 20))

        self.gridLayout.addWidget(self.status_label, 1, 0, 1, 2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Parameter Logger", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Controls", None))
        self.start_stop_button.setText(QCoreApplication.translate("Form", u"Start", None))
        self.time_unit.setItemText(0, QCoreApplication.translate("Form", u"sec", None))
        self.time_unit.setItemText(1, QCoreApplication.translate("Form", u"min", None))

        self.status_label.setText(QCoreApplication.translate("Form", u"Counts:", None))
    # retranslateUi

