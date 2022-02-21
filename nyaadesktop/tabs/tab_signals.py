from PySide6.QtCore import QObject, Signal

class TabSignals(QObject):
    replace = Signal(object)
    cleanup = Signal()
    search_request = Signal(str)