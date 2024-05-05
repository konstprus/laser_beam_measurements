# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera_display.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QHBoxLayout, QLabel,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from ..utils.custom_graphics_view import CustomGraphicsView

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(638, 505)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 2, 2, 2)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout.addWidget(self.label)

        self.colormap_combo_box = QComboBox(Form)
        self.colormap_combo_box.setObjectName(u"colormap_combo_box")

        self.horizontalLayout.addWidget(self.colormap_combo_box)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.graphicsView = CustomGraphicsView(Form)
        self.graphicsView.setObjectName(u"graphicsView")

        self.verticalLayout.addWidget(self.graphicsView)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.fps_label = QLabel(Form)
        self.fps_label.setObjectName(u"fps_label")

        self.horizontalLayout_2.addWidget(self.fps_label)

        self.frames_label = QLabel(Form)
        self.frames_label.setObjectName(u"frames_label")

        self.horizontalLayout_2.addWidget(self.frames_label)

        self.errors_label = QLabel(Form)
        self.errors_label.setObjectName(u"errors_label")

        self.horizontalLayout_2.addWidget(self.errors_label)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.label.setText(QCoreApplication.translate("Form", u"Colormap", None))
        self.fps_label.setText(QCoreApplication.translate("Form", u"FPS (Actual):   ", None))
        self.frames_label.setText(QCoreApplication.translate("Form", u"Frames:", None))
        self.errors_label.setText(QCoreApplication.translate("Form", u"Errors:", None))
    # retranslateUi

