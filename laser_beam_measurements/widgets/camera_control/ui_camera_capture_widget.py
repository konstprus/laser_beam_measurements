# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera_capture_widget.ui'
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
    QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

from ..utils.custom_graphics_view import CustomGraphicsView
from ..utils.slider_spin_box import SliderSpinBox

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(509, 510)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(1, 1, 0, 1)
        self.buttonsGroupBox = QGroupBox(Form)
        self.buttonsGroupBox.setObjectName(u"buttonsGroupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonsGroupBox.sizePolicy().hasHeightForWidth())
        self.buttonsGroupBox.setSizePolicy(sizePolicy)
        self.buttonsGroupBox.setMinimumSize(QSize(0, 40))
        self.buttonsGroupBox.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout = QHBoxLayout(self.buttonsGroupBox)
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setContentsMargins(1, 1, 1, 1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.start_button = QPushButton(self.buttonsGroupBox)
        self.start_button.setObjectName(u"start_button")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy1)
        self.start_button.setMaximumSize(QSize(35, 30))
        self.start_button.setIconSize(QSize(25, 25))
        self.start_button.setCheckable(True)
        self.start_button.setChecked(False)

        self.horizontalLayout.addWidget(self.start_button)

        self.save_image_button = QPushButton(self.buttonsGroupBox)
        self.save_image_button.setObjectName(u"save_image_button")
        sizePolicy1.setHeightForWidth(self.save_image_button.sizePolicy().hasHeightForWidth())
        self.save_image_button.setSizePolicy(sizePolicy1)
        self.save_image_button.setMaximumSize(QSize(35, 30))
        self.save_image_button.setStyleSheet(u"")
        self.save_image_button.setIconSize(QSize(24, 24))
        self.save_image_button.setCheckable(False)

        self.horizontalLayout.addWidget(self.save_image_button)

        self.horizontalSpacer = QSpacerItem(185, 18, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.buttonsGroupBox)

        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setMinimumSize(QSize(0, 100))
        self.groupBox.setMaximumSize(QSize(16777215, 100))
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 1, 2, 1)
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QSize(80, 20))
        self.label_4.setMaximumSize(QSize(80, 20))

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.gain_slider = SliderSpinBox(self.groupBox)
        self.gain_slider.setObjectName(u"gain_slider")
        sizePolicy.setHeightForWidth(self.gain_slider.sizePolicy().hasHeightForWidth())
        self.gain_slider.setSizePolicy(sizePolicy)
        self.gain_slider.setMinimumSize(QSize(0, 20))
        self.gain_slider.setMaximumSize(QSize(500, 20))

        self.gridLayout.addWidget(self.gain_slider, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        sizePolicy1.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy1)
        self.label_2.setMinimumSize(QSize(80, 20))
        self.label_2.setMaximumSize(QSize(80, 20))

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.exposure_slider = SliderSpinBox(self.groupBox)
        self.exposure_slider.setObjectName(u"exposure_slider")
        sizePolicy.setHeightForWidth(self.exposure_slider.sizePolicy().hasHeightForWidth())
        self.exposure_slider.setSizePolicy(sizePolicy)
        self.exposure_slider.setMinimumSize(QSize(180, 20))
        self.exposure_slider.setMaximumSize(QSize(500, 20))

        self.gridLayout.addWidget(self.exposure_slider, 1, 1, 1, 1)

        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setMinimumSize(QSize(80, 10))
        self.label_3.setMaximumSize(QSize(80, 20))

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.fps_slider = SliderSpinBox(self.groupBox)
        self.fps_slider.setObjectName(u"fps_slider")
        sizePolicy.setHeightForWidth(self.fps_slider.sizePolicy().hasHeightForWidth())
        self.fps_slider.setSizePolicy(sizePolicy)
        self.fps_slider.setMinimumSize(QSize(180, 20))
        self.fps_slider.setMaximumSize(QSize(500, 20))

        self.gridLayout.addWidget(self.fps_slider, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.groupBox)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.colormap_combo_box = QComboBox(Form)
        self.colormap_combo_box.setObjectName(u"colormap_combo_box")

        self.horizontalLayout_3.addWidget(self.colormap_combo_box)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

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
        self.buttonsGroupBox.setTitle("")
#if QT_CONFIG(tooltip)
        self.start_button.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Connect to camera</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.start_button.setText(QCoreApplication.translate("Form", u"Start", None))
#if QT_CONFIG(tooltip)
        self.save_image_button.setToolTip(QCoreApplication.translate("Form", u"<html><head/><body><p>Save Image</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.save_image_button.setText(QCoreApplication.translate("Form", u"Save", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Camera Settings", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Gain", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Exposure", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"FPS", None))
        self.label.setText(QCoreApplication.translate("Form", u"Colormap", None))
        self.fps_label.setText(QCoreApplication.translate("Form", u"FPS (Actual):   ", None))
        self.frames_label.setText(QCoreApplication.translate("Form", u"Frames:", None))
        self.errors_label.setText(QCoreApplication.translate("Form", u"Errors:", None))
    # retranslateUi

