from __future__ import annotations
from PySide6.QtCore import Qt, QAbstractTableModel, QModelIndex, QSize
from PySide6.QtGui import QColor, QIcon

from nyaadesktop.item import Item
import re

# Colors ~~stolen~~ from nyaa
NYAA_LIGHT_REMAKE = "#f2dede"
NYAA_LIGHT_TRUSTED = "#dff0d8"
NYAA_LIGHT_LINK = "#000000"
NYAA_LIGHT_ANIME_ENGLISH = "#650093"
NYAA_LIGHT_ANIME_NONENGLISH = "#247d00"
NYAA_LIGHT_ANIME_RAW = "#555c68"

NYAA_DARK_TRUSTED = "#36482f"
NYAA_DARK_REMAKE = "#462c2c"
NYAA_DARK_LINK = "#6badf4"
NYAA_DARK_ANIME_ENGLISH = "#bc61e2"
NYAA_DARK_ANIME_NONENGLISH = "#3fd500"
NYAA_DARK_ANIME_RAW = "#b7c2ca"


class ResultsModel(QAbstractTableModel):
    def __init__(self, data: list[Item] = None, is_dark_theme=False):
        super().__init__()
        self.items: list[Item] = data or []
        self.columns = (
            "Category",
            "Name",
            "Size",
            "Date",
            "Seeds",
            "Leechers",
            "Complete",
            "Comments",
        )
        self.is_dark_theme = is_dark_theme

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

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        column = index.column()
        row = index.row()

        if role == Qt.DisplayRole:

            item = self.items[row]
            if column == 0:
                return simplify_category(item.category)
            if column == 1:
                return item.name
            if column == 2:
                return item.size
            if column == 3:
                return item.date
            if column == 4:
                return item.seeders
            if column == 5:
                return item.leechers
            if column == 6:
                return item.completed
            if column == 7:
                return item.comment_count
            else:
                return ""

        elif role == Qt.ToolTipRole:

            item = self.items[row]
            if column == 0:
                return item.category
            if column == 1:
                return item.name
            if column == 2:
                return item.size
            if column == 3:
                return item.date
            if column == 4:
                return item.seeders
            if column == 5:
                return item.leechers
            if column == 6:
                return item.completed
            if column == 7:
                return item.comment_count
            else:
                return ""

        elif role == Qt.SizeHintRole:

            return QSize(1, 28)

        elif role == Qt.DecorationRole:

            item = self.items[row]

            # Category column
            if column == 0:
                if item.category.endswith("Non-English-translated"):
                    return QIcon(":/icons/es")
                elif item.category.endswith("English-translated"):
                    return QIcon(":/icons/en")
                elif item.category.endswith("Raw"):
                    return QIcon(":/icons/jp")
                else:
                    return None

            # Name column
            # I have no idea why, but this was causing performance issues.
            elif column == 1:
                return None
                if item.badge == "trusted":
                    return QIcon(":/icons/ok")
                elif item.badge == "remake":
                    return QIcon(":/icons/danger")
                else:
                    return None

        elif role == Qt.BackgroundRole:

            if column != 0:
                item = self.items[row]
                if item.badge == "trusted":
                    if self.is_dark_theme:
                        return QColor(NYAA_DARK_TRUSTED)
                    else:
                        return QColor(NYAA_LIGHT_TRUSTED)
                elif item.badge == "remake":
                    if self.is_dark_theme:
                        return QColor(NYAA_DARK_REMAKE)
                    else:
                        return QColor(NYAA_LIGHT_REMAKE)
                else:
                    return None

        elif role == Qt.ForegroundRole:

            if column == 0:
                item = self.items[row]

                if item.category.startswith("Anime"):
                    if item.category.endswith("Non-English-translated"):
                        if self.is_dark_theme:
                            return QColor(NYAA_DARK_ANIME_NONENGLISH)
                        else:
                            return QColor(NYAA_LIGHT_ANIME_NONENGLISH)
                    elif item.category.endswith("English-translated"):
                        if self.is_dark_theme:
                            return QColor(NYAA_DARK_ANIME_ENGLISH)
                        else:
                            return QColor(NYAA_LIGHT_ANIME_ENGLISH)
                    elif item.category.endswith("Raw"):
                        if self.is_dark_theme:
                            return QColor(NYAA_DARK_ANIME_RAW)
                        else:
                            return QColor(NYAA_LIGHT_ANIME_RAW)
                    else:
                        return None
            elif column == 1:
                if self.is_dark_theme:
                    # Damn this replicates nyaa feeling really well
                    return QColor(NYAA_DARK_LINK)
                else:
                    # Light theme suffers though...
                    return QColor(NYAA_LIGHT_LINK)

            elif column == 4:  # Seeders
                if self.is_dark_theme:
                    return QColor(Qt.green)
                else:
                    return QColor(Qt.darkGreen)
            elif column == 5:  # Leechers
                return QColor(Qt.red)

        return None


def simplify_category(category: str) -> str:
    if category.endswith("Non-English-translated"):
        return re.sub(" - Non-English-translated", "", category)
    elif category.endswith("English-translated"):
        return re.sub(" - English-translated", "", category)
    elif category.endswith("Raw"):
        return re.sub(" - Raw", "", category)
    else:
        return category
