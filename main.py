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
            
    def __init__(self, mode="default"):
        super().__init__()
        self.mode = mode
        self.initUi()
        
    def btn_clicked(self):
        clicked_btn: Calender.Date = self.sender()  # 아마 sender가 event를 당하는 객체를 의미하는 듯.
        clicked_btn()
        
        if self.mode == "default":
            p_TEditor = TEditor(clicked_btn)
            p_TEditor.exec_()
        
        elif self.mode == "sub":
            print("testing")
    
    def pn_btn_clicked(self):
        clicked_btn: QPushButton = self.sender()
        print(clicked_btn.text())  # 입력받은 text가 next인지 prev인지 확인해 달력 재구성.
    
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


class TEditor(QDialog):
    """
    요일별 무엇을 할 지 입력해주는 창.
    1. task가 무엇인지 입력할 것. (str)
    2. task의 완료 조건이 무엇인지 선택할 수 있을 것. (ex. 개수 count, long term task ... )
    3. task가 long term인 경우 일괄적으로 설정될 수 있게끔 할 것.
    """
    
    def __init__(self, clicked_btn: Calender.Date):
        super().__init__()
        try:  # 기존의 일정 수정
            self.f = open(SAVE_DIR + "/%d/%d/%d.txt" % (clicked_btn.year, clicked_btn.month, clicked_btn.date), "a")

        except:  # 새로운 일정 추가
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
        1. QLineEdit으로 task 입력
        2. QRadioButton으로 task유형 선택
        3. long term인 경우 별도의 QDialog를 쓰던,
            비활성화된 QLineEdit 2개를 써서 입력할 수 있게끔 만든다..
            활성화 조건 : long term RadioBtn이 활성화 된 경우
        조건: QLineEdit과 QRadioButton의 변경사항은 해당 날짜의 txt에 덮어쓰기 되어야됨.
        입력 사항은 Qtextbox를 통해 확인할 수 있어야 함.
        :return None: None
        """
        self.tb = QTextBrowser()
        self.le = QLineEdit()
        self.cb1 = QCheckBox("일회성 task")
        self.cb2 = QCheckBox("개수가 포함된 task")
        self.lbl_cb2 = QLabel("목표 : ")
        self.le_cb2 = QLineEdit()
        self.le_cb2.setEnabled(False)
        self.cb3 = QCheckBox("기한이 있는 task")  # 완료까지 4일 남음
        self.lbl_cb3 = QLabel("기한 : ")
        self.le_cb3 = QLineEdit()
        self.le_cb3.setEnabled(False)
        self.cb4 = QCheckBox("반복되는 task")  # TODO 반복조건 설정필요
        self.pb_cb4_1 = QPushButton("시작")  # TODO PushButton을 누르면 Calender class로 연결되게끔.
        self.pb_cb4_1.clicked.connect(self.cal_btn_clicked)
        # 이때 Calender class에서는 특정 월에 해당하는 calender를 생성후 push -> 선택한 요일 반환으로 한다.
        # self.pb_cb4_1.setEnabled(False)
        self.pb_cb4_2 = QPushButton("종료")
        self.pb_cb4_2.clicked.connect(self.cal_btn_clicked)
        # self.pb_cb4_2.setEnabled(False)
        self.cblist = [self.cb1, self.cb2, self.cb3, self.cb4]
        # 반복되는 task = 매일하는 운동...
        # 최종적으로는 cb의 조합으로 task를 판별할 수 있도록.
        
        
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