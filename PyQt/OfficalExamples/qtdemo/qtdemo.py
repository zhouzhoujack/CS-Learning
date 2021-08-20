#!/usr/bin/env python

from PyQt5.QtCore import QEventLoop, QTime
from PyQt5.QtWidgets import QApplication, QMessageBox

from colors import Colors
from mainwindow import MainWindow
from menumanager import MenuManager


def artisticSleep(sleepTime):
    time = QTime()
    time.restart()
    while time.elapsed() < sleepTime:
        QApplication.processEvents(QEventLoop.AllEvents, 50)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    Colors.parseArgs(sys.argv)

    if sys.platform == 'win32':
        QMessageBox.information(None, "Documentation Warning",
                "If you are using the GPL version of PyQt from the binary "
                "installer then you will probably see warning messages about "
                "missing documentation.  This is because the installer does "
                "not include a copy of the Qt documentation as it is so "
                "large.")

    mainWindow = MainWindow()
    MenuManager.instance().init(mainWindow)
    mainWindow.setFocus()

    if Colors.fullscreen:
        mainWindow.showFullScreen()
    else:
        mainWindow.enableMask(True)
        mainWindow.show()

    artisticSleep(500)
    mainWindow.start()

    sys.exit(app.exec_())
