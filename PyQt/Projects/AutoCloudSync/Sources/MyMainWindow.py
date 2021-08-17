"""
对MainWindow的主界面进行详细设置
"""
from typing import overload
from PyQt5.QtGui import QIcon
import pyautogui as pg
import time
from pynput.mouse import Listener
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QSettings, QFileInfo, QCoreApplication, QTimer
from PyQt5.QtWidgets import qApp, QMessageBox, QMainWindow, QSystemTrayIcon, QAction, QMenu

import sys,os 
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path) 
from Forms import Ui_MyMainWindow
from Resources import res_rc

_MILISECONDS_TO_HOUR = 1000*3600     # 毫秒转为小时 3600*1000

clickTimes = 0      # 记录点击次数用于终止鼠标监听事件
pos = []            # 记录云同步时鼠标三次点击的位置
interval = 3        # 设置云同步间隔时间,默认为3个小时

def performOperations(pos1, pos2, pos3):
    # pos1: "云同步"按钮的位置
    # pos2: "手动同步"按钮的位置
    # pos3: 同步完成后"确认"按钮的位置

    x, y = pg.position()

    pg.hotkey('win', 'd') 
    pg.moveTo(pos1[0], pos1[1], duration=0.0)
    pg.doubleClick()
    time.sleep(0.01)
    pg.moveTo(pos2[0], pos2[1], duration=0.0)
    pg.doubleClick()
    pg.moveTo(pos3[0], pos3[1], duration=0.1)
    time.sleep(0.5)
    pg.doubleClick()
    pg.hotkey('win', 'd')  

    pg.moveTo(x, y)

def timeoutEvent():
    # global pos
    performOperations(pos[0], pos[1], pos[2])
    print("Done!")

def pushButtonClickedEvent(win):
    ui = win.ui
    
    ui.lineEdit.setEnabled(False)
    ui.pushButton.setEnabled(False)
    ui.pushButton.setText("运行中..")
    ui.pushButton_3.setEnabled(False)
    win.setWindowIcon(QIcon(r":/img/icon_on.png"))

    global interval
    interval = int(ui.lineEdit.text())

    performOperations(pos[0], pos[1], pos[2])
    win.timer_.start(int(interval*_MILISECONDS_TO_HOUR))

    print("开始自动云同步...")

    # 将程序显示到托盘
    # QTimer.singleShot(1000000, lambda : win.setWindowState(QtCore.Qt.WindowMinimized))  

def pushButton_2ClickedEvent(win):
    ui = win.ui
    # 关闭云同步
    win.timer_.stop()               # 停止云同步运行

    ui.lineEdit.setEnabled(True)
    ui.pushButton.setEnabled(True)
    ui.pushButton_3.setEnabled(True)
    win.setWindowIcon(QIcon(r":/img/icon_off.png"))
    ui.pushButton.setText("开始执行")

    print("结束执行")

def pushButton_3ClickedEvent(win):
    ui = win.ui
    # 初始化云同步步骤的按钮的坐标位置
    def on_click(x, y, button, pressed):
        global clickTimes
        if pressed:
            print('Pressed at X: {} Y: {}'.format(x, y))
            pos.append([x, y])
            clickTimes += 1

        if clickTimes == 3:
            return False

    global pos
    pos = []

    QMessageBox.information(win, "提示", "请手动执行一次桌面日历的云同步!") 
    win.setVisible(False)

    # 连接事件以及释放
    # 这里的Listener是监听鼠标点击事件来获取桌面坐标
    """
    TODO (多线程执行完未完全退出)
    """
    with Listener(on_click=on_click) as listener:
        listener.join()

    global clickTimes
    clickTimes = 0

    # 将button的坐标保存到默认设置中，以便下次重启使用
    settings = QSettings("HXZZ", "AutoCloudSync")
    settings.beginGroup("Button_Positions")
    settings.setValue("pos", pos)
    settings.endGroup()

    win.setVisible(True)
    
    QMessageBox.information(win, "提示", "自动云同步设置完成!")
    # QTimer.singleShot(1000, )
  
    ui.pushButton.setEnabled(True)
    ui.pushButton_2.setEnabled(True)

def checkBoxStateChangedEvent(ui):
    # TODO 开机自动云同步一次，并隐藏在后台执行
    appPath = QCoreApplication.applicationDirPath() 
    print(appPath)

    changedFlag = ui.checkBox.isChecked()
    settings = QSettings("HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run")
    
    # 以程序名称作为注册表中的键
    # 根据键获取对应的值（程序路径）
    fInfo = QFileInfo()
    key = fInfo.baseName()
    # value = settings.value(key).toString()
    value = ""

    settings.setValue(key, value)

    if(changedFlag):
        value = QDir.toNativeSeparators(appPath)
        settings.setValue(key, value)
    
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.timer_ = QTimer(self)

        # 系统托盘
        self.trayIcon_ = QSystemTrayIcon()      
        self.trayIcon_.activated.connect(self.trayClick)

        # 界面的UI初始化,这部分代码由QT编译器自动生成，不用动
        self.ui = Ui_MyMainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        # 界面的一些设置
        self.windowSetting()

        # 控件的事件绑定
        self.widgetsSetting()

        # 加载保存的按钮坐标
        self.loadSettings()

    def windowSetting(self):
        self.setFixedSize(self.width(), self.height())

    def widgetsSetting(self):
        self.timer_.timeout.connect(lambda: timeoutEvent())

        self.setWindowIcon(QIcon(r":/img/icon_off.png"))

        self.ui.pushButton.clicked.connect(lambda: pushButtonClickedEvent(self))
        self.ui.pushButton_2.clicked.connect(lambda: pushButton_2ClickedEvent(self))
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.clicked.connect(lambda: pushButton_3ClickedEvent(self))
        self.ui.lineEdit.setText(str(interval))
        self.ui.checkBox.setChecked(True)
        self.ui.checkBox.stateChanged.connect(lambda:checkBoxStateChangedEvent(self))

    def loadSettings(self):
        settings = QSettings("HXZZ", "AutoCloudSync")
        settings.beginGroup("Button_Positions")

        global pos
        pos = settings.value("pos")
        print(pos)

        if pos is not None:
            self.ui.pushButton.setEnabled(True)
            self.ui.pushButton_2.setEnabled(True)

    def closeEvent(self, QCloseEvent):    
        """
        重写窗口关闭事件
        """
        print("closeEvent")
        # self.trayIcon_.hide()

    def trayClick(self, reason):
        """
        托盘点击响应事件
        """
        print("trayClick")
        if reason == QSystemTrayIcon.Trigger:
            self.showNormal()
            self.activateWindow()

    def changeEvent(self, event):
        """
        重写窗口状态改变函数
        """
        def _showTrayIconMesg():
            self.trayIcon_.setToolTip("桌面日历自动云同步")
            self.trayIcon_.showMessage("桌面日历自动云同步","已最小化至托盘")
        
        if event.type() == QtCore.QEvent.WindowStateChange:
            if self.windowState() & QtCore.Qt.WindowMinimized:
                event.ignore()
                print("窗口最小化")
                quitAction = QAction(u"退出", self, triggered = qApp.quit)
                menu = QMenu()
                menu.addAction(quitAction)
                self.trayIcon_.setContextMenu(menu)

                self.trayIcon_.setIcon(QIcon(r":/img/icon_off.png"))

                if not self.ui.pushButton.isEnabled():
                    self.trayIcon_.setIcon(QIcon(r":/img/icon_on.png"))

                QTimer.singleShot(600, lambda : _showTrayIconMesg())       
                
                self.trayIcon_.show()
                self.hide()
                
