from asyncio import CancelledError
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QSpinBox,
    QVBoxLayout,
    QLabel
)


class PageDialog(QDialog):
    
    def __init__(self, parent=None, min_value=1, max_value=1, current=1):
        super().__init__(parent)

        self.setWindowTitle("Set current page")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Close
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        message = QLabel("Enter page:")
        self.spin = QSpinBox()
        self.spin.setRange(min_value, max_value)
        self.spin.setValue(current)

        self.layout.addWidget(message)
        self.layout.addWidget(self.spin)
        self.layout.addWidget(self.buttonBox)

        self.setLayout(self.layout)

    def get_value(self) -> int:
        if super().exec():
            return self.spin.value()
        else:
            return False