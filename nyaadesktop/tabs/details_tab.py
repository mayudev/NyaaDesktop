from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Slot

from nyaadesktop.scraper.nyaa import Details
from nyaadesktop.tabs.tab_signals import TabSignals


class DetailsTab(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.signals = TabSignals()
        
        # DETAILS
        self.details_box = QtWidgets.QGroupBox()
        details_layout = QtWidgets.QGridLayout()

        key_category = QtWidgets.QLabel("<b>Category</b>")
        self.value_category = QtWidgets.QLabel("")
        self.value_category.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextBrowserInteraction)
        
        key_submitter = QtWidgets.QLabel("<b>Submitter</b>")
        self.value_submitter = QtWidgets.QLabel("")
        self.value_submitter.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextBrowserInteraction)

        key_information = QtWidgets.QLabel("<b>Information</b>")
        self.value_information = QtWidgets.QLabel("")
        self.value_information.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.TextBrowserInteraction)
        self.value_information.setOpenExternalLinks(True)

        details_layout.addWidget(key_category, 0, 0)
        details_layout.addWidget(self.value_category, 1, 0)

        details_layout.addWidget(key_submitter, 0, 1)
        details_layout.addWidget(self.value_submitter, 1, 1)

        details_layout.addWidget(key_information, 0, 2)
        details_layout.addWidget(self.value_information, 1, 2)

        self.details_box.setLayout(details_layout)

        # DESCRIPTION
        description_box = QtWidgets.QGroupBox("Description")
        description_layout = QtWidgets.QVBoxLayout()

        self.description = QtWidgets.QPlainTextEdit()
        self.description.setReadOnly(True)

        description_layout.addWidget(self.description)
        description_box.setLayout(description_layout)

        # Setting up the main layout
        main_layout = QtWidgets.QHBoxLayout()
        sub_layout = QtWidgets.QVBoxLayout()

        sub_layout.addWidget(self.details_box)
        sub_layout.addWidget(description_box)

        main_layout.addLayout(sub_layout)

        self.setLayout(main_layout)

        self.signals.replace.connect(self.replace)
        self.signals.cleanup.connect(self.cleanup)

    @Slot()
    def replace(self, details: Details):
        self.details_box.setTitle(details.title)
        self.value_category.setText(details.category)
        self.value_submitter.setText(details.submitter)
        
        if details.submitter_badge == "text-success":
            self.value_submitter.setStyleSheet("QLabel { color: green; }")
        else:
            self.value_submitter.setStyleSheet("")
        self.value_information.setText(details.information)
        self.description.setPlainText(details.description)

    @Slot()
    def cleanup(self):
        self.details_box.setTitle("Loading...")
        self.value_category.setText("")
        self.value_submitter.setText("")
        self.value_information.setText("")
        self.description.setPlainText("")