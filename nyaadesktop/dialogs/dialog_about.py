from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QLabel,
)

from nyaadesktop.__init__ import __version__
from platform import python_version
from importlib.metadata import version

description = """
<p>A desktop application for nyaa.si</p>

<p>Icons:<br />
<a style='color: #2980b9;' href='https://github.com/zayronxio/Zafiro-icons'>Zafiro-icons</a><br />
<a style='color: #2980b9;' href='https://icons8.com'>Flag icons by Icons8</a>
</p>

<p>
Repository:<br />
<a style='color: #2980b9;' href='https://github.com/mayudev/NyaaDesktop'>https://github.com/mayudev/NyaaDesktop</a>
</p>

<p>
<b>Python</b><br />
Version {}
</p>

<p>
<b>Qt</b><br />
Version {}
</p>
""".format(
    python_version(), version("PySide6")
)


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("About NyaaDesktop")

        layout = QVBoxLayout()
        header = QHBoxLayout()
        subheader = QVBoxLayout()

        title = QLabel("NyaaDesktop")
        title_font = title.font()
        title_font.setPointSize(title_font.pointSize() + 3)
        title.setFont(title_font)

        version = QLabel("Version {}".format(__version__))

        subheader.addWidget(title)
        subheader.addWidget(version)

        header.addLayout(subheader)

        group = QGroupBox()
        contents_layout = QVBoxLayout()

        contents = QLabel()
        contents.setTextInteractionFlags(
            Qt.TextSelectableByMouse | Qt.TextBrowserInteraction
        )
        contents.setOpenExternalLinks(True)
        contents.setText(description)

        contents_layout.addWidget(contents)
        group.setLayout(contents_layout)

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        layout.addLayout(header)
        layout.addWidget(group)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
