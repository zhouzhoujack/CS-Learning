# -*-coding:utf-8-*-
# 课程来自：https://www.cnblogs.com/archisama/p/5444032.html#4123611
# 窗口基础

import sys
from PyQt5.QtWidgets import QWidget, QToolTip, QPushButton, QApplication, QMessageBox,QDesktopWidget
from PyQt5.QtGui import QIcon,QFont
from PyQt5.QtCore import QCoreApplication

class Example(QWidget):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.setGeometry(300, 300, 300, 220)    # 融合了resize() and move()
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('./icons/feiji.png'))
        self.show()

    def initUI1(self):
        """
        显示带有button和鼠标提示的例子
        :return:
        """
        QToolTip.setFont(QFont('SansSerif', 10))    # 提示框对象，sansserif字体，10px大小
        self.setToolTip('This is a <b>QWidget</b> widget')

        btn = QPushButton('Button', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')       # 设置提示工具
        btn.resize(btn.sizeHint())  # sizeHint自动设置按钮大小
        btn.move(50, 50)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        self.show()

    def initUI2(self):
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)      # QCoreApplication类包含了主事件循环；它处理和转发所有事件
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Quit button')
        self.show()

    def initUI3(self):
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('message box')
        self.show()

    def initUI4(self):
        self.resize(250, 150)
        self.center()
        self.setWindowTitle('Center')
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        """
        重写，关闭一个QWidget(窗口)，QCloseEvent类事件将被生成
        """
        reply = QMessageBox.question(self, 'Message',"Are you sure to quit?", QMessageBox.Yes|QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

def show_window_center():
    """
    窗口居中
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI4()
    sys.exit(app.exec_())

def show_window_with_message_box():
    """
    显示窗口退出消息框
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI3()
    sys.exit(app.exec_())

def show_window_with_quit_btn():
    """
    button按钮响应退出事件
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI2()
    sys.exit(app.exec_())
    # ex.initUI2()

def show_a_window_with_button():
    """
    显示带有button和鼠标提示的窗口
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())       # 确保一个不留垃圾的退出


def show_a_window_with_icon():
    """
    显示带有图标的窗口
    """
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

def show_a_window():
    """
    显示一个窗口
    """
    app = QApplication(sys.argv)
    w = QWidget()       # 所有用户界面类的基础类
    w.resize(250, 1000)     # 调整窗口大小px
    w.move(300, 300)        # 出现在屏幕位置
    w.setWindowTitle('Simple')      # 窗口标题
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    """
    展示列子
    """
    # show_a_window_with_button()
    # show_window_with_quit_btn()
    # show_window_with_message_box()
    show_window_center()