from PyQt5.QtWidgets import *
from sys import argv, exit


class MainApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()

    def title(self):
        self.setWindowTitle("Testing")
        self.setGeometry(0, 0, 300, 500)

    def initUi(self):
        self.title()
        self.show()


if __name__ == "__main__":
    app = QApplication(argv)
    ex = MainApp()
    exit(app.exec_())