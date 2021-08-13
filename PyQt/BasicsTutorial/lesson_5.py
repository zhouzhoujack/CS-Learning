# -*- coding:utf-8 -*-
# 课程来源：https://www.cnblogs.com/archisama/p/5454922.html
# 对话框

import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QFileDialog, QAction,
        QTextEdit, QMainWindow,QInputDialog, QApplication)
from PyQt5.QtGui import QIcon


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

    def initUI(self):
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)

        self.le = QLineEdit(self)
        self.le.move(130, 22)

        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()

    def initUI1(self):

        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showFileDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()

    def showFileDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        if fname[0]:
            f = open(fname[0], 'r')
            with f:
                data = f.read()
                self.textEdit.setText(data)

    def showDialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog','Enter your name:')
        if ok:
            self.le.setText(str(text))

def input_dialog():
    """
    显示对话框并读取文本框内容
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI()
    sys.exit(app.exec_())

def file_dialog():
    """
    让用户选择文件或目录的对话框,打开并读取文件内容
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI1()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # input_dialog()
    file_dialog()