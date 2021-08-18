import sys
from PyQt5.QtWidgets import QApplication
from Sources import MyMainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    print(sys.argv[0])

    window = MyMainWindow.MainWindow()
    window.show()

    sys.exit(app.exec_())

