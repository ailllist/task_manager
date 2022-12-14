from PyQt5 import QtWidgets
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

class YMcal:
    
    def __init__(self, year, month):
        self.year = year
        self.month = month
    
    def __call__(self):
        print("year : ", self.year)
        print("month : ", self.month)

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
            
        def up_date(self, year, month, date, idx, ref_month):
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
            
    def __init__(self, mode="default"):
        super().__init__()
        self.mode = mode
        self.initUi()
        
    def btn_clicked(self):
        clicked_btn: Calender.Date = self.sender()  # ?????? sender??? event??? ????????? ????????? ???????????? ???.
        clicked_btn()
        
        if self.mode == "default":
            p_TEditor = TEditor(clicked_btn)
            p_TEditor.exec_()
        
        elif self.mode == "sub":
            print("testing")
    
    def pn_btn_clicked(self): # https://hipolarbear.tistory.com/30 -> stack ?????? ??? ??? +1??? ?????? -1??? ??????!.
        clicked_btn: QPushButton = self.sender()
        print(clicked_btn.text())  # ???????????? text??? next?????? prev?????? ????????? ?????? ?????????.
        if clicked_btn.text() == "next":
            self.ym.year = self.ym.year if (self.ym.month + 1) <= 12 else self.ym.year + 1
            self.ym.month = (self.ym.month % 12) + 1
            
        elif clicked_btn.text() == "prev":
            self.ym.year = self.ym.year if (self.ym.month - 1) >= 1 else self.ym.year - 1
            if self.ym.month - 1 < 1:
                self.ym.month = 12
            else:
                self.ym.month = self.ym.month - 1
        self.change_cal()
    
    def change_cal(self):
        print("in cal")
        self.ym()
        cal = Cal()
        days = cal.itermonthdays4(self.ym.year, self.ym.month)
        days_ = cal.itermonthdays4(self.ym.year, self.ym.month)
        for num, i in enumerate(days_): pass
        self.day_list = [[self.Date() for _ in range(7)] for _ in range((num + 1) // 7)]

        for num, i in enumerate(days):
            idx = (num // 7, num % 7)
            self.day_list[idx[0]][idx[1]].up_date(*i, self.ym.month)
            self.day_list[idx[0]][idx[1]].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.day_list[idx[0]][idx[1]].setEnabled(self.day_list[idx[0]][idx[1]].enabled)
            self.day_list[idx[0]][idx[1]].clicked.connect(self.btn_clicked)

        L_month = QLabel("%d" % self.ym.month)
        font = L_month.font()
        font.setPointSize(20)
        font.setBold(True)
        L_month.setFont(font)
        L_month.setAlignment(Qt.AlignCenter)

        tmp_hbox = QHBoxLayout()
        if self.mode == "sub":
            pb_1 = QPushButton("prev")
            pb_1.clicked.connect(self.pn_btn_clicked)
            pb_2 = QPushButton("next")
            pb_2.clicked.connect(self.pn_btn_clicked)
            tmp_hbox.addWidget(pb_1)
            tmp_hbox.addWidget(L_month)
            tmp_hbox.addWidget(pb_2)
        else:
            tmp_hbox.addWidget(L_month)
        vbox = QVBoxLayout()
        vbox.addLayout(tmp_hbox)
        for i in self.day_list:
            hbox = QHBoxLayout()
            for j in i:
                hbox.addWidget(j)
            vbox.addLayout(hbox)
        self.setLayout(vbox)
        
        self.show()
        
    def pushbutton(self):
        now = datetime.now()
        self.ym = YMcal(now.year, now.month)
        
        cal = Cal()
        days = cal.itermonthdays4(self.ym.year, self.ym.month)
        days_ = cal.itermonthdays4(self.ym.year, self.ym.month)
        for num, i in enumerate(days_): pass
        self.day_list = [[self.Date() for _ in range(7)] for _ in range((num+1)//7)]

        for num, i in enumerate(days):
            idx = (num // 7, num % 7)
            self.day_list[idx[0]][idx[1]].up_date(*i, self.ym.month)
            self.day_list[idx[0]][idx[1]].setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.day_list[idx[0]][idx[1]].setEnabled(self.day_list[idx[0]][idx[1]].enabled)
            self.day_list[idx[0]][idx[1]].clicked.connect(self.btn_clicked)
            
        L_month = QLabel("%d" % self.ym.month)
        font = L_month.font()
        font.setPointSize(20)
        font.setBold(True)
        L_month.setFont(font)
        L_month.setAlignment(Qt.AlignCenter)
        
        tmp_hbox = QHBoxLayout()
        if self.mode == "sub":
            pb_1 = QPushButton("prev")
            pb_1.clicked.connect(self.pn_btn_clicked)
            pb_2 = QPushButton("next")
            pb_2.clicked.connect(self.pn_btn_clicked)
            tmp_hbox.addWidget(pb_1)
            tmp_hbox.addWidget(L_month)
            tmp_hbox.addWidget(pb_2)
        else:
            tmp_hbox.addWidget(L_month)
        vbox = QVBoxLayout()
        vbox.addLayout(tmp_hbox)
        for i in self.day_list:
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


class TEditor(QDialog):
    """
    ????????? ????????? ??? ??? ??????????????? ???.
    1. task??? ???????????? ????????? ???. (str)
    2. task??? ?????? ????????? ???????????? ????????? ??? ?????? ???. (ex. ?????? count, long term task ... )
    3. task??? long term??? ?????? ??????????????? ????????? ??? ????????? ??? ???.
    """
    
    def __init__(self, clicked_btn: Calender.Date):
        super().__init__()
        try:  # ????????? ?????? ??????
            self.f = open(SAVE_DIR + "/%d/%d/%d.txt" % (clicked_btn.year, clicked_btn.month, clicked_btn.date), "a")

        except:  # ????????? ?????? ??????
            if not "%d" % clicked_btn.year in os.listdir(SAVE_DIR):
                os.mkdir(SAVE_DIR + "/%d" % clicked_btn.year)
            if not "%d" % clicked_btn.month in os.listdir(f"{SAVE_DIR}/{clicked_btn.year}"):
                os.mkdir(SAVE_DIR + "/%d/%d" % (clicked_btn.year, clicked_btn.month))
            self.f = open(SAVE_DIR + "/%d/%d/%d.txt" % (clicked_btn.year, clicked_btn.month, clicked_btn.date), "w")
        self.clicked_btn = clicked_btn
        self.initUi()
    
    def title(self):
        self.setWindowTitle("Editor")
        self.setGeometry(300, 300, 500, 500)
    
    def cal_btn_clicked(self):
        p_Calender = Calender("sub")
        p_Calender.exec_()
    
    def initUi(self):
        """
        1. QLineEdit?????? task ??????
        2. QRadioButton?????? task?????? ??????
        3. long term??? ?????? ????????? QDialog??? ??????,
            ??????????????? QLineEdit 2?????? ?????? ????????? ??? ????????? ?????????..
            ????????? ?????? : long term RadioBtn??? ????????? ??? ??????
        ??????: QLineEdit??? QRadioButton??? ??????????????? ?????? ????????? txt??? ???????????? ????????????.
        ?????? ????????? Qtextbox??? ?????? ????????? ??? ????????? ???.
        :return None: None
        """
        self.tb = QTextBrowser()
        self.le = QLineEdit()
        self.cb1 = QCheckBox("????????? task")
        self.cb2 = QCheckBox("????????? ????????? task")
        self.lbl_cb2 = QLabel("?????? : ")
        self.le_cb2 = QLineEdit()
        self.le_cb2.setEnabled(False)
        self.cb3 = QCheckBox("????????? ?????? task")  # ???????????? 4??? ??????
        self.lbl_cb3 = QLabel("?????? : ")
        self.le_cb3 = QLineEdit()
        self.le_cb3.setEnabled(False)
        self.cb4 = QCheckBox("???????????? task")  # TODO ???????????? ????????????
        self.pb_cb4_1 = QPushButton("??????")  # TODO PushButton??? ????????? Calender class??? ???????????????.
        self.pb_cb4_1.clicked.connect(self.cal_btn_clicked)
        # ?????? Calender class????????? ?????? ?????? ???????????? calender??? ????????? push -> ????????? ?????? ???????????? ??????.
        # self.pb_cb4_1.setEnabled(False)
        self.pb_cb4_2 = QPushButton("??????")
        self.pb_cb4_2.clicked.connect(self.cal_btn_clicked)
        # self.pb_cb4_2.setEnabled(False)
        self.cblist = [self.cb1, self.cb2, self.cb3, self.cb4]
        # ???????????? task = ???????????? ??????...
        # ?????????????????? cb??? ???????????? task??? ????????? ??? ?????????.
        
        
        phbox1 = QHBoxLayout()
        phbox1.addWidget(self.lbl_cb2)
        phbox1.addWidget(self.le_cb2)

        phbox2 = QHBoxLayout()
        phbox2.addWidget(self.lbl_cb3)
        phbox2.addWidget(self.le_cb3)
        
        phbox3 = QHBoxLayout()
        phbox3.addWidget(self.pb_cb4_1)
        phbox3.addWidget(self.pb_cb4_2)

        vbox = QVBoxLayout()
        vbox.addWidget(self.le)
        vbox.addWidget(self.cb1)
        vbox.addWidget(self.cb2)
        vbox.addLayout(phbox1)
        vbox.addWidget(self.cb3)
        vbox.addLayout(phbox2)
        vbox.addWidget(self.cb4)
        vbox.addLayout(phbox3)
        hbox = QHBoxLayout()
        hbox.addWidget(self.tb)  # TODO need to fix align error
        hbox.addLayout(vbox)
        self.setLayout(hbox)
        
        self.title()
        self.show()

if __name__ == "__main__":
    app = QApplication(argv)
    ex = MainApp()
    exit(app.exec_())