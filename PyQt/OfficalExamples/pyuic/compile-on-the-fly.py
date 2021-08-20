#!/usr/bin/env python

# 以文件形式加载ui界面

import sys

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUiType


app = QApplication(sys.argv)
form_class, base_class = loadUiType('PyQt\OfficalExamples\pyuic\demo.ui')

class DemoImpl(QDialog, form_class):
    def __init__(self, *args):
        super(DemoImpl, self).__init__(*args)

        self.setupUi(self)
    
    @pyqtSlot()
    def on_button1_clicked(self):
        for s in "This is a demo".split(" "):
            self.list.addItem(s)


form = DemoImpl()
form.show()
sys.exit(app.exec_())
