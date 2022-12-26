from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from sys import argv, exit
from calendar import Calendar as Cal
from datetime import datetime
import os


if "Management" in os.listdir():
    pass
else:
    os.mkdir("Management")
SAVE_DIR = "Management"

class MainApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUi()

    def pushbutton(self):
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
        self.pushbutton()

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
            self.year = 0
            self.month = 0
            self.date = 0
            self.updated = False
            self.enabled = False
            
        def add_date(self, year, month, date, idx, ref_month):
            self.year = year
            self.month = month
            self.date = date
            self.idx = idx
            self.setText(str(self.date))
            self.updated = True
            self.enabled = (month == ref_month)

        def __call__(self):
            print(f"year: {self.year}\nmonth: {self.month}\ndate: {self.date}\nidx: {self.idx}")
            # print(f"{Calender.Date.called}th Date")
            
    def __init__(self):
        super().__init__()
        self.initUi()
        
    def btn_clicked(self):
        clicked_btn: Calender.Date = self.sender()
        clicked_btn()
        try:
            f = open(SAVE_DIR + "/%d/%d/%d.txt" % (clicked_btn.year, clicked_btn.month, clicked_btn.date), "w")
        
        except:
            if not "%d" % clicked_btn.year in os.listdir(SAVE_DIR):
                os.mkdir(SAVE_DIR + "/%d" % clicked_btn.year)
            if not "%d" % clicked_btn.month in os.listdir(f"{SAVE_DIR}/{clicked_btn.year}"):
                os.mkdir(SAVE_DIR + "/%d/%d" % (clicked_btn.year, clicked_btn.month))
            f = open(SAVE_DIR + "/%d/%d/%d.txt" % (clicked_btn.year, clicked_btn.month, clicked_btn.date), "w")
            
    def pushbutton(self):
        now = datetime.now()
        cal = Cal()
        days = cal.itermonthdays4(now.year, now.month)
        days_ = cal.itermonthdays4(now.year, now.month)
        for num, i in enumerate(days_): pass
        day_list = [[self.Date() for _ in range(7)] for _ in range((num+1)//7)]

        for num, i in enumerate(days):
            idx = (num // 7, num % 7)
            day_list[idx[0]][idx[1]].add_date(*i, now.month)
            day_list[idx[0]][idx[1]].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            day_list[idx[0]][idx[1]].setEnabled(day_list[idx[0]][idx[1]].enabled)
            day_list[idx[0]][idx[1]].clicked.connect(self.btn_clicked)
            
        L_month = QLabel("%d" % now.month)
        font = L_month.font()
        font.setPointSize(20)
        font.setBold(True)
        L_month.setFont(font)
        L_month.setAlignment(Qt.AlignCenter)
        
        vbox = QVBoxLayout()
        vbox.addWidget(L_month)
        for i in day_list:
            hbox = QHBoxLayout()
            for j in i:
                hbox.addWidget(j)
            vbox.addLayout(hbox)
        self.setLayout(vbox)

    def title(self):
        self.setWindowTitle("Calender")
        self.setGeometry(300, 300, 500, 500)

    def initUi(self):
        self.pushbutton()
        self.title()
        self.show()
            

if __name__ == "__main__":
    app = QApplication(argv)
    ex = MainApp()
    exit(app.exec_())