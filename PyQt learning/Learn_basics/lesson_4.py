# -*- coding:utf-8 -*-
# 课程来源：https://www.cnblogs.com/archisama/p/5454200.html
# 事件与信号
# 事件源：状态发生改变的对象。它产生了事件
# 事件对象(event)：封装了事件源中的状态变化
# 事件目标：想要被通知的对象


import sys
from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtWidgets import (QWidget, QLCDNumber, QSlider, QMainWindow, QPushButton,
    QVBoxLayout, QApplication)


class Communicate(QObject):
    closeApp = pyqtSignal()

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

    def initUI(self):
        lcd = QLCDNumber(self)
        sld = QSlider(Qt.Horizontal, self)

        vbox = QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(sld)

        self.setLayout(vbox)
        sld.valueChanged.connect(lcd.display)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Signal & slot')
        self.show()

    def initUI1(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Event handler')
        self.show()

    def initUI2(self):
        btn1 = QPushButton("Button 1", self)
        btn1.move(30, 50)

        btn2 = QPushButton("Button 2", self)
        btn2.move(150, 50)

        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Event sender')
        self.show()

    def initUI3(self):
        self.c = Communicate()
        self.c.closeApp.connect(self.close)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Emit signal')
        self.show()

    def mousePressEvent(self, event):
        """
        鼠标点击事件处理，发送closeApp信号，应用中断
        :param event:
        :return:
        """
        self.c.closeApp.emit()

    def buttonClicked(self):
        """
        发送事件
        :return:
        """
        sender = self.sender()
        self.statusBar().showMessage(sender.text() + ' was pressed')

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Escape:
            self.close()

def sign_and_slot():
    """
    信号与槽(对信号做出反应的方法)之间的例子
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI()
    sys.exit(app.exec_())

def event_processing():
    """
    键盘按键事件处理
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI1()
    sys.exit(app.exec_())

def button_clicked_event():
    """
    按钮事件响应,更换继承类为QMaInWindow
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI2()
    sys.exit(app.exec_())

def mouse_clicked_event():
    """
    自定义信号发送
    :return: 
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI3()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # sign_and_slot()
    # event_processing()
    # button_clicked_event()
    mouse_clicked_event()