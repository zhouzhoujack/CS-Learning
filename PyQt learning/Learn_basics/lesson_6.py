# -*-coding:utf-8-*-
# 课程来源：https://www.cnblogs.com/archisama/p/5465104.html

import sys
from PyQt5.QtWidgets import QWidget, QCheckBox, QApplication, QFrame, QPushButton, QLabel, QSlider, QProgressBar, QCalendarWidget
from PyQt5.QtGui import QColor, QPixmap
from PyQt5.QtCore import Qt, QBasicTimer, QDate


class Example(QWidget):

    def __init__(self):
        super().__init__()

    def initUI(self):

        cb = QCheckBox('Show title', self)
        cb.move(20, 20)
        cb.toggle()
        cb.stateChanged.connect(self.changeTitle)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QCheckBox')
        self.show()

    def initUI1(self):
        self.col = QColor(0, 0, 0)

        redb = QPushButton('Red', self)
        redb.setCheckable(True)
        redb.move(10, 10)

        redb.clicked[bool].connect(self.setColor)

        redb = QPushButton('Green', self)
        redb.setCheckable(True)
        redb.move(10, 60)

        redb.clicked[bool].connect(self.setColor)

        blueb = QPushButton('Blue', self)
        blueb.setCheckable(True)
        blueb.move(10, 110)

        blueb.clicked[bool].connect(self.setColor)

        self.square = QFrame(self)
        self.square.setGeometry(150, 20, 100, 100)
        self.square.setStyleSheet("QWidget { background-color: %s }" %self.col.name())

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('Toggle button')
        self.show()

    def initUI2(self):
        sld = QSlider(Qt.Horizontal, self)
        sld.setFocusPolicy(Qt.NoFocus)
        sld.setGeometry(30, 40, 100, 30)
        sld.valueChanged[int].connect(self.changeValue)

        self.label = QLabel(self)
        self.label.setPixmap(QPixmap('./icons/mute.png'))
        self.label.setGeometry(160, 40, 80, 30)

        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QSlider')
        self.show()

    def initUI3(self):
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)
        self.btn = QPushButton('Start', self)
        self.btn.move(40, 80)
        self.btn.clicked.connect(self.doAction)
        self.timer = QBasicTimer()
        self.step = 0
        self.setGeometry(300, 300, 280, 170)
        self.setWindowTitle('QProgressBar')
        self.show()

    def initUI4(self):

        cal = QCalendarWidget(self)
        cal.setGridVisible(True)
        cal.move(20, 20)
        cal.clicked[QDate].connect(self.showDate)

        self.lbl = QLabel(self)
        date = cal.selectedDate()
        self.lbl.setText(date.toString())
        self.lbl.move(130, 260)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Calendar')
        self.show()

    def showDate(self, date):
        self.lbl.setText(date.toString())

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.btn.setText('Finished')
            return
        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')

    def changeValue(self, value):
        if value == 0:
            self.label.setPixmap(QPixmap('./icons/mute.png'))
        elif value > 0 and value <= 30:
            self.label.setPixmap(QPixmap('./icons/feiji.png'))
        elif value > 30 and value < 80:
            self.label.setPixmap(QPixmap('./icons/mute.png'))
        else:
            self.label.setPixmap(QPixmap('./icons/volume.png'))

    def setColor(self, pressed):
        source = self.sender()
        if pressed:
            val = 255
        else:
            val = 0
        if source.text() == "Red":
            self.col.setRed(val)
        elif source.text() == "Green":
            self.col.setGreen(val)
        else:
            self.col.setBlue(val)
        self.square.setStyleSheet("QFrame { background-color: %s }" %self.col.name())

    def changeTitle(self, state):
        if state == Qt.Checked:
            self.setWindowTitle('QCheckBox')
        else:
            self.setWindowTitle('')

def calendar_widget():
    """
    日历选择
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI4()
    sys.exit(app.exec_())

def process_bar():
    """
    进度条
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI3()
    sys.exit(app.exec_())

def slider_widget():
    """
    滑块条
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI2()
    sys.exit(app.exec_())

def checkBox_widget():
    """
    复选框,切换窗口标题
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI()
    sys.exit(app.exec_())

def toggle_button():
    """
    按钮组合使用和切换
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI1()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # checkBox_widget()
    # toggle_button()
    # slider_widget()
    # process_bar()
    calendar_widget()