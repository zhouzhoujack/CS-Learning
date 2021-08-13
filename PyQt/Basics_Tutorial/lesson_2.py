# -*- coding:utf-8 -*-
# 课程来自：https://www.cnblogs.com/archisama/p/5450834.html#4118008
# 主要讲一些控件
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, qApp, QTextEdit
from PyQt5.QtGui import QIcon

class Example(QMainWindow):
    def __init__(self):
        super().__init__()

    def initUI(self):
        self.statusBar().showMessage('Ready')
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Statusbar')
        self.show()

    def initUI1(self):
        exitAction = QAction(QIcon('./icons/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')    # 快捷键
        exitAction.setStatusTip('Exit application')     # 状态栏提示
        exitAction.triggered.connect(qApp.quit)
        menubar = self.menuBar()        # 创建菜单栏
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)      # 选中特定的动作，一个触发信号会被发送。信号连接到QApplication组件的quit()方法

        self.statusBar()
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Menubar')
        self.show()

    def initUI2(self):
        exitAction = QAction(QIcon('./icons/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(qApp.quit)
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Toolbar')
        self.show()

    def inintUI3(self):
        textEdit = QTextEdit()      # 文本框
        self.setCentralWidget(textEdit)     # 设置为中心组件，占据所有剩下空间

        exitAction = QAction(QIcon('./icons/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.show()

def show_all_bars():
    """
    几种工具一起使用
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.inintUI3()
    sys.exit(app.exec_())

def show_tool_bar():
    """
    展示工具栏
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI2()
    sys.exit(app.exec_())

def show_status_bar():
    """
    显示状态栏，状态栏依赖于QMainWindow组件
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI()
    sys.exit(app.exec_())

def show_menu_bar():
    """
    显示菜单栏
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI1()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # show_status_bar()
    # show_menu_bar()
    # show_tool_bar()
    show_all_bars()