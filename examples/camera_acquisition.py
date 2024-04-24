#
# Project: laser_beam_measurements
#
# File: camera_acquisition.py
#
# Author: Konstantin Prusakov
#
# Copyright 2024 Konstantin Prusakov <konstantin.prusakov@phystech.edu>
#

from laser_beam_measurements.widgets.camera_control.camera_capture_widget import CameraCaptureWidget
from laser_beam_measurements.camera_control.camera_grabber import CameraGrabber
from laser_beam_measurements.camera_control.camera_factory import CameraFactory

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    grabber = CameraGrabber()
    factory = CameraFactory()
    camera = factory.create_camera("opencv_camera", 0)
    camera.open()
    del factory
    grabber.set_camera(camera)

    w = CameraCaptureWidget()
    w.set_grabber(grabber)
    w.show()
    app.exec()
