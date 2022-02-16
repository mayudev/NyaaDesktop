from __future__ import annotations
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QSize, Slot
from PySide6.QtGui import QStandardItemModel, QStandardItem

from nyaadesktop.scraper.nyaa import Details, File
from nyaadesktop.tabs.tab_signals import TabSignals

class FilesTab(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.signals = TabSignals()
        #self.model = FilesModel(data=[("Ep01.mkv", "319.21 MiB"),("Ep02.mkv", "320.29 MiB")])

        self.table_view = QtWidgets.QTreeView(self)
        #self.table_view.setModel(self.model)

        #self.table_view.setRootIsDecorated(False)
        #self.table_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        #self.table_view.setUniformRowHeights(True)
        
        self.table_view.setColumnWidth(1, 100)

        #header = self.table_view.header()
        #header.setStretchLastSection(False)
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        #self.table_view.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.table_view)

        self.setLayout(self.main_layout)

        self.signals.replace.connect(self.replace)
        self.signals.cleanup.connect(self.cleanup)

    @Slot()
    def replace(self, details: Details):
        newData = details.files[0]

        model = QStandardItemModel()
        root = model.invisibleRootItem()

        def parseChildren(children):
            items = []

            for child in children:
                item = QStandardItem(child.name)
                if len(child.children) > 0:
                    child_children = parseChildren(child.children)
                    item.appendRows(child_children)

                items.append(item)

            return items

        root.appendRows(parseChildren(newData.children))
        self.table_view.setModel(model)

    @Slot()
    def cleanup(self):
        self.table_view.setModel(FilesModel())