from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QLabel
)

description = """
<p>A desktop application for easily accessing nyaa.si</p>

<p>Icons: <b>Zafiro-icons</b> <a href='https://github.com/zayronxio/Zafiro-icons'>https://github.com/zayronxio/Zafiro-icons</a></p>

repo
"""

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("About NyaaDesktop")

        layout = QVBoxLayout()

        title = QLabel("NyaaDesktop")

        contents = QLabel()
        contents.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextBrowserInteraction)
        contents.setOpenExternalLinks(True)
        contents.setText(description)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout.addWidget(title)
        layout.addWidget(contents)
        layout.addWidget(buttonBox)
        self.setLayout(layout)