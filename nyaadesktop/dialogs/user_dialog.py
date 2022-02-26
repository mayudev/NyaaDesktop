from __future__ import annotations
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QButtonGroup,
    QVBoxLayout,
    QRadioButton,
    QLineEdit,
)


class UserDialog(QDialog):
    def __init__(self, parent=None, current=None):
        super().__init__(parent)

        self.setWindowTitle("Specify user")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Close
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()

        group = QButtonGroup()

        self.radio_global = QRadioButton("Search globally")
        self.radio_user = QRadioButton("Search within user's torrents:")
        self.edit_user = QLineEdit()
        self.edit_user.setPlaceholderText("Specify username...")

        if current is None:
            self.radio_global.setChecked(True)
        else:
            self.radio_user.setChecked(True)
            self.edit_user.setText(current)

        group.addButton(self.radio_global)
        group.addButton(self.radio_user)

        self.layout.addWidget(self.radio_global)
        self.layout.addWidget(self.radio_user)
        self.layout.addWidget(self.edit_user)
        self.layout.addWidget(self.buttonBox)

        self.update()
        self.setLayout(self.layout)

        self.radio_global.clicked.connect(self.update)
        self.radio_user.clicked.connect(self.update)

    def update(self):
        if self.radio_global.isChecked():
            self.edit_user.setEnabled(False)
        elif self.radio_user.isChecked():
            self.edit_user.setEnabled(True)
            self.edit_user.setFocus()

    def get_value(self):
        if super().exec():
            return self.radio_global.isChecked(), self.edit_user.text()
        else:
            return False
