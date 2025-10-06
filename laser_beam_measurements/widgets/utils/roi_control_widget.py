from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QDoubleSpinBox


class ROIControl(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._layout = QHBoxLayout(self)
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self._label = QLabel(self)
        self._layout.addWidget(self._label)

        self._double_spin_box = QDoubleSpinBox(self)
        self._double_spin_box.setRange(-5000.0, 5000.0)
        self._layout.addWidget(self._double_spin_box)

    def set_label_text(self, text: str) -> None:
        self._label.setText(text)

    @property
    def double_spin_box(self) -> QDoubleSpinBox:
        return self._double_spin_box
