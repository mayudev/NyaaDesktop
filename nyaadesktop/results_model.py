from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QSize, Slot
from PySide6.QtGui import QColor, QIcon, QFont

from nyaadesktop.item import Item
import re

class ResultsModel(QAbstractTableModel):
    
    def __init__(self, data: list[Item]=None):
        super().__init__()
        self.items: list[Item] = data or []
        self.columns = ("Category", "Name", "Size", "Date", "Seeds", "Leechers", "Complete", "Comments")

    def rowCount(self, index):
        return len(self.items)

    def columnCount(self, index):
        return len(self.columns)

    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.columns[section]
        elif role == Qt.ToolTipRole:
            if section == 4:
                return "Seeders"
            elif section == 5:
                return "Leechers"
            elif section == 6:
                return "Completed downloads"
            elif section == 7:
                return "Comment count"
            return self.columns[section]
        else:
            return None

    def data(self, index: QModelIndex, role = Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:
            item = self.items[row]
            match column:
                case 0:
                    return simplify_category(item.category)
                case 1:
                    return item.name
                case 2:
                    return item.size
                case 3:
                    return item.date
                case 4:
                    return item.seeders
                case 5:
                    return item.leechers
                case 6:
                    return item.completed
                case 7:
                    return item.comment_count
                case _:
                    return ""
        elif role == Qt.ToolTipRole:
            item = self.items[row]
            match column:
                case 0:
                    return item.category
                case 1:
                    return item.name
                case 2:
                    return item.size
                case 3:
                    return item.date
                case 4:
                    return item.seeders
                case 5:
                    return item.leechers
                case 6:
                    return item.completed
                case 7:
                    return item.comment_count
                case _:
                    return ""
        elif role == Qt.StatusTipRole:
            return self.items[row].name
        elif role == Qt.BackgroundRole:
            item = self.items[row]
            if column == 0:
                if item.category.startswith("Anime"):
                    if item.category.endswith("Non-English-translated"):
                        return QColor("#4e7c3a")
                    elif item.category.endswith("English-translated"):
                        return QColor("#683f7a")
                    elif item.category.endswith("Raw"):
                        return QColor("#66727a")
                    else:
                        return None
        elif role == Qt.FontRole:
            if column == 0:
                font = QFont()
                font.setBold(True)
                return font
        elif role == Qt.SizeHintRole:
            return QSize(1, 28)
        elif role == Qt.DecorationRole:
            item = self.items[row]
            if column == 0:
                if item.category.endswith("Non-English-translated"):
                    return QIcon(":/icons/es")
                elif item.category.endswith("English-translated"):
                    return QIcon(":/icons/en")
                elif item.category.endswith("Raw"):
                    return QIcon(":/icons/jp")
                else:
                    return None
        elif role == Qt.ForegroundRole:
            if column == 0:
                item = self.items[row]

                if item.category.startswith("Anime") and (item.category.endswith("translated") or item.category.endswith("Raw")):
                    return QColor(Qt.white)
            if column == 4: # Seeders
                return QColor(Qt.green)
            elif column == 5: # Leechers
                return QColor(Qt.red)

        return None
            
def simplify_category(category: str) -> str:
    if category.endswith("Non-English-translated"):
        return re.sub(" - Non-English-translated", '', category)
    elif category.endswith("English-translated"):
        return re.sub( " - English-translated", '', category)
    elif category.endswith("Raw"):
        return re.sub( " - Raw", '', category)
    else:
        return category