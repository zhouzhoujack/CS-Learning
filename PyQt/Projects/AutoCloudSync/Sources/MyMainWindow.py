"""
对MainWindow的主界面进行详细设置
"""
from typing import overload
from typing_extensions import IntVar
from PyQt5.QtGui import QIcon
import pyautogui as pg
import time
from pynput.mouse import Listener
from PyQt5 import QtCore
from PyQt5.QtCore import QDir, QSettings, QFileInfo, QCoreApplication, QTimer, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import qApp, QMessageBox, QMainWindow, QSystemTrayIcon, QAction, QMenu, QToolTip, QLCDNumber

import win32api
import win32con, winreg

import sys,os 
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(path) 
from Forms import Ui_MyMainWindow
from Resources import res_rc


_SECONDS_OF_HOUR = 3600     # 1小时3600秒

clickTimes = 0      # 记录点击次数用于终止鼠标监听事件
pos = []            # 记录云同步时鼠标三次点击的位置
interval = 3        # 设置云同步间隔时间,默认为3个小时

def seconds2time(seconds):
    # 将秒转换为00:00:00格式的时间
    h = seconds // 3600
    _m = seconds - h * 3600
    m = _m // 60
    s = _m - m * 60
    h = str(h) if h >= 10 else '0' + str(h)
    m = str(m) if m >= 10 else '0' + str(m)
    s = str(s) if s >= 10 else '0' + str(s)
    return "%s:%s:%s"%(h, m, s)

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

def refreshTimerSlot(win):
    # 定时器的槽函数
    ui = win.ui
    win.duration -= 1   # 每s触发并减1

    formatTime = seconds2time(win.duration)
    ui.lcdNumber.display(formatTime)

    if win.duration == 0:
        performOperations(pos[0], pos[1], pos[2])
        win.duration = win.resetDuration(interval)

def pushButtonClickedEvent(win):
    ui = win.ui
    
    leText = ui.lineEdit.text()
    if leText == '':
        QMessageBox.warning(win, "提示", "请输入云同步间隔时间!") 
        return

    global interval
    interval = float(leText)

    if not ((interval > 0.1 and interval < 0.9 ) or (interval > 0 and interval < 10)):
        QMessageBox.warning(win, "提示", "请输入合法数据!") 
        return

    # 用户自定义执行的间隔时间(s)
    win.duration = win.resetDuration(interval)

    ui.lineEdit.setEnabled(False)
    ui.pushButton.setEnabled(False)
    ui.pushButton.setText("运行中..")
    ui.pushButton_3.setEnabled(False)
    win.setWindowIcon(QIcon(r":/img/icon_on.png"))

    performOperations(pos[0], pos[1], pos[2])
    win.timer_.start()

    print("开始自动云同步...")

def pushButton_2ClickedEvent(win):
    ui = win.ui

    # 关闭云同步
    win.timer_.stop()               # 停止云同步运行
    win.duration = win.resetDuration(interval)

    ui.lcdNumber.display("00:00:00")
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

def checkBoxClickedEvent(win):
    ui = win.ui
    changedFlag = ui.checkBox.isChecked()

    # 第一次设置自启动时需要检测是否初始化坐标了
    # 若没有，那么不允许设置自启动
    if changedFlag and len(pos) != 3:    
        QMessageBox.warning(win, "警告", "需要进行初始化操作!") 
        ui.checkBox.setChecked(False)
        return

    if changedFlag:
    # TODO 开机自动云同步一次，并隐藏在后台执行
        AutoRun(switch='open', key_name='AutoCloudSync')
    else :
        AutoRun(switch='close', key_name='AutoCloudSync')

def checkKey(key_name='AutoCloudSync',
            reg_root=win32con.HKEY_CURRENT_USER,  # 根节点
            reg_path=r"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run",  # 键的路径
            abspath=os.path.abspath(sys.argv[0])
            ):
    """
    检测自启动的注册表是否已经注册程序
    :param key_name: #  要查询的键名
    :param reg_root: # 根节点
        #win32con.HKEY_CURRENT_USER
        #win32con.HKEY_CLASSES_ROOT
        #win32con.HKEY_CURRENT_USER
        #win32con.HKEY_LOCAL_MACHINE
        #win32con.HKEY_USERS
        #win32con.HKEY_CURRENT_CONFIG
    :param reg_path: #  键的路径
    :return: feedback(True 则已经注册过否则为False)
    """
    reg_flags = win32con.WRITE_OWNER | win32con.KEY_WOW64_64KEY | win32con.KEY_ALL_ACCESS
    feedback = False
    try:
        key = winreg.OpenKey(reg_root, reg_path, 0, reg_flags)
        location, type = winreg.QueryValueEx(key, key_name)
        feedback = True 
        if location != abspath:
            feedback = 1
            print('键存在，但程序位置发生改变')
    except FileNotFoundError as e:
        print("键不存在", e)
    except PermissionError as e:
        print("权限不足", e)
    except:
        print("Error")

    return feedback

