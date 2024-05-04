import datetime
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QDateEdit,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QListWidget,
    QFrame,
    QFileDialog,
)


from laby08.log_parser import ApacheLog


class LogBrowser(QWidget):
    def __init__(self):
        self.valueLabels = {}
        super().__init__()
        self.initUI()
        self.current_page = 0
        self.lines_per_page = 100  # Number of lines to display per page
        self.total_pages = 0
        self.file_lines = []

    def initUI(self):
        self.setWindowTitle("Log Browser")
        self.setGeometry(100, 100, 900, 500)

        mainLayout = QVBoxLayout()

        topLayout = QHBoxLayout()
        self.pathLabel = QLabel("/home/student/NASA")
        self.openButton = QPushButton("Open")
        self.openButton.clicked.connect(self.openFileDialog)
        self.fromDateEdit = QDateEdit()
        self.fromDateEdit.setDate(datetime.datetime.now() - datetime.timedelta(days=7))
        self.toDateEdit = QDateEdit()
        self.toDateEdit.setDate(datetime.datetime.now())
        self.filterButton = QPushButton("Filter")
        self.filterButton.clicked.connect(self.applyDateFilter)

        topLayout.addWidget(QLabel("From"))
        topLayout.addWidget(self.fromDateEdit)
        topLayout.addWidget(QLabel("To"))
        topLayout.addWidget(self.toDateEdit)
        topLayout.addWidget(self.filterButton)
        topLayout.addWidget(self.pathLabel)
        topLayout.addWidget(self.openButton)

        middleLayout = QHBoxLayout()
        self.logListWidget = QListWidget()
        self.logListWidget.itemClicked.connect(self.select_log)
        middleLayout.addWidget(self.logListWidget, 1)

        self.detailsFrame = QFrame()
        detailsLayout = QVBoxLayout(self.detailsFrame)
        self.createDetailsWidgets(detailsLayout)
        middleLayout.addWidget(self.detailsFrame, 2)

        bottomLayout = QHBoxLayout()
        self.prevButton = QPushButton("Previous")
        self.nextButton = QPushButton("Next")
        self.prevButton.clicked.connect(self.showPreviousPage)
        self.nextButton.clicked.connect(self.showNextPage)
        bottomLayout.addWidget(self.prevButton)
        bottomLayout.addStretch()
        bottomLayout.addWidget(self.nextButton)

        mainLayout.addLayout(topLayout)
        mainLayout.addLayout(middleLayout)
        mainLayout.addLayout(bottomLayout)

        self.setLayout(mainLayout)

    def applyDateFilter(self):
        from_date = self.fromDateEdit.date().toPyDate()
        to_date = self.toDateEdit.date().toPyDate()
        self.filtered_lines = [
            line
            for line in self.file_lines
            if from_date
            <= datetime.datetime.strptime(
                ApacheLog.from_log(line).timestamp.strftime("%Y-%m-%d"), "%Y-%m-%d"
            ).date()
            <= to_date
        ]
        self.total_pages = (len(self.filtered_lines) - 1) // self.lines_per_page + 1
        self.current_page = 0
        self.updateListWidget()

    def select_log(self, item):
        log = ApacheLog.from_log(item.data(0))

        self.valueLabels["Remote host"].setText(log.host_address)
        self.valueLabels["Date"].setText(log.timestamp.strftime("%Y-%m-%d"))
        self.valueLabels["Time"].setText(log.timestamp.strftime("%H:%M:%S"))
        self.valueLabels["Timezone"].setText(log.timestamp.strftime("%z"))
        self.valueLabels["Status code"].setText(str(log.http_code))
        self.valueLabels["Method"].setText(log.http_method)
        self.valueLabels["Resource"].setText(log.url)
        self.valueLabels["Size"].setText(str(log.number_of_bytes))

    def createDetailsWidgets(self, layout):
        gridLayout = QGridLayout()

        labels = [
            "Remote host",
            "Date",
            "Time",
            "Timezone",
            "Status code",
            "Method",
            "Resource",
            "Size",
        ]

        for index, label in enumerate(labels):
            labelWidget = QLabel(f"{label}:")
            valueLabel = QLabel()
            gridLayout.addWidget(labelWidget, index, 0)
            gridLayout.addWidget(valueLabel, index, 1)
            self.valueLabels[label] = valueLabel

        layout.addLayout(gridLayout)

    def openFileDialog(self):
        fileName, _ = QFileDialog.getOpenFileName(
            self,
            "Open Log File",
            "",
            "Log Files (*.log);;All Files (*)",
        )
        if fileName:
            self.pathLabel.setText(fileName)
            self.loadLogFile(fileName)

    def loadLogFile(self, filePath):
        self.file_lines = []
        with open(filePath, "r") as file:
            self.file_lines = file.readlines()
        self.total_pages = (len(self.file_lines) - 1) // self.lines_per_page + 1
        self.current_page = 0
        self.updateListWidget()

    def updateListWidget(self):
        self.logListWidget.clear()
        start_index = self.current_page * self.lines_per_page
        end_index = start_index + self.lines_per_page
        for line in self.file_lines[start_index:end_index]:
            self.logListWidget.addItem(line.strip())

    def showNextPage(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self.updateListWidget()

    def showPreviousPage(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.updateListWidget()


def main():
    app = QApplication(sys.argv)
    ex = LogBrowser()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
