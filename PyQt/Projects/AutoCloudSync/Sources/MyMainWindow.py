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
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QSystemTrayIcon

import sys,os 
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path) 
from Forms import Ui_MyMainWindow
from Resources import res_rc

_MILISECONDS_TO_HOUR = 1000*3600     # 毫秒转为小时 3600*1000

clickTimes = 0      # 记录点击次数用于终止鼠标监听事件
pos = []            # 记录云同步时鼠标三次点击的位置
interval = 3        # 设置云同步间隔时间,默认为3个小时
isClicked = False   # 记录button是否被点击过

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

def pushButtonClickedEvent(ui, win):
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
    # win.setWindowFlags(QtCore.Qt.SplashScreen | QtCore.Qt.FramelessWindowHint)
    win.showMinimized()
    
def pushButton_2ClickedEvent(ui, win):
    # 关闭云同步
    win.timer_.stop()               # 停止云同步运行

    ui.lineEdit.setEnabled(True)
    ui.pushButton.setEnabled(True)
    ui.pushButton_3.setEnabled(True)
    win.setWindowIcon(QIcon(r":/img/icon_off.png"))
    ui.pushButton.setText("开始执行")

    print("结束执行")

def pushButton_3ClickedEvent(ui, win):
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

        self.trayIcon_ = QSystemTrayIcon()

        # 界面的UI初始化,这部分代码由QT编译器自动生成，不用动
        ui = Ui_MyMainWindow.Ui_MainWindow()
        ui.setupUi(self)

        # 界面的一些设置
        self.windowSetting()

        # 控件的事件绑定
        self.widgetsSetting(ui)

        # 加载保存的按钮坐标
        self.loadSettings(ui)

    def windowSetting(self):
        self.setFixedSize(self.width(), self.height())

    def widgetsSetting(self, ui):
        self.timer_.timeout.connect(lambda: timeoutEvent())

        self.setWindowIcon(QIcon(r":/img/icon_off.png"))

        ui.pushButton.clicked.connect(lambda: pushButtonClickedEvent(ui, self))
        ui.pushButton_2.clicked.connect(lambda: pushButton_2ClickedEvent(ui, self))
        ui.pushButton.setEnabled(False)
        ui.pushButton_2.setEnabled(False)
        ui.pushButton_3.clicked.connect(lambda: pushButton_3ClickedEvent(ui, self))
        ui.lineEdit.setText(str(interval))
        ui.checkBox.setChecked(True)
        ui.checkBox.stateChanged.connect(lambda:checkBoxStateChangedEvent(ui))

    def loadSettings(self, ui):
        settings = QSettings("HXZZ", "AutoCloudSync")
        settings.beginGroup("Button_Positions")

        global pos
        pos = settings.value("pos")
        print(pos)

        if pos is not None:
            ui.pushButton.setEnabled(True)
            ui.pushButton_2.setEnabled(True)
