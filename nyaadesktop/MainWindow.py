# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSplitter,
    QStatusBar,
    QToolBar,
    QTreeView,
    QVBoxLayout,
    QWidget,
)
from . import resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(769, 600)
        self.actionQuit = QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        icon = QIcon()
        icon.addFile(":/icons/quit", QSize(), QIcon.Normal, QIcon.Off)
        self.actionQuit.setIcon(icon)
        self.actionQuit.setShortcutContext(Qt.ApplicationShortcut)
        self.actionSave_torrent_file = QAction(MainWindow)
        self.actionSave_torrent_file.setObjectName("actionSave_torrent_file")
        icon1 = QIcon()
        icon1.addFile(":/icons/download", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSave_torrent_file.setIcon(icon1)
        self.actionDownload = QAction(MainWindow)
        self.actionDownload.setObjectName("actionDownload")
        icon2 = QIcon()
        icon2.addFile(":/icons/open", QSize(), QIcon.Normal, QIcon.Off)
        self.actionDownload.setIcon(icon2)
        self.actionDownload.setMenuRole(QAction.TextHeuristicRole)
        self.actionDownload.setPriority(QAction.NormalPriority)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        icon3 = QIcon()
        icon3.addFile(":/icons/about", QSize(), QIcon.Normal, QIcon.Off)
        self.actionAbout.setIcon(icon3)
        self.actionOpen_in_browser = QAction(MainWindow)
        self.actionOpen_in_browser.setObjectName("actionOpen_in_browser")
        icon4 = QIcon()
        icon4.addFile(":/icons/world", QSize(), QIcon.Normal, QIcon.Off)
        self.actionOpen_in_browser.setIcon(icon4)
        self.actionSettings = QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        icon5 = QIcon()
        icon5.addFile(":/icons/preferences", QSize(), QIcon.Normal, QIcon.Off)
        self.actionSettings.setIcon(icon5)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.search_bar = QHBoxLayout()
        self.search_bar.setObjectName("search_bar")
        self.search_user = QPushButton(self.centralwidget)
        self.search_user.setObjectName("search_user")

        self.search_bar.addWidget(self.search_user)

        self.search_filter = QComboBox(self.centralwidget)
        self.search_filter.setObjectName("search_filter")

        self.search_bar.addWidget(self.search_filter)

        self.search_categories = QComboBox(self.centralwidget)
        self.search_categories.setObjectName("search_categories")

        self.search_bar.addWidget(self.search_categories)

        self.search_text = QLineEdit(self.centralwidget)
        self.search_text.setObjectName("search_text")

        self.search_bar.addWidget(self.search_text)

        self.search_sort = QComboBox(self.centralwidget)
        self.search_sort.setObjectName("search_sort")

        self.search_bar.addWidget(self.search_sort)

        self.search_button = QPushButton(self.centralwidget)
        self.search_button.setObjectName("search_button")
        icon6 = QIcon()
        icon6.addFile(":/icons/search", QSize(), QIcon.Normal, QIcon.Off)
        self.search_button.setIcon(icon6)

        self.search_bar.addWidget(self.search_button)

        self.verticalLayout.addLayout(self.search_bar)

        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName("splitter")
        self.splitter.setOrientation(Qt.Vertical)
        self.results = QTreeView(self.splitter)
        self.results.setObjectName("results")
        self.results.setContextMenuPolicy(Qt.CustomContextMenu)
        self.results.setAlternatingRowColors(True)
        self.results.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.results.setRootIsDecorated(False)
        self.results.setUniformRowHeights(True)
        self.splitter.addWidget(self.results)
        self.frame = QFrame(self.splitter)
        self.frame.setObjectName("frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.splitter.addWidget(self.frame)

        self.verticalLayout.addWidget(self.splitter)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.details_button = QPushButton(self.centralwidget)
        self.details_button.setObjectName("details_button")
        icon7 = QIcon()
        icon7.addFile(":/icons/details", QSize(), QIcon.Normal, QIcon.Off)
        self.details_button.setIcon(icon7)
        self.details_button.setCheckable(True)
        self.details_button.setFlat(True)

        self.horizontalLayout_2.addWidget(self.details_button)

        self.files_button = QPushButton(self.centralwidget)
        self.files_button.setObjectName("files_button")
        icon8 = QIcon()
        icon8.addFile(":/icons/files", QSize(), QIcon.Normal, QIcon.Off)
        self.files_button.setIcon(icon8)
        self.files_button.setCheckable(True)
        self.files_button.setFlat(True)

        self.horizontalLayout_2.addWidget(self.files_button)

        self.comments_button = QPushButton(self.centralwidget)
        self.comments_button.setObjectName("comments_button")
        icon9 = QIcon()
        icon9.addFile(":/icons/comments", QSize(), QIcon.Normal, QIcon.Off)
        self.comments_button.setIcon(icon9)
        self.comments_button.setCheckable(True)
        self.comments_button.setFlat(True)

        self.horizontalLayout_2.addWidget(self.comments_button)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.page_go = QPushButton(self.centralwidget)
        self.page_go.setObjectName("page_go")

        self.horizontalLayout.addWidget(self.page_go)

        self.page_prev = QPushButton(self.centralwidget)
        self.page_prev.setObjectName("page_prev")

        self.horizontalLayout.addWidget(self.page_prev)

        self.page_display = QLabel(self.centralwidget)
        self.page_display.setObjectName("page_display")
        self.page_display.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.page_display)

        self.page_next = QPushButton(self.centralwidget)
        self.page_next.setObjectName("page_next")

        self.horizontalLayout.addWidget(self.page_next)

        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 769, 23))
        self.menuFIle = QMenu(self.menubar)
        self.menuFIle.setObjectName("menuFIle")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolbar_top = QToolBar(MainWindow)
        self.toolbar_top.setObjectName("toolbar_top")
        self.toolbar_top.setContextMenuPolicy(Qt.NoContextMenu)
        self.toolbar_top.setMovable(False)
        self.toolbar_top.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolbar_top)

        self.menubar.addAction(self.menuFIle.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFIle.addAction(self.actionQuit)
        self.menuEdit.addAction(self.actionSave_torrent_file)
        self.menuEdit.addAction(self.actionDownload)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionOpen_in_browser)
        self.menuEdit.addAction(self.actionSettings)
        self.menuHelp.addAction(self.actionAbout)
        self.toolbar_top.addAction(self.actionQuit)
        self.toolbar_top.addAction(self.actionSave_torrent_file)
        self.toolbar_top.addAction(self.actionDownload)
        self.toolbar_top.addAction(self.actionOpen_in_browser)
        self.toolbar_top.addAction(self.actionSettings)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "NyaaDesktop", None)
        )
        self.actionQuit.setText(QCoreApplication.translate("MainWindow", "Quit", None))
        self.actionSave_torrent_file.setText(
            QCoreApplication.translate("MainWindow", "Save .torrent file", None)
        )
        self.actionDownload.setText(
            QCoreApplication.translate("MainWindow", "Download selected", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionDownload.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+S", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", "About", None)
        )
        self.actionOpen_in_browser.setText(
            QCoreApplication.translate("MainWindow", "Open in browser", None)
        )
        self.actionSettings.setText(
            QCoreApplication.translate("MainWindow", "Settings", None)
        )
        self.search_user.setText(
            QCoreApplication.translate("MainWindow", "User...", None)
        )
        self.search_filter.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Filter", None)
        )
        self.search_categories.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Category", None)
        )
        self.search_sort.setPlaceholderText(
            QCoreApplication.translate("MainWindow", "Sort", None)
        )
        self.search_button.setText(
            QCoreApplication.translate("MainWindow", "Search", None)
        )
        self.details_button.setText(
            QCoreApplication.translate("MainWindow", "Details", None)
        )
        self.files_button.setText(
            QCoreApplication.translate("MainWindow", "Files", None)
        )
        self.comments_button.setText(
            QCoreApplication.translate("MainWindow", "Comments", None)
        )
        self.page_go.setText(
            QCoreApplication.translate("MainWindow", "Go to page...", None)
        )
        self.page_prev.setText(
            QCoreApplication.translate("MainWindow", "Previous", None)
        )
        self.page_display.setText(
            QCoreApplication.translate("MainWindow", "Page <b>1</b> / 2", None)
        )
        self.page_next.setText(QCoreApplication.translate("MainWindow", "Next", None))
        self.menuFIle.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", "Edit", None))
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "Help", None))
        self.toolbar_top.setWindowTitle(
            QCoreApplication.translate("MainWindow", "toolBar", None)
        )

    # retranslateUi
