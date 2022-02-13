from nyaadesktop.item import Item

from PySide6.QtCore import QRunnable, Slot, QObject, Signal

import traceback, sys

class WorkerSignals(QObject):
    result = Signal(tuple)
    error = Signal(object)

class ScraperWorker(QRunnable):
    '''
    Worker thread for scrapers
    '''

    def __init__(self, fn, *args, **kwargs):
        super(ScraperWorker, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @Slot()
    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)