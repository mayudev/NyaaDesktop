from __future__ import annotations
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtGui import QStandardItemModel, QStandardItem

from nyaadesktop.scraper.nyaa import Details
from nyaadesktop.tabs.tab_signals import TabSignals

class FilesTabItem(QStandardItem):
    def __init__(self, *args):
        super().__init__(*args)
        self.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.setSizeHint(QSize(1, 25))

class FilesTab(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.signals = TabSignals()

        self.tree_view = QtWidgets.QTreeView(self)

        self.tree_view.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree_view.setUniformRowHeights(True)
        
        self.tree_view.setColumnWidth(1, 100)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.tree_view)

        self.setLayout(self.main_layout)

        self.signals.replace.connect(self.replace)
        self.signals.cleanup.connect(self.cleanup)

    @Slot()
    def replace(self, details: Details):
        newData = details.files[0]

        model = QStandardItemModel(0, 2)
        model.setHorizontalHeaderLabels(["Name", "Size"])
        root = model.invisibleRootItem()

        def parseChildren(children):
            items = []

            for child in children:
                
                if len(child.children) > 0:
                    item = FilesTabItem(child.name)
                    child_children = parseChildren(child.children)
                    for row in child_children:
                        item.appendRow(row)
                else:
                    itemColumn1 = FilesTabItem(child.name)
                    itemColumn2 = FilesTabItem(child.size)
                    item = [itemColumn1, itemColumn2]

                items.append(item)

            return items

        parentItemColumn1 = FilesTabItem(newData.name)

        if len(newData.children) > 0:
            for row in parseChildren(newData.children):
                parentItemColumn1.appendRow(row)
            root.appendRow(parentItemColumn1)
        else:
            parentItemColumn2 = FilesTabItem(newData.size)
            parentItem = [parentItemColumn1, parentItemColumn2]
            root.appendRow(parentItem)

        self.tree_view.setModel(model)
        self.tree_view.expandRecursively(parentItemColumn1.index())

        # This is the only way I could get this to work.
        self.tree_view.setColumnWidth(0, self.window().width()-140)

    @Slot()
    def cleanup(self):
        self.tree_view.setModel(QStandardItemModel())