# -*- coding: utf-8 -*-
# 课程来自：https://www.cnblogs.com/archisama/p/5453260.html
# 主要讲组件的布局管理
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, \
    QHBoxLayout, QVBoxLayout, QGridLayout, QLineEdit,QTextEdit


class Example(QWidget):

    def __init__(self):
        super().__init__()

    def initUI(self):
        lbl1 = QLabel('Zetcode', self)
        lbl1.move(15, 10)

        lbl2 = QLabel('tutorials', self)
        lbl2.move(35, 40)

        lbl3 = QLabel('for programmers', self)
        lbl3.move(55, 70)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Absolute')
        self.show()

    def initUI1(self):
        okButton = QPushButton("OK")
        cancelButton = QPushButton("Cancel")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 300, 150)
        self.setWindowTitle('Buttons')
        self.show()

    def initUI2(self):
        grid = QGridLayout()
        self.setLayout(grid)
        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']

        positions = [(i, j) for i in range(5) for j in range(4)]
        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)
        self.move(300, 150)
        self.setWindowTitle('Calculator')
        self.show()

    def initUI3(self):
        title = QLabel('Title')
        author = QLabel('Author')
        review = QLabel('Review')

        titleEdit = QLineEdit()
        authorEdit = QLineEdit()
        reviewEdit = QTextEdit()

        grid = QGridLayout()

        grid.setSpacing(10)     # 组件之间的间距
        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)
        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)
        grid.addWidget(review, 3, 0)
        grid.addWidget(reviewEdit, 3, 1, 5, 1)
        self.setLayout(grid)
        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('Review')
        self.show()

def window_grid_layout1():
    """
    另一种网格布局
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI3()
    sys.exit(app.exec_())


def window_grid_layout():
    """
    网格布局
    :return: 
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI2()
    sys.exit(app.exec_())

def window_absolute_position():
    """
    组件绝对定位
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI()
    sys.exit(app.exec_())

def window_relative_position():
    """
    组件相对定位,组件随布局移动不改变相对于窗口的位置
    :return:
    """
    app = QApplication(sys.argv)
    ex = Example()
    ex.initUI1()
    sys.exit(app.exec_())

if __name__ == '__main__':
    # window_absolute_position()
    # window_relative_position()
    # window_grid_layout()
    window_grid_layout1()