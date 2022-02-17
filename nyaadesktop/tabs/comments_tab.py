from PySide6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTextBrowser
from PySide6.QtCore import Qt, Slot

from nyaadesktop.scraper.nyaa import Details
from nyaadesktop.tabs.tab_signals import TabSignals

class CommentsTab(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = TabSignals()

        self.main_layout = QVBoxLayout()

        group = QGroupBox("Comments")
        group_layout = QVBoxLayout()
        
        self.contents = QTextBrowser()
        self.contents.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextBrowserInteraction)
        self.contents.setReadOnly(True)

        group_layout.addWidget(self.contents, 1)
        group.setLayout(group_layout)

        self.main_layout.addWidget(group)
        self.setLayout(self.main_layout)

        self.signals.replace.connect(self.replace)
        self.signals.cleanup.connect(self.cleanup)

    @Slot()
    def replace(self, details: Details):
        comments = details.comments

        if len(comments):
            comments_string = ""
            for comment in comments:
                comments_string += "<p><b>{}</b> ({})<br />{}</p>".format(comment.author, comment.date, comment.comment)

            self.contents.setText(comments_string)
    @Slot()
    def cleanup(self):
        self.contents.setText("")