from PyQt5.QtWidgets import *
from sys import argv, exit
from calendar import Calendar as Cal
from datetime import datetime

class MainApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()

    def pushbutten(self):
        self.q_1 = QPushButton("Calender")
        self.q_1.clicked.connect(self.start_calender)
        self.q_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        vbox_1 = QVBoxLayout()

        vbox_1.addWidget(self.q_1)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox_1)

        self.setLayout(hbox)

    def title(self):
        self.setWindowTitle("Testing")
        self.setGeometry(0, 0, 300, 500)
        self.pushbutten()

    def initUi(self):
        self.title()
        self.show()

    def start_calender(self):
        p_calender = Calender()
        p_calender.exec_()


class Calender(QDialog):
    class Date(QPushButton):

        def __init__(self):
            super().__init__()
            self.month = 0
            self.date = 0
            self.updated = False
            self.enabled = False

        def add_date(self, month, date, idx, ref_month):
            self.month = month
            self.date = date
            self.idx = idx
            self.setText(str(self.date))
            self.updated = True
            self.enabled = (month == ref_month)

        def __call__(self):
            print(f"month: {self.month}\ndate: {self.date}\nidx: {self.idx}")

    def __init__(self):
        super().__init__()
        self.initUi()

    def pushbutten(self):
        now = datetime.now()
        cal = Cal()
        days = cal.itermonthdays4(now.year, now.month)
        day_list = [[self.Date() for i in range(7)] for j in range(5)]
        for num, i in enumerate(days):
            idx = (num // 7, num % 7)
            day_list[idx[0]][idx[1]].add_date(i[1], i[2], i[3], now.month)
            day_list[idx[0]][idx[1]].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            day_list[idx[0]][idx[1]].setEnabled(day_list[idx[0]][idx[1]].enabled)

        vbox = QVBoxLayout()
        for i in day_list:
            hbox = QHBoxLayout()
            for j in i:
                hbox.addWidget(j)
            vbox.addLayout(hbox)
        self.setLayout(vbox)

    def initUi(self):
        try:
            self.pushbutten()
            self.setWindowTitle("Calender")
            self.setGeometry(300, 300, 500, 500)
            self.show()
        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = QApplication(argv)
    ex = MainApp()
    exit(app.exec_())