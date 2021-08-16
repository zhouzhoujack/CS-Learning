"""
对MainWindow的控件进行事件绑定
"""
from typing import overload
from PyQt5.QtGui import QIcon
import pyautogui as pg
import time
from pynput.mouse import Listener
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMessageBox, QMainWindow
from threading import Thread

import sys,os 
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path) 
from Forms import Ui_MyMainWindow

clickTimes = 0  # 记录点击次数用于终止鼠标监听事件
pos = []        # 记录云同步时鼠标三次点击的位置
interval = 10   # 设置云同步间隔时间,默认为10
isClicked = False   # 记录button是否被点击过
isCloudSycn = True  # 控制后台的自动同步

def performOperations(pos1, pos2, pos3):
    # pos1: "云同步"按钮的位置
    # pos2: "手动同步"按钮的位置
    # pos3: 同步完成后"确认"按钮的位置
    pg.hotkey('win', 'd')  # 返回桌面
    pg.moveTo(pos1[0], pos1[1], duration=0.0)
    pg.doubleClick()
    time.sleep(0.01)
    pg.moveTo(pos2[0], pos2[1], duration=0.0)
    pg.doubleClick()
    pg.moveTo(pos3[0], pos3[1], duration=0.1)
    time.sleep(0.4)
    pg.doubleClick()
    pg.hotkey('win', 'd')   # 返回桌面

def thread_func():
    # 开一个线程让自动云同步后台运行
    while(True):
        time.sleep(interval)
        if not isCloudSycn:
            break
        performOperations(pos[0], pos[1], pos[2])
        print("Done!")

def pushButtonClickedEvent(ui, win):
    global isClicked
    isClicked = 1-isClicked

    autoSyncThread = Thread(target=thread_func)     # 云同步线程

    ui.lineEdit.setEnabled(False)
    ui.pushButton.setEnabled(False)
    ui.pushButton.setText("执行中")
    ui.pushButton_3.setEnabled(False)
    win.setWindowIcon(QIcon(r"C:\\Users\\0317\\Desktop\\CS-Learning\\PyQt\\Projects\\AutoCloudSync\\img\\icon_on.png"))

    global interval
    interval = int(ui.lineEdit.text())
    print("开始自动云同步...")
    autoSyncThread.start()

def pushButton_2ClickedEvent(ui, win):
    # 关闭云同步
    global isCloudSycn
    isCloudSycn = False             # 关闭自动云同步的线程
    ui.lineEdit.setEnabled(True)
    ui.pushButton.setEnabled(True)
    ui.pushButton_3.setEnabled(True)
    win.setWindowIcon(QIcon(r"C:\\Users\\0317\\Desktop\\CS-Learning\\PyQt\\Projects\\AutoCloudSync\\img\\icon_off.png"))
    ui.pushButton.setText("开始执行")
    print("结束执行")

def pushButton_3ClickedEvent(ui):
    # 初始化云同步步骤的按钮的坐标位置
    def on_click(x, y, button, pressed):
        global clickTimes
        if pressed:
            print('Pressed at X: {} Y: {}'.format(x, y))
            pos.append([x, y])
            clickTimes += 1

        if clickTimes == 3:
            return False

    # 连接事件以及释放
    # 这里的Listener是监听鼠标点击事件来获取桌面坐标
    """
    TODO (多线程执行完未完全退出)
    """
    with Listener(on_click=on_click) as listener:
        listener.join()

    global clickTimes
    clickTimes = 0
    print("自动云同步设置完成!")

    ui.pushButton.setEnabled(True)
    ui.pushButton_2.setEnabled(True)

def checkBoxStateChangedEvent(ui):
    # TODO 开机自动云同步一次，并隐藏在后台执行
    print(ui.checkBox.isChecked())


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 界面的UI初始化,这部分代码由QT编译器自动生成，不用动
        ui = Ui_MyMainWindow.Ui_MainWindow()
        ui.setupUi(self)

        # 界面的一些设置
        self.windowSetting()

        # 控件的事件绑定
        self.widgetsSetting(ui)

    def windowSetting(self):
        self.setFixedSize(self.width(), self.height())

    def widgetsSetting(self, ui):
        self.setWindowIcon(QIcon(r"C:\\Users\\0317\\Desktop\\CS-Learning\\PyQt\\Projects\\AutoCloudSync\\img\\icon_off.png"))

        ui.pushButton.clicked.connect(lambda: pushButtonClickedEvent(ui, self))
        ui.pushButton_2.clicked.connect(lambda: pushButton_2ClickedEvent(ui, self))
        ui.pushButton.setEnabled(False)
        ui.pushButton_2.setEnabled(False)
        ui.pushButton_3.clicked.connect(lambda: pushButton_3ClickedEvent(ui))
        ui.lineEdit.setText(str(interval))
        ui.checkBox.setChecked(True)
        ui.checkBox.stateChanged.connect(lambda:checkBoxStateChangedEvent(ui))