import sys,os
from PyQt5.QtWidgets import qApp, QApplication
from Sources import MyMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    print(sys.argv[0])
    print(qApp.applicationFilePath())
    print(os.path.realpath(sys.executable))

    window = MyMainWindow.MainWindow()
    window.show()

    sys.exit(app.exec_())

