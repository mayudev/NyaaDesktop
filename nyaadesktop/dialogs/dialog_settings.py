from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)
from PySide6.QtGui import QIcon


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setWindowIcon(QIcon(":/icons/preferences"))

        self.init_widgets()

    def init_widgets(self):
        layout = QVBoxLayout()

        general = QGroupBox()
        general.setTitle("General")

        general_contents = QVBoxLayout()

        setting_url = QHBoxLayout()
        setting_url.addWidget(QLabel("Nyaa URL"))

        self.url = QLineEdit()
        self.url.setText("https://nyaa.si")  # TODO get value from settings

        url_reset = QPushButton("Reset")
        url_reset.clicked.connect(self.reset_url)

        setting_url.addWidget(self.url, 1)
        setting_url.addWidget(url_reset)

        general_contents.addLayout(setting_url)

        general.setLayout(general_contents)

        layout.addWidget(general)
        self.setLayout(layout)

    def reset_url(self):
        self.url.setText("https://nyaa.si")
