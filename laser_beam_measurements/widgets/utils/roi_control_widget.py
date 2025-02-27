from PySide6.QtWidgets import QWidget

from ..utils.ui_roi_control_widget import Ui_Form

class ROIControl(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

    def set_label_text(self, text: str) -> None:
        self.ui.label.setText(text)

    @property
    def doubleSpinBox(self) -> None:
        return self.ui.doubleSpinBox