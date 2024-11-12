# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'camera_property_controller_widget.ui'
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
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QGridLayout, QGroupBox,
    QHBoxLayout, QHeaderView, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

from ..utils.slider_spin_box import SliderSpinBox

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(585, 265)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 2, 2, 2)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.property_dialog_button = QPushButton(Form)
        self.property_dialog_button.setObjectName(u"property_dialog_button")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.property_dialog_button.sizePolicy().hasHeightForWidth())
        self.property_dialog_button.setSizePolicy(sizePolicy)
        self.property_dialog_button.setMinimumSize(QSize(30, 30))
        self.property_dialog_button.setMaximumSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.property_dialog_button)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.camera_info_group_box = QGroupBox(Form)
        self.camera_info_group_box.setObjectName(u"camera_info_group_box")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.camera_info_group_box.sizePolicy().hasHeightForWidth())
        self.camera_info_group_box.setSizePolicy(sizePolicy1)
        self.camera_info_group_box.setMinimumSize(QSize(0, 105))
        self.camera_info_group_box.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout = QHBoxLayout(self.camera_info_group_box)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 0, 5, 5)
        self.camera_info = QTableWidget(self.camera_info_group_box)
        if (self.camera_info.columnCount() < 1):
            self.camera_info.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.camera_info.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if (self.camera_info.rowCount() < 4):
            self.camera_info.setRowCount(4)
        font = QFont()
        font.setBold(True)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        self.camera_info.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font);
        self.camera_info.setVerticalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font);
        self.camera_info.setVerticalHeaderItem(2, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font);
        self.camera_info.setVerticalHeaderItem(3, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.camera_info.setItem(0, 0, __qtablewidgetitem5)
        self.camera_info.setObjectName(u"camera_info")
        self.camera_info.setMinimumSize(QSize(0, 80))
        self.camera_info.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.camera_info.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.camera_info.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored)
        self.camera_info.setSortingEnabled(False)
        self.camera_info.horizontalHeader().setVisible(False)
        self.camera_info.horizontalHeader().setMinimumSectionSize(225)
        self.camera_info.horizontalHeader().setDefaultSectionSize(10000)
        self.camera_info.verticalHeader().setVisible(True)
        self.camera_info.verticalHeader().setCascadingSectionResizes(False)
        self.camera_info.verticalHeader().setMinimumSectionSize(20)
        self.camera_info.verticalHeader().setDefaultSectionSize(20)

        self.horizontalLayout.addWidget(self.camera_info)


        self.verticalLayout.addWidget(self.camera_info_group_box)

        self.camera_settings_group_box = QGroupBox(Form)
        self.camera_settings_group_box.setObjectName(u"camera_settings_group_box")
        self.camera_settings_group_box.setMinimumSize(QSize(0, 100))
        self.camera_settings_group_box.setMaximumSize(QSize(16777215, 16777215))
        self.gridLayout = QGridLayout(self.camera_settings_group_box)
        self.gridLayout.setSpacing(1)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(2, 1, 2, 1)
        self.label_4 = QLabel(self.camera_settings_group_box)
        self.label_4.setObjectName(u"label_4")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy2)
        self.label_4.setMinimumSize(QSize(80, 20))
        self.label_4.setMaximumSize(QSize(80, 20))

        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)

        self.gain_slider = SliderSpinBox(self.camera_settings_group_box)
        self.gain_slider.setObjectName(u"gain_slider")
        sizePolicy2.setHeightForWidth(self.gain_slider.sizePolicy().hasHeightForWidth())
        self.gain_slider.setSizePolicy(sizePolicy2)
        self.gain_slider.setMinimumSize(QSize(0, 20))
        self.gain_slider.setMaximumSize(QSize(500, 20))

        self.gridLayout.addWidget(self.gain_slider, 0, 1, 1, 1)

        self.label_2 = QLabel(self.camera_settings_group_box)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QSize(80, 20))
        self.label_2.setMaximumSize(QSize(80, 20))

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.exposure_slider = SliderSpinBox(self.camera_settings_group_box)
        self.exposure_slider.setObjectName(u"exposure_slider")
        sizePolicy2.setHeightForWidth(self.exposure_slider.sizePolicy().hasHeightForWidth())
        self.exposure_slider.setSizePolicy(sizePolicy2)
        self.exposure_slider.setMinimumSize(QSize(180, 20))
        self.exposure_slider.setMaximumSize(QSize(500, 20))

        self.gridLayout.addWidget(self.exposure_slider, 1, 1, 1, 1)

        self.label_3 = QLabel(self.camera_settings_group_box)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QSize(80, 10))
        self.label_3.setMaximumSize(QSize(80, 20))

        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)

        self.fps_slider = SliderSpinBox(self.camera_settings_group_box)
        self.fps_slider.setObjectName(u"fps_slider")
        sizePolicy2.setHeightForWidth(self.fps_slider.sizePolicy().hasHeightForWidth())
        self.fps_slider.setSizePolicy(sizePolicy2)
        self.fps_slider.setMinimumSize(QSize(180, 20))
        self.fps_slider.setMaximumSize(QSize(500, 20))

        self.gridLayout.addWidget(self.fps_slider, 2, 1, 1, 1)


        self.verticalLayout.addWidget(self.camera_settings_group_box)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Property Controller", None))
        self.property_dialog_button.setText("")
        self.camera_info_group_box.setTitle(QCoreApplication.translate("Form", u"Camera Info", None))
        ___qtablewidgetitem = self.camera_info.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Form", u"Type:", None));
        ___qtablewidgetitem1 = self.camera_info.verticalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Form", u"Name:", None));
        ___qtablewidgetitem2 = self.camera_info.verticalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Form", u"Matrix Shape:", None));
        ___qtablewidgetitem3 = self.camera_info.verticalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Form", u"Pixel Size:", None));

        __sortingEnabled = self.camera_info.isSortingEnabled()
        self.camera_info.setSortingEnabled(False)
        self.camera_info.setSortingEnabled(__sortingEnabled)

        self.camera_settings_group_box.setTitle(QCoreApplication.translate("Form", u"Camera Settings", None))
        self.label_4.setText(QCoreApplication.translate("Form", u"Gain", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Exposure", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"FPS", None))
    # retranslateUi

