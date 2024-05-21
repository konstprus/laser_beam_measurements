# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGroupBox, QHBoxLayout,
    QLabel, QMainWindow, QMdiArea, QMenuBar,
    QPushButton, QSizePolicy, QSpacerItem, QStatusBar,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(862, 659)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsGroupBox = QGroupBox(self.centralwidget)
        self.buttonsGroupBox.setObjectName(u"buttonsGroupBox")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonsGroupBox.sizePolicy().hasHeightForWidth())
        self.buttonsGroupBox.setSizePolicy(sizePolicy)
        self.buttonsGroupBox.setMinimumSize(QSize(0, 40))
        self.buttonsGroupBox.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout = QHBoxLayout(self.buttonsGroupBox)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.camera_section_label = QLabel(self.buttonsGroupBox)
        self.camera_section_label.setObjectName(u"camera_section_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.camera_section_label.sizePolicy().hasHeightForWidth())
        self.camera_section_label.setSizePolicy(sizePolicy1)
        self.camera_section_label.setMinimumSize(QSize(30, 30))
        self.camera_section_label.setMaximumSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.camera_section_label)

        self.start_button = QPushButton(self.buttonsGroupBox)
        self.start_button.setObjectName(u"start_button")
        sizePolicy1.setHeightForWidth(self.start_button.sizePolicy().hasHeightForWidth())
        self.start_button.setSizePolicy(sizePolicy1)
        self.start_button.setMaximumSize(QSize(30, 30))
        self.start_button.setIconSize(QSize(25, 25))
        self.start_button.setCheckable(True)
        self.start_button.setChecked(False)

        self.horizontalLayout.addWidget(self.start_button)

        self.pause_button = QPushButton(self.buttonsGroupBox)
        self.pause_button.setObjectName(u"pause_button")
        sizePolicy1.setHeightForWidth(self.pause_button.sizePolicy().hasHeightForWidth())
        self.pause_button.setSizePolicy(sizePolicy1)
        self.pause_button.setMaximumSize(QSize(30, 30))
        self.pause_button.setIconSize(QSize(25, 25))
        self.pause_button.setCheckable(True)
        self.pause_button.setChecked(False)

        self.horizontalLayout.addWidget(self.pause_button)

        self.stop_button = QPushButton(self.buttonsGroupBox)
        self.stop_button.setObjectName(u"stop_button")
        sizePolicy1.setHeightForWidth(self.stop_button.sizePolicy().hasHeightForWidth())
        self.stop_button.setSizePolicy(sizePolicy1)
        self.stop_button.setMaximumSize(QSize(30, 30))
        self.stop_button.setStyleSheet(u"")
        self.stop_button.setIconSize(QSize(24, 24))
        self.stop_button.setCheckable(False)

        self.horizontalLayout.addWidget(self.stop_button)

        self.show_display_button = QPushButton(self.buttonsGroupBox)
        self.show_display_button.setObjectName(u"show_display_button")
        sizePolicy1.setHeightForWidth(self.show_display_button.sizePolicy().hasHeightForWidth())
        self.show_display_button.setSizePolicy(sizePolicy1)
        self.show_display_button.setMaximumSize(QSize(30, 30))
        self.show_display_button.setStyleSheet(u"")
        self.show_display_button.setIconSize(QSize(24, 24))
        self.show_display_button.setCheckable(False)
        self.show_display_button.setChecked(False)

        self.horizontalLayout.addWidget(self.show_display_button)

        self.show_settings_button = QPushButton(self.buttonsGroupBox)
        self.show_settings_button.setObjectName(u"show_settings_button")
        sizePolicy1.setHeightForWidth(self.show_settings_button.sizePolicy().hasHeightForWidth())
        self.show_settings_button.setSizePolicy(sizePolicy1)
        self.show_settings_button.setMaximumSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.show_settings_button)

        self.save_image_button = QPushButton(self.buttonsGroupBox)
        self.save_image_button.setObjectName(u"save_image_button")
        sizePolicy1.setHeightForWidth(self.save_image_button.sizePolicy().hasHeightForWidth())
        self.save_image_button.setSizePolicy(sizePolicy1)
        self.save_image_button.setMaximumSize(QSize(30, 30))
        self.save_image_button.setStyleSheet(u"")
        self.save_image_button.setIconSize(QSize(24, 24))
        self.save_image_button.setCheckable(False)

        self.horizontalLayout.addWidget(self.save_image_button)

        self.line = QFrame(self.buttonsGroupBox)
        self.line.setObjectName(u"line")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy2)
        self.line.setMinimumSize(QSize(10, 0))
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line)

        self.image_processing_section_label = QLabel(self.buttonsGroupBox)
        self.image_processing_section_label.setObjectName(u"image_processing_section_label")
        sizePolicy1.setHeightForWidth(self.image_processing_section_label.sizePolicy().hasHeightForWidth())
        self.image_processing_section_label.setSizePolicy(sizePolicy1)
        self.image_processing_section_label.setMinimumSize(QSize(30, 30))
        self.image_processing_section_label.setMaximumSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.image_processing_section_label)

        self.show_beam_finder = QPushButton(self.buttonsGroupBox)
        self.show_beam_finder.setObjectName(u"show_beam_finder")
        sizePolicy1.setHeightForWidth(self.show_beam_finder.sizePolicy().hasHeightForWidth())
        self.show_beam_finder.setSizePolicy(sizePolicy1)
        self.show_beam_finder.setMaximumSize(QSize(30, 30))
        self.show_beam_finder.setIconSize(QSize(25, 25))
        self.show_beam_finder.setCheckable(True)
        self.show_beam_finder.setChecked(False)

        self.horizontalLayout.addWidget(self.show_beam_finder)

        self.show_beam_profiler = QPushButton(self.buttonsGroupBox)
        self.show_beam_profiler.setObjectName(u"show_beam_profiler")
        sizePolicy1.setHeightForWidth(self.show_beam_profiler.sizePolicy().hasHeightForWidth())
        self.show_beam_profiler.setSizePolicy(sizePolicy1)
        self.show_beam_profiler.setMaximumSize(QSize(30, 30))
        self.show_beam_profiler.setIconSize(QSize(25, 25))
        self.show_beam_profiler.setCheckable(True)
        self.show_beam_profiler.setChecked(False)

        self.horizontalLayout.addWidget(self.show_beam_profiler)

        self.save_processed_image_button = QPushButton(self.buttonsGroupBox)
        self.save_processed_image_button.setObjectName(u"save_processed_image_button")
        sizePolicy1.setHeightForWidth(self.save_processed_image_button.sizePolicy().hasHeightForWidth())
        self.save_processed_image_button.setSizePolicy(sizePolicy1)
        self.save_processed_image_button.setMinimumSize(QSize(0, 0))
        self.save_processed_image_button.setMaximumSize(QSize(30, 30))

        self.horizontalLayout.addWidget(self.save_processed_image_button)

        self.line_2 = QFrame(self.buttonsGroupBox)
        self.line_2.setObjectName(u"line_2")
        sizePolicy2.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy2)
        self.line_2.setMinimumSize(QSize(10, 0))
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_2)

        self.horizontalSpacer = QSpacerItem(185, 18, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.buttonsGroupBox)

        self.mdiArea = QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName(u"mdiArea")

        self.verticalLayout.addWidget(self.mdiArea)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 862, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.buttonsGroupBox.setTitle("")
