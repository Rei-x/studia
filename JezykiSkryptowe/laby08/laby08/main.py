import sys
from PyQt6.QtWidgets import QApplication

from laby08.browser import LogBrowser


def main():
    app = QApplication(sys.argv)
    ex = LogBrowser()
    ex.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
