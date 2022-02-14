from nyaadesktop.open import open_links, save_torrents
from nyaadesktop.MainWindow import Ui_MainWindow
from nyaadesktop.item import Item
from nyaadesktop.results_model import ResultsModel

from nyaadesktop.dialogs.dialog_about import AboutDialog
from nyaadesktop.dialogs.page_dialog import PageDialog
from nyaadesktop.dialogs.confirmation_dialog import ConfirmationDialog

from nyaadesktop.tabs.comments_tab import CommentsTab
from nyaadesktop.tabs.details_tab import DetailsTab
from nyaadesktop.tabs.files_tab import FilesModel, FilesTab

from nyaadesktop.scraper.details_scraper import details_scraper
from nyaadesktop.scraper.results_scraper import result_scraper
from nyaadesktop.scraper.worker import ScraperWorker
from nyaadesktop.scraper.nyaa import BASE_URL, Details, ScraperNoResults, categories, details_url_builder, url_builder

from PySide6 import QtWidgets
from PySide6.QtCore import QModelIndex, QThreadPool
from PySide6.QtGui import QKeySequence, QCursor

import sys

if __name__ == "__main__":
    DEFAULT_TIMEOUT = 5000

    class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
        def __init__(self):
            super().__init__()
            self.setupUi(self)

            self.threadpool = QThreadPool()
            self.worker = None

            self.filters = ("No filter", "No remakes", "Trusted only")
            self.columns = ("size", "id", "seeders", "leechers", "downloads", "comments")
            self.current_page = 1
            self.page_count = 10

            self.stack = QtWidgets.QStackedLayout()

            # Dark theme detection
            palette = self.palette()
            self.dark_theme = palette.windowText().color().value() > palette.window().color().value()

            # tabs
            self.details_tab = DetailsTab(self)
            self.files_tab = FilesTab(self)

            self.connect_actions()
            self.init_statusbar()
            self.init_combo()
            self.init_search()
            self.init_pages()
            self.init_frame()
            self.init_tabs()
            self.init_results_view()
            
        def connect_actions(self):
            """
            Connect actions to triggers and specify shortcuts (since it wasn't done in Designer)
            """
            # Quit action
            self.actionQuit.triggered.connect(self.close)
            self.actionQuit.setShortcut(QKeySequence.Quit)

            # About action
            self.actionAbout.triggered.connect(self.show_about)

            # List action
            self.actionSave_torrent_file.triggered.connect(self.save_torrent)
            self.actionDownload.triggered.connect(self.open_magnet)
            self.actionOpen_in_browser.triggered.connect(self.open_browser)

        def init_statusbar(self):
            self.statusbar = QtWidgets.QStatusBar()
            self.setStatusBar(self.statusbar)

        def init_combo(self):
            """
            Populate combo boxes with choices
            """
            # Filters
            for filter_name in self.filters:
                self.search_filter.addItem(filter_name)
            
            self.search_filter.setCurrentIndex(0)

            # Categories
            for category in categories:
                self.search_categories.addItem(category.name)

            # TODO set position from last run
            self.search_categories.setCurrentIndex(0)

            # Sort
            for sort_name in self.columns:
                self.search_sort.addItem(sort_name)

            # Default sort is set to seeders, as it's what you usually want
            # unless it's 
            self.search_sort.setCurrentIndex(2)

        def init_search(self):
            """
            Set up the search bar
            """
            self.search_text.returnPressed.connect(self.initiate_search)
            self.search_button.clicked.connect(self.initiate_search)

        def init_pages(self):
            """
            Set up buttons for page navigation
            """
            self.page_prev.clicked.connect(lambda: self.switch_page(-1))
            self.page_next.clicked.connect(lambda: self.switch_page(1))
            self.page_go.clicked.connect(self.show_page_selection)
            self.update_page_count()

        def init_frame(self):
            """
            Set up StackedWidget in the frame
            """

            self.stack.addWidget(self.details_tab)
            self.stack.addWidget(self.files_tab)
            self.stack.addWidget(CommentsTab(self))

            self.frame.setMaximumHeight(300)
            self.frame.setLayout(self.stack)
            self.frame.setVisible(False)

        def init_tabs(self):
            """
            Set up a button group, connect tab buttons to signals
            """

            # TODO do this in a smarter way?
            self.button_group = QtWidgets.QButtonGroup()

            self.button_group.setExclusive(True)

            self.button_group.addButton(self.details_button)
            # self.button_group.addButton(self.description_button)
            self.button_group.addButton(self.files_button)
            self.comments_button.setVisible(False) # Hiding, I'm too lazy to implement this for now
            #self.button_group.addButton(self.comments_button)

            self.details_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
            # self.description_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
            self.files_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
            #self.comments_button.clicked.connect(lambda: self.stack.setCurrentIndex(2))

            self.details_button.setChecked(True)
            
        def init_results_view(self):
            # Set up initial model
            self.items: list[Item] = []


            # placeholder data
            for i in range(0, 100):
                self.items.append(Item("Literature - Raw", "Index {}".format(i), "/torrent", "/view/76", "magnet", "1 MiB", "2022-02-12 13:06", 10, 0, 0, 0))
            self.model = ResultsModel(data=self.items, is_dark_theme=self.dark_theme)
            self.results.setModel(self.model)

            # Resize columns that hold only numbers
            for i in range(4, 8):
                self.results.setColumnWidth(i, 60)

            # Resize Date columns as it's too small by default
            self.results.setColumnWidth(3, 120)

            header = self.results.header()
            header.setStretchLastSection(False)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

            self.results.customContextMenuRequested.connect(self.invoke_menu)
            self.results.selectionModel().selectionChanged.connect(self.selection_changed)

        def switch_page(self, offset):
            if 1 <= self.current_page + offset <= self.page_count:
                self.current_page += offset
                self.search()
            else:
                print("range exceeded")


        def initiate_search(self):
            """
            Reset the page counter to 1 and initiate a new search
            """
            self.current_page = 1
            self.search()

        def search(self):
            """
            Initiate a request to nyaa
            """
            query = self.search_text.text()
            current_sort = self.columns[self.search_sort.currentIndex()]

            current_category = categories[self.search_categories.currentIndex()]
            category_string = "{}_{}".format(current_category.id, current_category.subid)
            
            url = url_builder(
                query, 
                category_id=category_string, 
                filter_id=self.search_filter.currentIndex(),
                page=self.current_page,
                sort=current_sort)
            
            # Execute worker
            if self.worker is None:
                self.lock_buttons()

                self.worker = ScraperWorker(result_scraper, url)
                self.worker.signals.result.connect(self.process_scraper_result)
                self.worker.signals.error.connect(self.process_scraper_error)

                self.threadpool.start(self.worker)

        def process_scraper_result(self, result):
            self.worker = None

            results, pages = result

            self.model.items = results
            self.model.layoutChanged.emit()

            self.results.setModel(self.model)

            self.results.scrollToTop()
            self.results.clearSelection()

            self.page_count = pages
            self.update_page_count()

        def process_scraper_error(self, err):
            self.worker = None

            if err[0] == ScraperNoResults:
                print("No results")
                # TODO show an error dialog
                pass
            else:
                print("Something went wrong")
        
        def details_scraper_result(self, result: Details, item: Item):
            self.worker = None

            result.category = item.category

            self.details_tab.signals.replace.emit(result)
            self.files_tab.signals.replace.emit(result)

            # Show frame (which displays details)
            self.frame.setVisible(True)

        def details_scraper_error(self, err):
            self.worker = None

            print("something went wrong")

        def lock_buttons(self):
            # Show loading message
            self.statusbar.showMessage("Loading...")

            self.search_button.setEnabled(False)
            self.page_prev.setEnabled(False)
            self.page_next.setEnabled(False)
            self.page_go.setEnabled(False)

        def update_page_count(self):
            self.page_display.setText("Page {} / {}".format(self.current_page, self.page_count))

            # 'Next page' button is enabled if current page is not last
            self.page_next.setEnabled(self.current_page != self.page_count)

            # 'Previous page' button is enabled if current page is not first
            self.page_prev.setEnabled(self.current_page != 1) 

            # Additionally, unlock buttons
            self.page_go.setEnabled(True)
            self.search_button.setEnabled(True)
            
            self.statusbar.clearMessage()       
        
        def update_actions(self, count):
            """
            Display the number of selected items next to actions
            """
            base_torrent = "Save .torrent file"
            base_download = "Download selected"

            if count > 1:
                self.actionSave_torrent_file.setText("{} ({})".format(base_torrent, count))
                self.actionDownload.setText("{} ({})".format(base_download, count))
            else:
                self.actionSave_torrent_file.setText(base_torrent)
                self.actionDownload.setText(base_download)

        def invoke_menu(self):
            """
            Shows the 'Edit' menu as context menu
            """
            point = QCursor.pos()
            self.menuEdit.exec(point)

        def selection_changed(self):
            # Update selection count in actions
            selections = self.results.selectedIndexes()

            selected_count = int(len(selections) / len(self.model.columns))
            self.update_actions(selected_count)

            # Hide frame if no elements are selected
            if selected_count == 0:
                self.frame.setVisible(False)
                self.details_tab.signals.cleanup.emit()
                self.files_tab.signals.cleanup.emit()

            # Don't send request if there's more than one selected item,
            # since we don't want to query nyaa too much.
            if len(self.model.columns) == len(selections):
                selection: QModelIndex = selections[0]
                selected_row = selection.row()

                # Query nyaa and display details in tabs
                if self.worker is None:
                    self.details_tab.signals.cleanup.emit()
                    self.files_tab.signals.cleanup.emit()

                    url = details_url_builder(self.model.items[selected_row].details_url)
                    self.worker = ScraperWorker(details_scraper, url)
                    self.worker.signals.result.connect(lambda result: self.details_scraper_result(result, self.model.items[selected_row]))
                    self.worker.signals.error.connect(self.details_scraper_error)

                    self.threadpool.start(self.worker)
        
        def save_torrent(self):
            selections = self.results.selectedIndexes()

            torrent_urls = []

            try:
                for selection in range(0, len(selections), len(self.model.columns)):
                    index = selections[selection].row()
                    torrent_url = self.model.items[index].torrent_url

                    if torrent_url is None:
                        raise
                    else:
                        torrent_urls.append(torrent_url)
            except:
                # TODO show error
                print("No torrent file")
            else:
                save_torrents(torrent_urls)
                self.statusbar.showMessage("Saved {} .torrent files in current directory.".format(len(torrent_urls)), DEFAULT_TIMEOUT)

        def open_magnet(self):
            selections = self.results.selectedIndexes()

            magnet_list = []
            # selectedIndexes contains an element for every column, so every row has 8 elements

            try:
                for selection in range(0, len(selections), len(self.model.columns)):
                    index = selections[selection].row()
                    magnet = self.model.items[index].magnet

                    if magnet is None:
                        raise
                    else:
                        magnet_list.append(magnet)
            except:
                print("No magnet") # TODO no magnet message
            else:
                # Opening too many links at once can be painful,
                # so we're showing a confirmation dialog here.
                if len(magnet_list) > 5:
                    confirmation = ConfirmationDialog("Confirmation", "Do you want to open {} torrents in your client?".format(len(magnet_list)), self)
                    if confirmation.exec():
                        open_links(magnet_list)
                        self.statusbar.showMessage("Opened {} files in your torrent client.".format(len(magnet_list)), DEFAULT_TIMEOUT)
                else:
                    open_links(magnet_list)
                    self.statusbar.showMessage("Opened {} files in your torrent client.".format(len(magnet_list)), DEFAULT_TIMEOUT)

        def open_browser(self):
            selections = self.results.selectedIndexes()

            # Let's make it open only the first selected element
            index = selections[0].row()
            details_url = self.model.items[index].details_url

            if details_url is None:
                print("No url") # TODO error message
            else:
                open_links([BASE_URL+details_url])

        def show_page_selection(self):
            """
            Shows the page selection dialog
            """
            dialog = PageDialog(self, 1, self.page_count, self.current_page)
            rvalue = dialog.get_value()
            if rvalue:
                self.current_page = rvalue
                self.search()

        def show_about(self):
            """
            Show the about dialog
            """
            dialog = AboutDialog(self)
            dialog.exec()
        

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()