#if QT_CONFIG(tooltip)
        self.camera_section_label.setToolTip(QCoreApplication.translate("MainWindow", u"Camera Control Section", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.camera_section_label.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.camera_section_label.setText("")
#if QT_CONFIG(tooltip)
        self.start_button.setToolTip(QCoreApplication.translate("MainWindow", u"Start", None))
#endif // QT_CONFIG(tooltip)
        self.start_button.setText("")
#if QT_CONFIG(tooltip)
        self.pause_button.setToolTip(QCoreApplication.translate("MainWindow", u"Pause", None))
#endif // QT_CONFIG(tooltip)
        self.pause_button.setText("")
#if QT_CONFIG(tooltip)
        self.stop_button.setToolTip(QCoreApplication.translate("MainWindow", u"Stop", None))
#endif // QT_CONFIG(tooltip)
        self.stop_button.setText("")
#if QT_CONFIG(tooltip)
        self.show_display_button.setToolTip(QCoreApplication.translate("MainWindow", u"Show Display", None))
#endif // QT_CONFIG(tooltip)
        self.show_display_button.setText("")
#if QT_CONFIG(tooltip)
        self.show_settings_button.setToolTip(QCoreApplication.translate("MainWindow", u"Show Property Controller", None))
#endif // QT_CONFIG(tooltip)
        self.show_settings_button.setText("")
#if QT_CONFIG(tooltip)
        self.save_image_button.setToolTip(QCoreApplication.translate("MainWindow", u"Save Image", None))
#endif // QT_CONFIG(tooltip)
        self.save_image_button.setText("")
#if QT_CONFIG(tooltip)
        self.image_processing_section_label.setToolTip(QCoreApplication.translate("MainWindow", u"Camera Control Section", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.image_processing_section_label.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.image_processing_section_label.setText("")
#if QT_CONFIG(tooltip)
        self.show_beam_finder.setToolTip(QCoreApplication.translate("MainWindow", u"Beam Finder", None))
#endif // QT_CONFIG(tooltip)
        self.show_beam_finder.setText("")
#if QT_CONFIG(tooltip)
        self.show_beam_profiler.setToolTip(QCoreApplication.translate("MainWindow", u"Beam Profiler", None))
#endif // QT_CONFIG(tooltip)
        self.show_beam_profiler.setText("")
#if QT_CONFIG(tooltip)
        self.save_processed_image_button.setToolTip(QCoreApplication.translate("MainWindow", u"Save Processed Image", None))
#endif // QT_CONFIG(tooltip)
        self.save_processed_image_button.setText("")
    # retranslateUi

