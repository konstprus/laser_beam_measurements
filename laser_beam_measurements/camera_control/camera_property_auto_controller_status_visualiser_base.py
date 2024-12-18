from .camera_property_auto_controller import ControllerStatus
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Slot


class ControllerStatusVisualiserBase(QLabel):

    def __init__(self, parent=None):
        super(ControllerStatusVisualiserBase, self).__init__(parent)
        self._status_styles: dict[ControllerStatus, str] = {
            # ControllerStatus.STATUS_NONE: "",
            # ControllerStatus.STATUS_OK: "",
            # ControllerStatus.STATUS_NOT_OK: "",
            # ControllerStatus.STATUS_HIGH : "",
            # ControllerStatus.STATUS_LOW : "",
            # ControllerStatus.STATUS_RUNNING : "",
            # ControllerStatus.STATUS_BAD_LOW : "",
            # ControllerStatus.STATUS_BAD_HIGH : "",
        }
        self._status_text: dict[ControllerStatus, str] = {
            # ControllerStatus.STATUS_NONE: "",
            # ControllerStatus.STATUS_OK: "",
            # ControllerStatus.STATUS_NOT_OK: "",
            # ControllerStatus.STATUS_HIGH : "",
            # ControllerStatus.STATUS_LOW : "",
            # ControllerStatus.STATUS_RUNNING : "",
            # ControllerStatus.STATUS_BAD_LOW : "",
            # ControllerStatus.STATUS_BAD_HIGH : "",
        }
        self._init_styles_dict()

    @Slot(ControllerStatus)
    def show_status(self, status: ControllerStatus) -> None:
        print(status)
        if status in self._status_styles.keys() and status in self._status_text.keys():
            status_style = self._status_styles.get(status)
            status_text = self._status_text.get(status)
            # self.setStyleSheet(status_style)
            # self.setText(status_text)
            self._set_style_and_text(status_style, status_text)
        else:
            self.set_default_status()

    def _set_style_and_text(self, style: str, text: str) -> None:
        self.setStyleSheet(style)
        self.setText(text)

    def set_default_status(self):
        raise NotImplementedError()

    def _init_styles_dict(self):
        raise NotImplementedError()