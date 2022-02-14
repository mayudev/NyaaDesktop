from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QSize, Slot
from nyaadesktop.scraper.nyaa import Details, File
from nyaadesktop.tabs.tab_signals import TabSignals

class FilesModel(QAbstractTableModel):

    def __init__(self, data: list[File]=None):
        super().__init__()
        self.items = data or []
        self.columns = ("Name", "Size")

    def rowCount(self, index):
        return len(self.items)

    def columnCount(self, index):
        return len(self.columns)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role != Qt.DisplayRole:
            return None
        if orientation == Qt.Horizontal:
            return self.columns[section]
        else:
            return "{}".format(section)

    def data(self, index: QModelIndex, role = Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            item = self.items[row]
            if column == 0:
                return item.name
            elif column == 1:
                return item.size
        elif role == Qt.SizeHintRole:
            return QSize(1, 25)

        return None

class FilesTab(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.signals = TabSignals()
        self.model = FilesModel(data=[("Ep01.mkv", "319.21 MiB"),("Ep02.mkv", "320.29 MiB")])

        self.table_view = QtWidgets.QTreeView()
        self.table_view.setModel(self.model)

        self.table_view.setRootIsDecorated(False)
        self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.table_view.setUniformRowHeights(True)
        
        self.table_view.setColumnWidth(1, 100)

        header = self.table_view.header()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        #self.table_view.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.table_view)

        self.setLayout(self.main_layout)

        self.signals.replace.connect(self.replace)
        self.signals.cleanup.connect(self.cleanup)

    @Slot()
    def replace(self, details: Details):
        newModel = FilesModel(data=details.files)
        #newModel = mesg
        self.table_view.setModel(newModel)

    @Slot()
    def cleanup(self):
        self.table_view.setModel(FilesModel())