def AutoRun(switch="open", 
            key_name='AutoCloudSync',
            abspath=os.path.abspath(sys.argv[0])):
    # 如果没有自定义路径，就用os.path.abspath(sys.argv[0])获取主程序的路径，如果主程序已经打包成exe格式，就相当于获取exe文件的路径

    flag = checkKey(reg_root=win32con.HKEY_CURRENT_USER,
                        reg_path=r"Software\\Microsoft\\Windows\\CurrentVersion\\Run",  # 键的路径
                        key_name=key_name,
                        abspath=abspath)
    # 注册表项名
    KeyName = r'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
    key = win32api.RegOpenKey(win32con.HKEY_CURRENT_USER, KeyName, 0, win32con.KEY_ALL_ACCESS)
    if switch == "open":
        # 异常处理
        try:
            if not flag:
                win32api.RegSetValueEx(key, key_name, 0, win32con.REG_SZ, abspath)
                win32api.RegCloseKey(key)
                print('开机自启动添加成功！')
        except:
            print('添加失败，未知错误')

    elif switch == "close":
        try:
            if flag:
                win32api.RegDeleteValue(key, key_name)  # 删除值
                win32api.RegCloseKey(key)
                print('成功删除键！')
        except:
            print('删除失败,未知错误！')

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # 定时器执行的间隔时间
        self.duration = self.resetDuration(interval)

        # 定时器用于定时执行脚本
        self.timer_ = QTimer(self)
        self.timer_.setInterval(1000)
        self.timer_.timeout.connect(lambda: refreshTimerSlot(self))

        # 系统托盘
        self.trayIcon_ = QSystemTrayIcon()     
        self.trayIcon_.activated.connect(self.trayClick)
        self.trayIcon_.setToolTip("xxx")

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
        self.setWindowIcon(QIcon(r":/img/icon_off.png"))

        # 限制lineEdit编辑框只能输入字符.和数字
        validator = QRegExpValidator(self)
        validator.setRegExp(QRegExp("([1-9])|(0.[1-9])"))
        self.ui.lineEdit.setValidator(validator)
        self.ui.lineEdit.setPlaceholderText("设置范围：0.1h~9h")
        self.ui.lineEdit.setText(str(interval))

        self.ui.pushButton.clicked.connect(lambda: pushButtonClickedEvent(self))
        self.ui.pushButton_2.clicked.connect(lambda: pushButton_2ClickedEvent(self))
        self.ui.pushButton.setEnabled(False)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton_3.clicked.connect(lambda: pushButton_3ClickedEvent(self))

        flag = checkKey()    # 这里检测一下程序自启动的注册表是否已经修改
        self.ui.checkBox.setChecked(flag)
        self.ui.checkBox.clicked.connect(lambda:checkBoxClickedEvent(self))

        self.ui.lcdNumber.setStyleSheet("border: 1px solid black; color: red;")
        self.ui.lcdNumber.setDigitCount(9)
        self.ui.lcdNumber.display("00:00:00")
        self.ui.lcdNumber.setSegmentStyle(QLCDNumber.Flat)

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
        self.trayIcon_.hide()

    def trayClick(self, reason):
        """
        托盘点击响应事件
        """
        print("trayClick")
        if reason == QSystemTrayIcon.Trigger:
            self.showNormal()
            self.activateWindow()

    def resetScript(self):
        """
        重置自动云同步
        """
        pushButtonClickedEvent(self)

    def resetDuration(self, h):
        return int(h*_SECONDS_OF_HOUR)

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
                quitAction = QAction(u"退出", self, triggered=qApp.quit)
                resetScriptAction = QAction(u"重置运行", self, triggered=self.resetScript)
                menu = QMenu()
                menu.addAction(resetScriptAction)
                menu.addAction(quitAction)
                self.trayIcon_.setContextMenu(menu)
                self.trayIcon_.setIcon(QIcon(r":/img/icon_off.png"))

                if not self.ui.pushButton.isEnabled():
                    self.trayIcon_.setIcon(QIcon(r":/img/icon_on.png"))

                QTimer.singleShot(600, lambda : _showTrayIconMesg())       
                
                self.trayIcon_.show()
                self.hide()
                
