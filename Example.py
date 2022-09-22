from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QLineEdit, QTextBrowser, QLabel, QSizePolicy, QSizeGrip, \
    QVBoxLayout, QHBoxLayout, QGridLayout, QProgressBar, QRadioButton, QDialog, QCheckBox, QShortcut
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtCore import QBasicTimer, QPoint, Qt
from random import shuffle
import os
from bs4 import BeautifulSoup
from requests import get
from copy import copy, deepcopy
from wmi import WMI
from pyautogui import press
from sys import argv, exit
from shutil import rmtree


class MainApp(QWidget):
    
    def __init__(self):
        global target
        super().__init__()
        path = os.getenv('AppData')
        path_list = path.split('\\')
        path_list.reverse()
        while path_list[0].upper() != 'APPDATA':
            del path_list[0]
        path_list.reverse()
        path = '/'.join(path_list)
        path = path.replace('C:/', 'C://')
        if not os.path.isdir(path + "/local"):
            b_target = path + "/local"
            os.mkdir(b_target)
        if not os.path.isdir(str(path) + "/local/Eng program"):
            target = str(path) + "/local/Eng program"
            os.mkdir(target)
        target = str(path) + "/local/Eng program"
        user_names = ['            WGS4PXVN', 'BTLA83010S5B128I']
        c = WMI()
        m = c.Win32_PhysicalMedia()
        print('사용자를 확인합니다.')
        for i in user_names:
            if i == m[0].SerialNumber:
                print('확인 완료!')
                user = True
                break
            else:
                user = True
        if user == True:
            # t = open(target + '/all_eng.txt', 'r')
            # c_list = [i.rstrip('\n') for i in t.readlines()]
            # t.close()
            # for i in c_list:
            #     try:
            #         o = open(target + '/%s' % i)
            #         if len(o) != len(c_list):
            #             print('critical error')
            #     except:
            #         print('error occured')
            self.initUi()
        else:
            self.FinitUI()
    
    def FinitUI(self):
        q = QLabel('잘못된 접근입니다.')
        v = QVBoxLayout(self)
        v.addWidget(q)
        self.setLayout(v)
        self.show()
    
    def resizeText(self, event):
        defaultSize = 9
        for bu in self.buttons:
            if self.rect().width() // 40 > defaultSize:
                f = QFont('', self.rect().width() // 40)
            else:
                f = QFont('', defaultSize)
            
            bu.setFont(f)
    
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    
    def pushbutten(self):
        global con
        con = os.path.isfile(target + '/s_all_eng.txt')
        self.q_1 = QPushButton('단어검색')
        self.q_1.clicked.connect(self.mode1)
        self.q_2 = QPushButton('단어분석')
        self.q_2.clicked.connect(self.mode2)
        self.q_3 = QPushButton('K2E 학습')
        self.q_3.clicked.connect(self.mode3)
        self.q_4 = QPushButton('통합설정')
        self.q_4.setEnabled(False)
        self.q_5 = QPushButton('단어암기')
        self.q_5.clicked.connect(self.mode5)
        self.q_6 = QPushButton('구간설정')
        self.q_6.clicked.connect(self.mode6)
        self.q_7 = QPushButton('빠른입력')
        self.q_7.clicked.connect(self.mode7)
        self.q_8 = QPushButton('관계분석')
        self.q_8.clicked.connect(self.mode8)
        self.q_1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.q_2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.q_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.q_4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.q_5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.q_6.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.q_7.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.q_8.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.buttons = [self.q_1, self.q_2, self.q_3, self.q_4, self.q_5, self.q_6, self.q_7, self.q_8]
        self.q_1.resizeEvent = self.resizeText
        self.mousepressEvent = self.mouseMoveEvent
        self.sizegrip_1 = QSizeGrip(self)
        self.sizegrip_1.setVisible(True)
        self.sizegrip_2 = QSizeGrip(self)
        self.sizegrip_2.setVisible(True)
        self.sizegrip_3 = QSizeGrip(self)
        self.sizegrip_3.setVisible(True)
        self.sizegrip_4 = QSizeGrip(self)
        self.sizegrip_4.setVisible(True)
        
        vbox_1 = QVBoxLayout()
        vbox_1.addWidget(self.sizegrip_1)
        vbox_1.addStretch()
        vbox_1.addWidget(self.q_1)
        vbox_1.addWidget(self.q_2)
        vbox_1.addWidget(self.q_3)
        vbox_1.addWidget(self.q_4)
        vbox_1.addStretch()
        vbox_1.addWidget(self.sizegrip_2)
        
        vbox_2 = QVBoxLayout()
        
        vbox_2.addWidget(self.sizegrip_3)
        vbox_2.addStretch()
        vbox_2.addWidget(self.q_5)
        vbox_2.addWidget(self.q_6)
        vbox_2.addWidget(self.q_7)
        vbox_2.addWidget(self.q_8)
        vbox_2.addStretch()
        vbox_2.addWidget(self.sizegrip_4)
        
        self.hbox = QHBoxLayout()
        
        self.hbox.addLayout(vbox_1)
        self.hbox.addLayout(vbox_2)
        
        self.setLayout(self.hbox)
    
    def title(self):
        
        self.setWindowTitle('ENG_PROTO')
        self.setGeometry(0, 0, 300, 500)
    
    def initUi(self):
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.title()
        self.pushbutten()
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        self.resizing = False
        
        self.show()
        
        self.out = QShortcut(QKeySequence("Ctrl+E"), self)
        self.out.activated.connect(self.close)
        try:
            f = open('튜토리얼을_다시_보고_싶으면_이파일을_지우세요.txt', 'r')
        except:
            index_1 = index()
            index_1.exec_()
    
    def mode1(self):
        
        e_mode1 = mode_1()
        e_mode1.exec_()
    
    def mode2(self):
        
        # rmtree(target)
        # os.mkdir(target)
        e_mode2 = mode_2()
        e_mode2.exec()
    
    def mode3(self):
        
        e_mode3 = mode_3()
        e_mode3.exec_()
    
    def mode5(self):
        
        e_mode5 = mode_5()
        e_mode5.exec_()
    
    def mode6(self):
        
        e_mode6 = mode_6()
        e_mode6.exec_()
        try:
            print(e_mode6.st, e_mode6.ed)
            engs = open(target + '/all_eng.txt', 'r')
            kors = open(target + '/all_kor.txt', 'r', encoding='utf-8')
            
            s_engs = open(target + '/s_all_eng.txt', 'w')
            s_kors = open(target + '/s_all_kor.txt', 'w', encoding='utf-8')
            
            self.b_kor_list = kors.readlines()
            self.b_eng_list = engs.readlines()
            
            for i in range(e_mode6.st, e_mode6.ed):
                s_engs.write(self.b_eng_list[i].rstrip('\n'))
                s_engs.write('\n')
                s_kors.write(self.b_kor_list[i].rstrip('\n'))
                s_kors.write('\n')
            engs.close()
            kors.close()
            s_engs.close()
            s_kors.close()
        except:
            pass
    
    def mode7(self):
        
        e_mode7 = mode_7()
        e_mode7.exec_()
    
    def mode8(self):
        
        e_mode8 = sub_mode_8()
        e_mode8.exec_()


class index(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        
        self.notice = QTextBrowser()
        self.notice.append('Ctrl + E하면 나가집니다')
        self.notice.append(
            '경고 : 1년정도 사용하면서 프로그램상의 오류만 있었지, 학습에 지장될정도로 큰 오류, 예를 들면 영어뜻과 한국어가 틀렸다거나...이런건 없었습니다. 그래도 어디선가 문제가 생길 수도 있기 때문에 너무 맹신하지는 마세요. (가끔 오류가 있었지만, 대부분 손잘못이였음)')
        self.notice.append('\n\n사용방법')
        self.notice.append('1. 단어검색 혹은 빠른입력 모드를 통해 new.txt파일을 생성합니다. 예전 파일에 액세스가 가능하고 형식만 맞춘다면 어떤 텍스트 파일이라도 사용이 가능합니다.')
        self.notice.append('형식 : 파일의 이름은 new.txt고정, 파일 속 내용은 영단어/한글(줄바꿈)...')
        self.notice.append('2. 단어분석 모드를 진행합니다. -> 학습에 사용될 유사도 파일을 만드는 과정')
        self.notice.append('3. 구간설정을 통해 new.txt에서 자신이 외우고 싶은 부분만 선택합니다.')
        self.notice.append('4. 나머지 기능을 활용해 학습을 진행하면 됩니다.')
        self.notice.append('\n\n활용방법')
        self.notice.append('1. 단어검색을 통해 모르는 단어를 찾아가면서 영어 지문 분석')
        self.notice.append('2. 자신만의 단어장을 만들고 다양한 단어암기 모드를 통한 암기')
        self.notice.append('\n\n세부설명')
        self.notice.append('원래 위에서 서술한 문제 해결하기 위해 검토하는 프로그램이 있었는데 까먹고 추가 안했습니다...쓰레드써서 백그라운드에서 실행시킬려고 준비중입니다.')
        self.notice.append('단어검색 : 2개의 사전으로부터 단어를 검색합니다.')
        self.notice.append('단어분석 : 단어간의 유사도를 분석합니다.')
        self.notice.append('K2E 학습 : 한국어->영어 학습을 진행합니다. 5지선다입니다.')
        self.notice.append('통합설정 : 언젠가 커스터마이징이 가능해질껍니다.')
        self.notice.append('단어암기 : 10개씩 끊어가며 단어를 암기합니다. retry를 누르면 단어가 다시 추가됩니다.')
        self.notice.append('구간설정 : 단어분석이 끝난뒤 진행해야되며, 학습에 사용될 단어 구간을 설정합니다.')
        self.notice.append('빠른입력 : 단어장에 단어를 추가합니다. 편의를 위해 한/영이 자동으로 변환됩니다.')
        self.notice.append('관계분석 : 특정 유사도이상을 지닌 단어들을 분석해 txt파일로 제작해줍니다.')
        self.notice.append('단어분석 -> 구간설정 -> 학습 순으로 진행되어야 합니다.')
        self.notice.append('\n\n각각의 프로그램의 목표는 다음과 같습니다.')
        self.notice.append('단어검색 : 더 많은 사전을 추가할 예정입니다.')
        self.notice.append('단어분석 : 분석에 필요한 시간을 줄이고, 매번 처음부터 시작하는것이 아니라 기존의 데이터에 덧씌우는 형태로 제작할 것입니다.')
        self.notice.append('K2E 학습 : 시험지 만들 의향있음.')
        self.notice.append('통합설정 : 프로그램이 복잡해지면 환경설정과 같은 역할을 할 것입니다.')
        self.notice.append('단어암기 : 끊는 개수를 설정할 수 있게끔 고칠것입니다.')
        self.notice.append('구간설정 : 안귀찮게 할 수 있는 방안을 고민중입니다.')
        self.notice.append('빠른입력 : 거의 최종본입니다.')
        self.notice.append('관계분석 : 오프라인 단어장 형성을 최종 목표로 하고있으며, 원하는 단어만 추출할 수 있게끔 제작하고자 합니다. 현재는 수작업으로 해주셔야 합니다.')
        self.notice.append('조만간 커스터마이징 요소를 추가할 것입니다. 제가 프로그램을 예쁘게 못만들겠거든요.')
        self.notice.append('\n\n아는데 안고치는거')
        self.notice.append('1. 처음부터 단어분석하는 것 : 불편한거 아는데 고치는데 시간이 조금 걸립니다...')
        self.notice.append('2. 지난학습 이어하기 : 예전에 만든적 있어서 조만간 추가될듯합니다.')
        self.notice.append('3. 안예쁨 : 색조합정도는 자유롭게 할 수 있게끔 만들의향은 있는데 GUI는 딱히 기대하지 않는게...')
        self.notice.append('4. 관계분석도 단어분석처럼 진행도 표시는 해줄 수 있긴함.')
        self.notice.append('\n\n아는데 못고치는거')
        self.notice.append('1. 좀 많이 오래쓰다 보면(2시간 이상) 간간히 틩깁니다. 왜그런지 모르겠어요.')
        self.notice.append('2. 단어검색 많이하면 중간에 프로그램이 멈춥니다. 프로그램상 오류가 아니라 웹사이트의 문제라 고칠방법이 없어요. 그냥 껏다 다시 키는게 답입니다.')
        self.notice.append('\n\n그 외 오류사항')
        self.notice.append('페메로 보내시면됩니다.')
        self.notice.append('\n\n주의사항')
        self.notice.append(
            '단어분석은 한번 진행한 이상 왠만해서 누르지 마세요. 1800개 기준 10분 걸립니다...물론 데이터가 갱신될때마다 해줘야겠지만, 실수로 누른다거나 생각없이 누르면 오열할 수도 있습니다. 기존의 데이터가 날아가거든요.')
        
        self.cb = QCheckBox('다시 보지 않음')
        self.cb.stateChanged.connect(self.don_t_show)
        vbox = QVBoxLayout()
        vbox.addWidget(self.notice)
        vbox.addWidget(self.cb)
        self.setLayout(vbox)
        self.setWindowTitle('notice')
        self.setGeometry(300, 300, 500, 900)
        self.show()
    
    def don_t_show(self, state):
        if state == Qt.Checked:
            f = open('튜토리얼을_다시_보고_싶으면_이파일을_지우세요.txt', 'w')
            f.write('True')
            f.close()
        else:
            pass


class mode_1(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def m_step(self):
        self.txt = self.le.text()
        self.le.clear()
        if self.le.text() == '':
            self.crowl_control()
    
    def initUI(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.le = QLineEdit()
        self.le.returnPressed.connect(self.m_step)
        # self.le.returnPressed.connect(self.crowl_control)
        
        self.tb = QTextBrowser()
        self.tb.setAcceptRichText(True)
        self.tb.setOpenExternalLinks(True)
        
        grid = QGridLayout()
        self.setLayout(grid)
        
        grid.addWidget(QLabel('input: '), 0, 0)
        grid.addWidget(QLabel('output: '), 1, 0)
        
        grid.addWidget(self.le, 0, 1)
        grid.addWidget(self.tb, 1, 1)
        
        self.setWindowTitle('mode1 : 단어검색')
        self.setGeometry(300, 300, 500, 500)
        self.show()
    
    def crowl_control(self):
        text = self.txt
        text_list = text.split(", ")
        self.le.clear()
        for text in text_list:
            self.tb.append(text)
            mean_1 = self.crawling(text)
            mean_2 = self.old_crawling(text)
            self.tb.append('word_Ref : %s' % mean_1)
            self.tb.append('naver : %s\n' % mean_2)
    
    def crawling(self, word):
        
        word_list = []
        url = 'https://www.wordreference.com/enko/' + word
        print(url)
        response = get(url)
        soup = BeautifulSoup(response.content, "lxml", from_encoding='utf-8')
        
        try:
            e = soup.find('div', {'class': 'notfound'})
            try:
                if len(e) > 0: return word_list
            except:
                pass
            a = soup.find('div', {'id': 'articleWRD'}).find('table', {'class': 'WRD'}).findAll('tr', {'class': 'even'})
            b = soup.find('div', {'id': 'articleWRD'}).find('table', {'class': 'WRD'}).findAll('tr', {'class': 'odd'})
            for i in a:
                try:
                    a = i.find('td', {'class': 'ToWrd'}).get_text()
                    a_1 = i.find('td', {'class': 'ToWrd'}).find('em').get_text()
                    a_str = a.replace(a_1, "")
                    if a_str.count(',') == 0:
                        word_list.append(a_str.rstrip())
                    elif a_str.count(',') != 0:
                        a_list = a_str.split(', ')
                        for i in range(0, len(a_list)):
                            word_list.append(a_list[i].rstrip())
                except:
                    continue
            for i in b:
                try:
                    b = i.find('td', {'class': 'ToWrd'}).get_text()
                    b_1 = i.find('td', {'class': 'ToWrd'}).find('em').get_text()
                    b_str = b.replace(b_1, "")
                    if b_str.count(',') == 0:
                        word_list.append(b_str.rstrip())
                    elif b_str.count(',') != 0:
                        b_list = b_str.split(', ')
                        for i in range(0, len(b_list)):
                            word_list.append(b_list[i].rstrip())
                except:
                    continue
        except:
            pass
        word_list = list(set(word_list))
        return word_list
    
    def old_crawling(self, word):
        
        mean_list = []
        url = 'http://endic.naver.com/search.nhn?query=' + word
        # print(url)
        response = get(url)
        soup = BeautifulSoup(response.content, "lxml", from_encoding='utf-8')
        try:
            a = soup.find('dl', {'class': 'list_e2'}).find('dt', {'class': 'first'}).find('span',
                                                                                          {'class': 'fnt_e30'}).find(
                'a')
            new_url = 'https://endic.naver.com' + a['href']
            print(new_url)
            n_response = get(new_url)
            n_soup = BeautifulSoup(n_response.content, "lxml", from_encoding='utf-8')
            try:
                for j in n_soup.findAll('dl', {'class': 'list_a3'}):
                    for i in j.select('dt'):
                        i = str(i.find('em', {'class': 'align_line'}).find('span', {'class': 'fnt_k06'}).get_text())
                        if len(i.strip()) != 0:
                            mean_list.append(i.strip())
            except:
                pass
        except:
            pass
        if len(mean_list) != 0:
            mean_list = ', '.join(mean_list)
            mean_list = mean_list.split(', ')
        
        return mean_list


class mode_2(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def make_sim(self, word_1, word_2):
        
        sim_list = []
        
        if len(word_1) > len(word_2):
            min_word = word_2
            max_word = word_1
        else:
            min_word = word_1
            max_word = word_2
        
        while len(min_word) != 0:
            index_list = []
            word_list = []
            del_list = []
            
            for i in range(len(max_word)):
                if min_word[0] == max_word[i]:
                    index_list.append(i)
            
            for i in range(len(min_word)):
                p_sim = 1
                i = min_word[0:i + 1]
                for j in index_list:
                    for k in range(j, len(max_word)):
                        if i == max_word[j:k + 1]:
                            if len(i) > 1:
                                del_list.append(i)
            try:
                del_list.reverse()
                min_word = min_word.replace(del_list[0], '', 1)
                sim_list.append(len(del_list[0]))
            except:
                min_word = min_word.replace(min_word[0], '', 1)
        
        sim = round(sum(sim_list) / ((len(word_1) + len(word_2)) / 2), 3)
        
        return sim
    
    def initUI(self):
        
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.target = target
        self.pbar = QProgressBar(self)
        self.pbar.resize(700, 20)
        
        f = open("new.txt", 'r', encoding='utf-8')
        lines = f.readlines()
        word = {}
        for i in lines:
            i = i.strip('\n')
            i = i.split('/')
            
            if i[0] in word:
                i_0_list = word[i[0]].split(', ')
                i_1_list = i[1].split(', ')
                all_list = i_0_list + i_1_list
                all_list = set(all_list)
                all_list = list(all_list)
                eng_word = ', '.join(all_list)
                word[str(i[0])] = eng_word
            else:
                word[str(i[0])] = str(i[1])
        
        eng = list(word.keys())
        kor = list(word.values())  # 새로 들어올 것들
        try:
            o_eng = open(self.target + '/all_eng.txt', 'r')
            o_kor = open(self.target + '/all_kor.txt', 'r', encoding='utf-8')
            self.o_engs = [i.rstrip('\n') for i in o_eng.readlines()]
            self.o_kors = [i.rstrip('\n') for i in o_kor.readlines()]
            self.add_eng = list(set(eng) - set(self.o_engs))
            self.add_kor = []
            o_eng.close()
            o_kor.close()
            for i in self.add_eng:
                self.add_kor.append(word[str(i)])
            total_word = self.o_engs + self.add_eng
            o_eng = open(self.target + '/all_eng.txt', 'a')
            o_kor = open(self.target + '/all_kor.txt', 'a', encoding='utf-8')
            for i in range(0, len(self.add_eng)):
                o_eng.write('%s\n' % self.add_eng[i])
                o_kor.write('%s\n' % self.add_kor[i])
            o_eng.close()
            o_kor.close()
        
        except:
            engs = open(self.target + '/all_eng.txt', 'w')
            kors = open(self.target + '/all_kor.txt', 'w', encoding='utf-8')
            for i in range(0, len(eng)):
                engs.write(eng[i])
                engs.write('\n')
                kors.write(kor[i])
                kors.write('\n')
            engs.close()
            kors.close()
            self.add_eng = []
        all_engs = open(target + '/all_eng.txt', 'r')
        self.index_list = []
        
        b_index_list = all_engs.readlines()
        for i in b_index_list: self.index_list.append(i.rstrip('\n'))
        self.c_index_list = deepcopy(self.index_list)
        self.b_index_list = deepcopy(self.index_list)
        self.sub_index_list = deepcopy(self.add_eng)
        print(len(self.add_eng))
        if len(self.add_eng) != 0:
            self.config = True
        else:
            if len(self.o_engs) == 0:
                self.config = False
            else:
                self.config = 'close'
        self.timer = QBasicTimer()
        self.doAction()
        self.step = 0
        self.QL = QLabel('Ready')
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.pbar)
        vbox.addWidget(self.QL)
        vbox.addStretch(1)
        
        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        
        self.setLayout(hbox)
        
        self.setWindowTitle('mode2 : 단어분석')
        self.setGeometry(300, 300, 1000, 20)
        self.show()
    
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    
    def timerEvent(self, e):
        if self.config == True:
            self.mousepressEvent = self.mouseMoveEvent
            sim_list = []
            self.QL.setText(
                '%d/%d analyzing.....' % (len(self.b_index_list) - len(self.index_list), len(self.b_index_list)))
            if len(self.index_list) == 0:
                self.QL.setText('Finished!')
                self.timer.stop()
                self.close()
                return
            self.step = 100 - round((100 * len(self.index_list)) / len(self.b_index_list), 0)
            self.pbar.setValue(self.step)
            if self.index_list[0] in self.add_eng:
                f = open(target + '/%s.txt' % self.index_list[0], 'a')
                sim = self.make_sim(self.c_index_list[0], self.index_list[0])
                sim_list.append(sim)
                save_word = str(self.c_index_list[0]) + '/' + str(sim)
                f.write(save_word)
                f.write('\n')
                f.close()
                del self.c_index_list[0]
                
                if len(self.c_index_list) == 0:
                    self.c_index_list = deepcopy(
                        self.b_index_list)  # b_index_list는 갱신을 위한 리스트, c_index_list는 분석을 위한 리스트
                    del self.index_list[0]  # 파일 넘어가는 용도
            else:
                f = open(target + '/%s.txt' % self.index_list[0], 'a')
                sim = self.make_sim(self.sub_index_list[0], self.index_list[0])
                sim_list.append(sim)
                save_word = str(self.sub_index_list[0]) + '/' + str(sim)
                f.write(save_word)
                f.write('\n')
                f.close()
                del self.sub_index_list[0]
                
                if len(self.sub_index_list) == 0:
                    self.sub_index_list = deepcopy(self.add_eng)  # b_index_list는 갱신을 위한 리스트, c_index_list는 분석을 위한 리스트
                    del self.index_list[0]  # 파일 넘어가는 용도
        elif self.config == False:
            self.mousepressEvent = self.mouseMoveEvent
            sim_list = []
            self.QL.setText(
                '%d/%d analyzing.....' % (len(self.b_index_list) - len(self.index_list), len(self.b_index_list)))
            if len(self.index_list) == 0:
                self.QL.setText('Finished!')
                self.timer.stop()
                self.close()
                return
            self.step = 100 - round((100 * len(self.index_list)) / len(self.b_index_list), 0)
            self.pbar.setValue(self.step)
            f = open(target + '/%s.txt' % self.index_list[0], 'a', encoding='utf-8')
            sim = self.make_sim(self.c_index_list[0], self.index_list[0])
            sim_list.append(sim)
            save_word = str(self.c_index_list[0]) + '/' + str(sim)
            f.write(save_word)
            f.write('\n')
            f.close()
            del self.c_index_list[0]
            
            if len(self.c_index_list) == 0:
                self.c_index_list = deepcopy(self.b_index_list)
                del self.index_list[0]
        else:
            self.close()
    
    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(0, self)


class mode_3(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def make_sim_list(self, word):
        f = open(target + '/%s.txt' % word, 'r', encoding='utf-8')
        list_1 = f.readlines()
        sim_list = []
        max_sim_list = []
        for i in list_1:
            i = i.strip('\n')
            i = i.split('/')
            sim_list.append(i[1])
            max_sim_list.append(i[1])
        return sim_list, max_sim_list
    
    def find_word(self, sim_list, max_sim_list, index_list, word):
        n_w_list = []
        w_list = [word]
        copy_w_list = copy(index_list)
        while len(w_list) <= 4 and len(sim_list) != 0:
            num = sim_list.index(max_sim_list[0])  # 최대 유삿값의 위치를 찾는다.
            n_word = copy_w_list[num]  # 최대 유삿값을 가진 단어를 찾는다.
            del max_sim_list[0]  # 지운다
            del sim_list[num]
            del copy_w_list[num]
            if n_word != word:
                w_list.append(n_word)
            w_list = list(set(w_list))  # 이 과정에서 섞인다.
        for i in w_list:
            n = w_list.index(i) + 1
            c = str(n) + '. ' + str(i)
            n_w_list.append(c)
        
        return w_list, n_w_list
    
    def re_make(self):
        word = self.rand_list[0]
        word_index = self.index_list.index(word)
        self.sim_list, self.max_sim_list = self.make_sim_list(word)
        self.max_sim_list.sort(reverse=True)
        self.word.setText(self.kor_list[word_index])
        self.w_list, self.n_w_list = self.find_word(self.sim_list, self.max_sim_list, self.index_list, word)
        self.c_answer = str(int(self.w_list.index(word)) + 1)
        self.a1.setText(self.n_w_list[0])
        self.a2.setText(self.n_w_list[1])
        self.a3.setText(self.n_w_list[2])
        self.a4.setText(self.n_w_list[3])
        self.a5.setText(self.n_w_list[4])
    
    def cl(self):
        if self.a1.isChecked():
            if self.c_answer == '1':
                del self.rand_list[0]
                self.re_make()
                if self.status.text != '':
                    self.status.setText('')
            else:
                k = open('worng_answer_K2E.txt', 'a')
                k.write(self.word.text())
                k.write(" / yoer answer is : ")
                k.write(self.w_list[0])
                k.write('\n')
                k.close()
                self.status.setText('%s(x) %s(o)' % (self.w_list[0], self.w_list[int(self.c_answer) - 1]))
                del self.rand_list[0]
                self.re_make()
        
        if self.a2.isChecked():
            if self.c_answer == '2':
                del self.rand_list[0]
                self.re_make()
                if self.status.text != '':
                    self.status.setText('')
            else:
                k = open('worng_answer_K2E.txt', 'a')
                k.write(self.word.text())
                k.write(" / yoer answer is : ")
                k.write(self.w_list[1])
                k.write('\n')
                k.close()
                self.status.setText('%s(x) %s(o)' % (self.w_list[1], self.w_list[int(self.c_answer) - 1]))
                del self.rand_list[0]
                self.re_make()
        
        if self.a3.isChecked():
            if self.c_answer == '3':
                del self.rand_list[0]
                self.re_make()
                if self.status.text != '':
                    self.status.setText('')
            else:
                k = open('worng_answer_K2E.txt', 'a')
                k.write(self.word.text())
                k.write(" / yoer answer is : ")
                k.write(self.w_list[2])
                k.write('\n')
                k.close()
                self.status.setText('%s(x) %s(o)' % (self.w_list[2], self.w_list[int(self.c_answer) - 1]))
                del self.rand_list[0]
                self.re_make()
        
        if self.a4.isChecked():
            if self.c_answer == '4':
                del self.rand_list[0]
                self.re_make()
                if self.status.text != '':
                    self.status.setText('')
            else:
                k = open('worng_answer_K2E.txt', 'a')
                k.write(self.word.text())
                k.write(" / yoer answer is : ")
                k.write(self.w_list[3])
                k.write('\n')
                k.close()
                self.status.setText('%s(x) %s(o)' % (self.w_list[3], self.w_list[int(self.c_answer) - 1]))
                del self.rand_list[0]
                self.re_make()
        
        if self.a5.isChecked():
            if self.c_answer == '5':
                del self.rand_list[0]
                self.re_make()
                if self.status.text != '':
                    self.status.setText('')
            else:
                k = open('worng_answer_K2E.txt', 'a')
                k.write(self.word.text())
                k.write(" / yoer answer is : ")
                k.write(self.w_list[4])
                k.write('\n')
                k.close()
                self.status.setText('%s(x) %s(o)' % (self.w_list[4], self.w_list[int(self.c_answer) - 1]))
                del self.rand_list[0]
                self.re_make()
    
    def initUI(self):
        try:
            engs = open(target + '/s_all_eng.txt', 'r')
            
            all_engs = open(target + '/all_eng.txt', 'r')
            all_kors = open(target + '/all_kor.txt', 'r', encoding='utf-8')
            
            self.index_list = [i.rstrip('\n') for i in all_engs.readlines()]
            self.rand_list = [i.rstrip('\n') for i in engs.readlines()]
            self.kor_list = [i.rstrip('\n') for i in all_kors.readlines()]
            
            shuffle(self.rand_list)
            all_kors.close()
            all_engs.close()
            engs.close()
            word = self.rand_list[0]
            word_index = self.index_list.index(word)
            self.word = QLabel('%s' % self.kor_list[word_index])
            self.sim_list, self.max_sim_list = self.make_sim_list(word)
            self.max_sim_list.sort(reverse=True)
            self.w_list, self.n_w_list = self.find_word(self.sim_list, self.max_sim_list, self.index_list, word)
            self.c_answer = str(int(self.w_list.index(word)) + 1)
            self.a1 = QRadioButton(self.n_w_list[0])
            self.a1.clicked.connect(self.cl)
            self.a2 = QRadioButton(self.n_w_list[1])
            self.a2.clicked.connect(self.cl)
            self.a3 = QRadioButton(self.n_w_list[2])
            self.a3.clicked.connect(self.cl)
            self.a4 = QRadioButton(self.n_w_list[3])
            self.a4.clicked.connect(self.cl)
            self.a5 = QRadioButton(self.n_w_list[4])
            self.a5.clicked.connect(self.cl)
            self.status = QLabel()
            vbox = QVBoxLayout()
            vbox.addStretch(1)
            vbox.addWidget(self.word)
            vbox.addStretch(1)
            vbox.addWidget(self.a1)
            vbox.addWidget(self.a2)
            vbox.addWidget(self.a3)
            vbox.addWidget(self.a4)
            vbox.addWidget(self.a5)
            vbox.addStretch(1)
            
            hbox = QHBoxLayout()
            hbox.addLayout(vbox)
            hbox.addWidget(self.status)
            self.setLayout(hbox)
            
            self.setGeometry(300, 300, 500, 500)
            self.setWindowTitle('mode3 : K2E학습')
            self.show()
        except:
            self.task = QLabel('구간설정을 진행해주세요.')
            vbox = QVBoxLayout(self)
            vbox.addWidget(self.task)
            self.setLayout(vbox)
            self.show()


class mode_5(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def pass_def(self):
        if self.mean.text() == '' and self.word.text() == '':
            self.word.setText(self.check_list[0])
            self.re_btn.setEnabled(False)
        elif self.mean.text() == 'mean, click pass to start':
            self.word.setText(self.check_list[0])
            self.mean.setText('')
            self.re_btn.setEnabled(False)
        elif self.word.text() == self.check_list[0]:
            if self.mean.text() == '':
                word_num = self.index_list.index(self.check_list[0])
                self.mean.setText(self.kor_list[word_num])
                self.re_btn.setEnabled(True)
            else:
                print(self.rand_list)
                print(self.check_list)
                del self.check_list[0]
                if len(self.check_list) == 0:
                    if len(self.rand_list) >= 10:
                        r_rand_list = deepcopy(self.rand_list[:10])
                        del self.rand_list[:10]
                    else:
                        r_rand_list = deepcopy(self.rand_list)
                        self.rand_list = []
                    self.check_list = deepcopy(r_rand_list)
                if len(self.check_list) != 0:
                    self.word.setText(self.check_list[0])
                    self.re_btn.setEnabled(False)
                else:
                    self.word.setText('ended!')
                    self.close()
                self.mean.setText('')
    
    def re_def(self):
        self.check_list.append(self.check_list[0])
        del self.check_list[0]
        self.word.setText(self.check_list[0])
        self.mean.setText('')
        self.re_btn.setEnabled(False)
    
    def initUI(self):
        
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        
        engs = open(target + '/s_all_eng.txt', 'r')
        kors = open(target + '/s_all_kor.txt', 'r', encoding='utf-8')
        
        self.index_list = []
        self.kor_list = []
        
        b_index_list = engs.readlines()
        b_kor_list = kors.readlines()
        
        for i in b_index_list: self.index_list.append(i.rstrip('\n'))
        for i in b_kor_list: self.kor_list.append(i.rstrip('\n'))
        
        self.rand_list = deepcopy(self.index_list)
        shuffle(self.rand_list)
        
        self.check_list = []
        if len(self.rand_list) >= 10:
            self.check_list = deepcopy(self.rand_list[:10])
            del self.rand_list[:10]
            print('mode 1')
        elif len(self.rand_list) < 10:
            self.check_list = deepcopy(self.rand_list[:len(self.rand_list)])
            del self.rand_list[:len(self.rand_list)]
            print('mode 2')
        
        self.word = QLabel('Word, click pass to start')
        font2 = self.word.font()
        font2.setFamily('신명조')
        font2.setPointSize(20)
        self.word.setFont(font2)
        self.word.setStyleSheet("color: rgb(255, 255, 255);")
        self.mean = QLabel('mean, click pass to start')
        font2 = self.mean.font()
        font2.setFamily('신명조')
        font2.setPointSize(20)
        self.mean.setFont(font2)
        self.mean.setStyleSheet("color: rgb(255, 255, 255);")
        self.pass_btn = QPushButton('pass')
        self.re_btn = QPushButton('retry')
        self.re_btn.setEnabled(False)
        
        self.setGeometry(300, 300, 500, 500)
        self.re_btn.clicked.connect(self.re_def)
        self.pass_btn.clicked.connect(self.pass_def)
        hbox = QHBoxLayout()
        hbox.addWidget(self.re_btn)
        hbox.addWidget(self.pass_btn)
        
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.word)
        vbox.addWidget(self.mean)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        
        self.setLayout(vbox)
        self.setWindowTitle('mode5 : 단어암기')
        self.show()


class mode_6(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def fin(self):
        self.st = int(self.st_rt.text()) - 1
        self.ed = int(self.ed_rt.text())
        con = True
        self.close()
    
    def initUI(self):
        s_engs = open(target + '/all_eng.txt', 'r')
        lines = [i for i in s_engs.readlines()]
        s_engs.close()
        
        notice = QLabel('max_number is %d' % len(lines))
        start = QLabel('시작구간 : ')
        end = QLabel('종료구간 : ')
        
        self.st_rt = QLineEdit()
        self.ed_rt = QLineEdit()
        
        ed_btn = QPushButton('finished!')
        ed_btn.clicked.connect(self.fin)
        vbox_1 = QVBoxLayout()
        vbox_1.addWidget(start)
        vbox_1.addWidget(end)
        vbox_1.addStretch(1)
        
        vbox_2 = QVBoxLayout()
        vbox_2.addWidget(self.st_rt)
        vbox_2.addWidget(self.ed_rt)
        vbox_2.addStretch(1)
        
        hbox = QHBoxLayout()
        hbox.addLayout(vbox_1)
        hbox.addLayout(vbox_2)
        
        vbox_3 = QVBoxLayout()
        vbox_3.addStretch(1)
        vbox_3.addWidget(notice)
        vbox_3.addLayout(hbox)
        vbox_3.addStretch(1)
        vbox_3.addWidget(ed_btn)
        
        self.setLayout(vbox_3)
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('mode6 : 구간설정')
        self.show()


class mode_7(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def m_tesk(self):
        self.box.append(self.inputs.text())
        press('hangul')
        if self.tesk.text() == 'input eng : ':
            self.tesk.setText('input kor : ')
            self.E_word = self.inputs.text()
        elif self.tesk.text() == 'input kor : ':
            self.tesk.setText('input eng : ')
            self.K_word = self.inputs.text()
            f = open('new.txt', 'a', encoding='utf-8')
            f.write('%s/%s\n' % (self.E_word, self.K_word))
            f.close()
        self.inputs.clear()
    
    def initUI(self):
        try:
            self.tesk = QLabel('input eng : ')
            self.inputs = QLineEdit()
            self.inputs.returnPressed.connect(self.m_tesk)
            self.box = QTextBrowser()
            
            hbox = QHBoxLayout()
            hbox.addWidget(self.tesk)
            hbox.addWidget(self.inputs)
            
            vbox = QVBoxLayout()
            vbox.addLayout(hbox)
            vbox.addWidget(self.box)
            
            self.setLayout(vbox)
            self.setWindowTitle('mode7 : 빠른입력')
            self.setGeometry(300, 300, 500, 500)
            self.show()
        except:
            self.task = QLabel('구간설정을 진행해주세요.')
            vbox = QVBoxLayout(self)
            vbox.addWidget(self.task)
            self.setLayout(vbox)
            self.show()


class mode_8(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    
    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        try:
            rmtree(target + '/sim')
        except:
            pass
        if not os.path.isdir(target + '/sim'):
            os.mkdir(target + '/sim')
        f = open('temp.txt', 'r')
        self.sim = f.readline()
        self.tesk = QLabel('분석이 진행중입니다...')
        vbox = QVBoxLayout()
        vbox.addWidget(self.tesk)
        self.n_dict = {}
        self.timer = QBasicTimer()
        self.doAction()
        self.step = 0
        self.all_engs = open(target + '/all_eng.txt', 'r')
        self.lines = [i.rstrip('\n') for i in self.all_engs.readlines()]
        self.dlines = deepcopy(self.lines)
        self.all_engs.close()
        self.setLayout(vbox)
        self.show()
    
    def timerEvent(self, e):
        
        n_lines = [j.rstrip('\n') for j in open(target + '/%s.txt' % self.lines[0], 'r').readlines()]
        for k in n_lines:
            s_list = k.split('/')
            if float(s_list[1]) >= float(self.sim):
                if self.lines[0] in self.n_dict:
                    p_word = self.n_dict[self.lines[0]]
                    self.n_dict[self.lines[0]] = p_word + ['%s/%s' % (s_list[0], s_list[1])]
                else:
                    self.n_dict[self.lines[0]] = ['%s/%s' % (s_list[0], s_list[1])]
        f = open(target + '/sim/%s.txt' % self.lines[0], 'a')
        for k in self.n_dict[self.lines[0]]:
            f.write('%s\n' % k)
        f.close()
        del self.lines[0]
        if len(self.lines) == 0:
            k = open('sim_result.txt', 'w')
            for i in self.dlines:
                g = open(target + '/sim/%s.txt' % i, 'r')
                save_list = []
                for j in g.readlines():
                    j = j.rstrip('\n')
                    j_l = j.split('/')
                    if int(float(j_l[1])) != 1:
                        save_list.append(j_l[0])
                if len(save_list) != 0:
                    k.write('%s\n%s\n\n' % (i, ', '.join(save_list)))
            self.timer.stop()
            self.close()
            return
    
    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(0, self)


class main_mode_8(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        f = open(target + '/new.txt', 'r')
        self.main_dict = {}
        lines = [i.rstrip('\n') for i in f.readlines()]
        f.close()
        for i in lines:
            i.split('/')
            self.main_dict[i[0]] = i[0]
        k = open(target + '/s_all_eng.txt', 'r')
        lines = [i.rstrip('\n') for i in k.readlines()]
        self.main_word = QLabel('')


class sub_mode_8(QDialog):
    
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()
    
    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()
    
    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.status = QLabel('목표 유사도를 입력하세요.')
        self.le = QLineEdit()
        self.le.returnPressed.connect(self.cll)
        vbox = QVBoxLayout()
        vbox.addWidget(self.status)
        vbox.addWidget(self.le)
        
        self.setLayout(vbox)
    
    def cll(self):
        self.sim = self.le.text()
        f = open('temp.txt', 'w')
        f.write(self.sim)
        f.close()
        self.close()
        es = mode_8()
        es.exec_()


try:
    app = QApplication(argv)
    ex = MainApp()
    exit(app.exec_())
except:
    input()