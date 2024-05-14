import datetime
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QDateEdit,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QFileDialog,
)

from laby08.detail_viewer import LogDetailViewer
from laby08.file_manager import FileManager
from laby08.log_parser import ApacheLog


class LogBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self.file_manager = FileManager()
        self.log_detail_viewer = LogDetailViewer()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Log Browser")
        self.setGeometry(100, 100, 900, 500)

        mainLayout = QVBoxLayout()

        topLayout = QVBoxLayout()
        topLayout.setSpacing(10)
        fileLayout = QHBoxLayout()
        filterLayout = QHBoxLayout()

        self.pathLabel = QLabel("")
        self.openButton = QPushButton("Open")
        self.openButton.setFixedWidth(100)
        self.openButton.clicked.connect(self.openFileDialog)

        self.fromDateEdit = QDateEdit()
        self.fromDateEdit.setCalendarPopup(True)
        self.fromDateEdit.setDate(datetime.datetime.now() - datetime.timedelta(days=7))
        self.fromDateEdit.setFixedWidth(150)
        self.fromDateEdit.setDisabled(True)

        self.toDateEdit = QDateEdit()
        self.toDateEdit.setCalendarPopup(True)
        self.toDateEdit.setDate(datetime.datetime.now())
        self.toDateEdit.setFixedWidth(150)
        self.toDateEdit.setDisabled(True)

        self.filterButton = QPushButton("Filter")
        self.filterButton.setFixedWidth(100)
        self.filterButton.setDisabled(True)

        self.filterButton.clicked.connect(self.applyDateFilter)

        fileLayout.addWidget(self.pathLabel)
        fileLayout.addWidget(self.openButton)

        filterLayout.addWidget(QLabel("From"))
        filterLayout.addWidget(self.fromDateEdit)

        filterLayout.addWidget(QLabel("To"))
        filterLayout.addWidget(self.toDateEdit)

        filterLayout.addWidget(self.filterButton)
        filterLayout.addStretch(1)
        topLayout.addLayout(fileLayout)

        horizontalLine = QLabel()
        horizontalLine.setFrameStyle(1)
        horizontalLine.setFixedHeight(1)
        topLayout.addWidget(horizontalLine)

        topLayout.addLayout(filterLayout)

        middleLayout = QHBoxLayout()
        self.logListWidget = QListWidget()
        self.logListWidget.itemClicked.connect(self.select_log)
        middleLayout.addWidget(self.logListWidget, 1)
        middleLayout.addWidget(self.log_detail_viewer, 2)

        bottomLayout = QHBoxLayout()
        self.prevButton = QPushButton("Previous")
        self.nextButton = QPushButton("Next")
        self.currentPageLabel = QLabel("Page 0/0")
        self.prevButton.clicked.connect(self.showPreviousPage)
        self.nextButton.clicked.connect(self.showNextPage)
        bottomLayout.addWidget(self.prevButton)
        bottomLayout.addStretch(1)
        bottomLayout.addWidget(self.currentPageLabel)
        bottomLayout.addStretch(1)
        bottomLayout.addWidget(self.nextButton)

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(middleLayout)
        mainLayout.addLayout(bottomLayout)
        self.updatePagination()
        self.setLayout(mainLayout)

    def applyDateFilter(self):
        from_date = self.fromDateEdit.date().toPyDate()
        to_date = self.toDateEdit.date().toPyDate()
        self.file_manager.apply_date_filter(from_date, to_date)
        self.updateListWidget()
        self.updatePagination()

    def updateListWidget(self):
        self.logListWidget.clear()
        page_lines = self.file_manager.get_page_lines()
        for line in page_lines:
            self.logListWidget.addItem(line.strip())

    def updatePagination(self):
        if self.file_manager.total_pages == 0:
            self.currentPageLabel.setText("Page 0/0")
        else:
            self.currentPageLabel.setText(
                f"Page {self.file_manager.current_page + 1}/{self.file_manager.total_pages}"
            )
        if self.file_manager.current_page == 0:
            self.prevButton.setEnabled(False)
        else:
            self.prevButton.setEnabled(True)

        if (
            self.file_manager.current_page == self.file_manager.total_pages - 1
            or self.file_manager.total_pages == 0
        ):
            self.nextButton.setEnabled(False)
        else:
            self.nextButton.setEnabled(True)

    def updateDateFilter(self):
        if not self.file_manager.filtered_lines:
            return
        self.fromDateEdit.setDisabled(False)
        self.toDateEdit.setDisabled(False)

        firstLog = ApacheLog.from_log(self.file_manager.filtered_lines[0])
        lastLog = ApacheLog.from_log(self.file_manager.filtered_lines[-1])

        self.fromDateEdit.setDate(firstLog.timestamp)
        self.toDateEdit.setDate(lastLog.timestamp)
        self.fromDateEdit.setMinimumDate(firstLog.timestamp)
        self.fromDateEdit.setMaximumDate(lastLog.timestamp)

    def select_log(self, item):
        log = ApacheLog.from_log(item.text())
        self.log_detail_viewer.set_log_details(log)

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open Log File",
            "",
            "Log Files (*.log);;All Files (*)",
        )
        if fileName:
            self.filterButton.setDisabled(False)
            self.pathLabel.setText(fileName)
            self.file_manager.load_log_file(fileName)
            self.updateListWidget()
            self.updateDateFilter()
            self.updatePagination()

    def showNextPage(self):
        if self.file_manager.next_page():
            self.updateListWidget()
            self.updatePagination()

    def showPreviousPage(self):
        if self.file_manager.previous_page():
            self.updateListWidget()
            self.updatePagination()
