from PyQt6.QtWidgets import QFrame, QVBoxLayout, QGridLayout, QLabel

from laby08.log_parser import ApacheLog


class LogDetailViewer(QFrame):
    def __init__(self):
        super().__init__()
        self.valueLabels = {}
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
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

    def set_log_details(self, log: ApacheLog):
        self.valueLabels["Remote host"].setText(log.host_address)
        self.valueLabels["Date"].setText(log.timestamp.strftime("%Y-%m-%d"))
        self.valueLabels["Time"].setText(log.timestamp.strftime("%H:%M:%S"))
        self.valueLabels["Timezone"].setText(log.timestamp.strftime("%z"))
        self.valueLabels["Status code"].setText(str(log.http_code))
        self.valueLabels["Method"].setText(log.http_method)
        self.valueLabels["Resource"].setText(log.url)
        self.valueLabels["Size"].setText(str(log.number_of_bytes))
