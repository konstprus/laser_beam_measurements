# 
# Project: laser_beam_measurements
#
# File: __main__.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#


from laser_beam_measurements.widgets.main.main_window import MainWindow
from laser_beam_measurements.main.main_object import MainObject


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QStyleFactory
    import sys

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))

    main_object = MainObject()
    w = MainWindow(main_object)
    w.setStyle(app.style())
    w.show()

    app.exec()
