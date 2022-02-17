from __future__ import annotations
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize, Slot
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon

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
        """
        Replace current model with new data
        """
        newData = details.files[0]

        # Create a new model with two columns
        model = QStandardItemModel(0, 2)
        model.setHorizontalHeaderLabels(["Name", "Size"])

        root = model.invisibleRootItem()

        # A method to parse children of a folder
        def parseChildren(children):
            items = []

            for child in children:
                # Child is a folder
                if len(child.children) > 0:
                    # Parent element
                    item = FilesTabItem(QIcon(":/icons/files"), child.name)

                    # Add a tooltip
                    item.setToolTip(child.name)

                    # Ah yes, children of a child.
                    child_children = parseChildren(child.children)
                    for row in child_children:
                        item.appendRow(row)

                # Child is a file (thank you)
                else:
                    itemColumn1 = FilesTabItem(QIcon(":/icons/file"), child.name)
                    itemColumn2 = FilesTabItem(child.size)

                    # Add a tooltip
                    itemColumn1.setToolTip(child.name)

                    item = [itemColumn1, itemColumn2]

                items.append(item)

            return items

        # Parent element name
        parentItemColumn1 = FilesTabItem(newData.name)
        parentItemColumn1.setToolTip(newData.name)

        # Parent is a folder
        if len(newData.children) > 0:
            parentItemColumn1.setIcon(QIcon(":/icons/files"))
            for row in parseChildren(newData.children):
                parentItemColumn1.appendRow(row)
            root.appendRow(parentItemColumn1)

        # Parent is a file
        else:
            parentItemColumn1.setIcon(QIcon(":/icons/file"))

            # Column 2 (size) is used only when parent is a file
            parentItemColumn2 = FilesTabItem(newData.size)
            parentItem = [parentItemColumn1, parentItemColumn2]

            root.appendRow(parentItem)

        self.tree_view.setModel(model)

        # Expand all by default
        self.tree_view.expandRecursively(parentItemColumn1.index())

        # Set considerable 'Name' column width
        # This is the only way I could get this to work.
        self.tree_view.setColumnWidth(0, self.window().width()-140)

    @Slot()
    def cleanup(self):
        # Clear tree view
        self.tree_view.setModel(QStandardItemModel())