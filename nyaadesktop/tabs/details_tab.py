from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Slot

from nyaadesktop.scraper.nyaa import Details
from nyaadesktop.tabs.tab_signals import TabSignals

placeholder = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec porta consectetur lacus, quis pellentesque risus mollis et. Mauris aliquet turpis a nisl laoreet varius. Pellentesque sollicitudin nibh est, et accumsan urna ullamcorper ut. Nam pretium elit est, in laoreet urna mattis et. Suspendisse fringilla erat ex, ac condimentum est rhoncus egestas. Curabitur blandit, neque eget varius aliquet, tellus sem feugiat lectus, id vehicula nibh dui a lorem. Etiam lacinia augue fringilla magna cursus laoreet. Cras vehicula turpis eu sem rhoncus ullamcorper. Aliquam ultricies dolor quis elit condimentum aliquam sit amet sit amet leo. Nam dignissim bibendum bibendum.

Nam in mauris dictum, efficitur risus id, blandit justo. Ut tempus, neque vitae vehicula fringilla, purus mauris elementum arcu, vitae mollis massa risus et nisi. Duis erat erat, vehicula non tristique sit amet, pellentesque id risus. Proin faucibus ac mauris ut cursus. Morbi in leo eleifend, dignissim diam ut, suscipit turpis. Vivamus aliquet efficitur tempus. Curabitur ut eros et eros ornare eleifend id et tortor. Pellentesque rutrum dui tortor, vitae dapibus lorem efficitur non. Donec et ultrices ante. Nulla vel sollicitudin magna. Sed ultrices scelerisque hendrerit. Morbi laoreet et augue non sagittis. Morbi vitae dapibus justo. Duis luctus pellentesque massa, et ultrices turpis malesuada finibus.

Nunc ultricies neque at velit finibus rhoncus sed vitae sem. Pellentesque sollicitudin varius augue non consectetur. Curabitur eu nulla tempus, tincidunt ligula id, tincidunt mi. Aliquam ut sem nunc. Nam quis condimentum neque. Curabitur finibus, dolor id varius mattis, urna ligula dapibus diam, et efficitur purus enim ac nunc. Duis venenatis, purus non varius aliquet, arcu mi placerat leo, eu bibendum est mi quis sem.

Pellentesque turpis nisi, ultricies quis imperdiet quis, cursus eu mi. Curabitur quis interdum leo, et tristique tellus. Pellentesque volutpat ante id ultricies vehicula. Pellentesque aliquet massa pretium consectetur convallis. Suspendisse id dolor nec sapien placerat rutrum et non sem. Etiam vel nisi dui. Proin eget sollicitudin turpis, eu maximus metus.

Ut mattis sapien libero, id sodales justo ullamcorper at. Nunc non est orci. Nulla vel maximus nulla. Aliquam non augue eu leo tempus ornare eget quis nunc. Proin sollicitudin libero vel varius faucibus. Vivamus lobortis aliquam quam, ornare blandit ante consectetur eu. Mauris tristique orci quis tristique vestibulum. Aliquam malesuada ornare mauris. Sed dapibus lacus eros, in dapibus lorem efficitur quis. Etiam enim tortor, commodo eget consectetur at, fringilla a massa. Suspendisse blandit vestibulum arcu, quis lobortis lacus ultrices eget. Sed eu nibh eu felis laoreet vehicula. Suspendisse id sapien tincidunt, finibus magna quis, finibus quam. Nullam rutrum diam sed nibh fringilla, in tempor est pretium. Donec in venenatis orci, quis rutrum velit. 
"""

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
        self.description.setPlainText(placeholder)

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