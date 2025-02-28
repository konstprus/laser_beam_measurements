# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'beam_finder_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDoubleSpinBox,
    QGroupBox, QHBoxLayout, QLabel, QSizePolicy,
    QSpacerItem, QSplitter, QVBoxLayout, QWidget)

from ..utils.custom_graphics_view import CustomGraphicsView
from ..utils.roi_control_widget import ROIControl

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(858, 561)
        self.horizontalLayout = QHBoxLayout(Form)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.groupBox = QGroupBox(Form)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(True)
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.enable_check_box = QCheckBox(self.groupBox)
        self.enable_check_box.setObjectName(u"enable_check_box")

        self.verticalLayout.addWidget(self.enable_check_box)

        self.rotation_group_box = QGroupBox(self.groupBox)
        self.rotation_group_box.setObjectName(u"rotation_group_box")
        self.rotation_group_box.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rotation_group_box.sizePolicy().hasHeightForWidth())
        self.rotation_group_box.setSizePolicy(sizePolicy)
        self.rotation_group_box.setMinimumSize(QSize(120, 70))
        self.rotation_group_box.setMaximumSize(QSize(120, 70))
        self.rotation_group_box.setFlat(False)
        self.rotation_group_box.setCheckable(True)
        self.rotation_group_box.setChecked(True)
        self.angle_label = QLabel(self.rotation_group_box)
        self.angle_label.setObjectName(u"angle_label")
        self.angle_label.setGeometry(QRect(8, 38, 40, 20))
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.angle_label.sizePolicy().hasHeightForWidth())
        self.angle_label.setSizePolicy(sizePolicy1)
        self.angle_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.angle_value_spin_box = QDoubleSpinBox(self.rotation_group_box)
        self.angle_value_spin_box.setObjectName(u"angle_value_spin_box")
        self.angle_value_spin_box.setGeometry(QRect(50, 38, 60, 20))
        self.angle_value_spin_box.setMaximumSize(QSize(60, 20))
        self.angle_value_spin_box.setDecimals(1)
        self.angle_value_spin_box.setMinimum(-45.000000000000000)
        self.angle_value_spin_box.setMaximum(45.000000000000000)

        self.verticalLayout.addWidget(self.rotation_group_box)

        self.roi_controls_group_box = QGroupBox(self.groupBox)
        self.roi_controls_group_box.setObjectName(u"roi_controls_group_box")
        sizePolicy.setHeightForWidth(self.roi_controls_group_box.sizePolicy().hasHeightForWidth())
        self.roi_controls_group_box.setSizePolicy(sizePolicy)
        self.roi_controls_group_box.setMinimumSize(QSize(120, 200))
        self.roi_controls_group_box.setMaximumSize(QSize(120, 200))
        self.roi_controls_group_box.setCheckable(True)
        self.roi_controls_group_box.setChecked(False)
        self.verticalLayout_2 = QVBoxLayout(self.roi_controls_group_box)
        self.verticalLayout_2.setSpacing(4)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(8, 0, 8, 4)
        self.find_auto_check_box = QCheckBox(self.roi_controls_group_box)
        self.find_auto_check_box.setObjectName(u"find_auto_check_box")
        self.find_auto_check_box.setMinimumSize(QSize(0, 20))
        self.find_auto_check_box.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_2.addWidget(self.find_auto_check_box)

        self.checkBox = QCheckBox(self.roi_controls_group_box)
        self.checkBox.setObjectName(u"checkBox")
        self.checkBox.setMinimumSize(QSize(0, 20))
        self.checkBox.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_2.addWidget(self.checkBox)

        self.rotation_auto_check_box = QCheckBox(self.roi_controls_group_box)
        self.rotation_auto_check_box.setObjectName(u"rotation_auto_check_box")
        self.rotation_auto_check_box.setMinimumSize(QSize(0, 20))
        self.rotation_auto_check_box.setMaximumSize(QSize(16777215, 20))

        self.verticalLayout_2.addWidget(self.rotation_auto_check_box)

        self.roi_x = ROIControl(self.roi_controls_group_box)
        self.roi_x.setObjectName(u"roi_x")
        sizePolicy.setHeightForWidth(self.roi_x.sizePolicy().hasHeightForWidth())
        self.roi_x.setSizePolicy(sizePolicy)
        self.roi_x.setMinimumSize(QSize(102, 20))

        self.verticalLayout_2.addWidget(self.roi_x)

        self.roi_y = ROIControl(self.roi_controls_group_box)
        self.roi_y.setObjectName(u"roi_y")
        sizePolicy.setHeightForWidth(self.roi_y.sizePolicy().hasHeightForWidth())
        self.roi_y.setSizePolicy(sizePolicy)
        self.roi_y.setMinimumSize(QSize(102, 20))

        self.verticalLayout_2.addWidget(self.roi_y)

        self.roi_w = ROIControl(self.roi_controls_group_box)
        self.roi_w.setObjectName(u"roi_w")
        sizePolicy.setHeightForWidth(self.roi_w.sizePolicy().hasHeightForWidth())
        self.roi_w.setSizePolicy(sizePolicy)
        self.roi_w.setMinimumSize(QSize(102, 20))

        self.verticalLayout_2.addWidget(self.roi_w)

        self.roi_h = ROIControl(self.roi_controls_group_box)
        self.roi_h.setObjectName(u"roi_h")
        sizePolicy.setHeightForWidth(self.roi_h.sizePolicy().hasHeightForWidth())
        self.roi_h.setSizePolicy(sizePolicy)
        self.roi_h.setMinimumSize(QSize(102, 20))

        self.verticalLayout_2.addWidget(self.roi_h)

        self.roi_a = ROIControl(self.roi_controls_group_box)
        self.roi_a.setObjectName(u"roi_a")
        sizePolicy.setHeightForWidth(self.roi_a.sizePolicy().hasHeightForWidth())
        self.roi_a.setSizePolicy(sizePolicy)
        self.roi_a.setMinimumSize(QSize(102, 20))

        self.verticalLayout_2.addWidget(self.roi_a)


        self.verticalLayout.addWidget(self.roi_controls_group_box)

        self.noise_group_box = QGroupBox(self.groupBox)
        self.noise_group_box.setObjectName(u"noise_group_box")
        self.noise_group_box.setEnabled(True)
        sizePolicy.setHeightForWidth(self.noise_group_box.sizePolicy().hasHeightForWidth())
        self.noise_group_box.setSizePolicy(sizePolicy)
        self.noise_group_box.setMinimumSize(QSize(120, 48))
        self.noise_group_box.setMaximumSize(QSize(120, 48))
        self.noise_group_box.setBaseSize(QSize(1, 1))
        self.noise_group_box.setMouseTracking(False)
        self.noise_group_box.setTabletTracking(False)
        self.noise_group_box.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.noise_group_box.setContextMenuPolicy(Qt.ContextMenuPolicy.DefaultContextMenu)
        self.noise_group_box.setAcceptDrops(False)
        self.noise_group_box.setToolTipDuration(-1)
        self.noise_group_box.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.noise_group_box.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.noise_group_box.setFlat(False)
        self.noise_group_box.setCheckable(True)
        self.noise_group_box.setChecked(True)
        self.noise_label = QLabel(self.noise_group_box)
        self.noise_label.setObjectName(u"noise_label")
        self.noise_label.setGeometry(QRect(8, 18, 40, 20))
        sizePolicy1.setHeightForWidth(self.noise_label.sizePolicy().hasHeightForWidth())
        self.noise_label.setSizePolicy(sizePolicy1)
        self.noise_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.noise_value_spin_box = QDoubleSpinBox(self.noise_group_box)
        self.noise_value_spin_box.setObjectName(u"noise_value_spin_box")
        self.noise_value_spin_box.setGeometry(QRect(50, 18, 60, 20))
        self.noise_value_spin_box.setMaximumSize(QSize(60, 20))
        self.noise_value_spin_box.setDecimals(1)
        self.noise_value_spin_box.setMinimum(-45.000000000000000)
        self.noise_value_spin_box.setMaximum(45.000000000000000)

        self.verticalLayout.addWidget(self.noise_group_box)

        self.colormap_groub_box = QGroupBox(self.groupBox)
        self.colormap_groub_box.setObjectName(u"colormap_groub_box")
        sizePolicy.setHeightForWidth(self.colormap_groub_box.sizePolicy().hasHeightForWidth())
        self.colormap_groub_box.setSizePolicy(sizePolicy)
        self.colormap_groub_box.setMinimumSize(QSize(120, 48))
        self.colormap_groub_box.setMaximumSize(QSize(120, 48))
        self.colormap_combo_box = QComboBox(self.colormap_groub_box)
        self.colormap_combo_box.setObjectName(u"colormap_combo_box")
        self.colormap_combo_box.setGeometry(QRect(10, 18, 100, 20))

        self.verticalLayout.addWidget(self.colormap_groub_box)

        self.verticalSpacer = QSpacerItem(20, 210, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addWidget(self.groupBox)

        self.splitter = QSplitter(Form)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.input_beam_view = CustomGraphicsView(self.splitter)
        self.input_beam_view.setObjectName(u"input_beam_view")
        self.splitter.addWidget(self.input_beam_view)

        self.horizontalLayout.addWidget(self.splitter)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.groupBox.setTitle(QCoreApplication.translate("Form", u"Controls", None))
        self.enable_check_box.setText(QCoreApplication.translate("Form", u"Enable", None))
        self.rotation_group_box.setTitle(QCoreApplication.translate("Form", u"Rotation", None))
        self.angle_label.setText(QCoreApplication.translate("Form", u"Angle:", None))
        self.roi_controls_group_box.setTitle(QCoreApplication.translate("Form", u"ROI", None))
        self.find_auto_check_box.setText(QCoreApplication.translate("Form", u"Find Auto", None))
        self.checkBox.setText(QCoreApplication.translate("Form", u"Rotation", None))
        self.rotation_auto_check_box.setText(QCoreApplication.translate("Form", u"Rotation Auto", None))
#if QT_CONFIG(tooltip)
        self.noise_group_box.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.noise_group_box.setTitle(QCoreApplication.translate("Form", u"Noise", None))
        self.noise_label.setText(QCoreApplication.translate("Form", u"Level", None))
        self.colormap_groub_box.setTitle(QCoreApplication.translate("Form", u"Colormap", None))
    # retranslateUi

