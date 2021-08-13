# -*- coding:utf-8 -*-
# environment：python 3.x，PyQt5, qdarkstyle
# copyright : huzhou
# time : 2019/3/13
"""
更新日志：
v1.0: 发布
"""

from PyQt5.QtWidgets import qApp, QAction,QMenu,QSystemTrayIcon,QSpinBox, QWidget, QMainWindow, QToolTip, QPushButton, QApplication,QGridLayout, QLineEdit, QTextEdit, QLabel, QCheckBox,QLCDNumber
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import QObject, QCoreApplication, Qt, QSettings, QThread, pyqtSignal, QTimer, QDateTime, QDate, QTime,QEvent
from weather import weather
import sys
import connect
import qdarkstyle       # 黑色主题
import time
import os

total_seconds = 0

def setTimer(refresh):
    timer = QTimer()
    timer.timeout.connect(refresh)
    timer.setInterval(1000)
    return timer

class TimeThread(QThread):
    """
    多线程动态显示时间
    """
    time_signal = pyqtSignal(str)      # 定义时间变化信号

    def __init__(self):
        super().__init__()

    def run(self):
        """
        开一条线程，在状态栏显示动态时间
        """
        date = time.strftime("%Y/%m/%d")
        while True:
            t = time.strftime('%H:%M:%S')
            self.time_signal.emit(date + ' ' + t)            # 发送信号让statusbar更新时间
            time.sleep(1)

class WeatherThread(QThread):
    """
    多线程显示天气
    """
    weather_signal = pyqtSignal(str)      # 定义天气信号
    def __init__(self):
        super().__init__()

    def run(self):
        """
        开一条线程，在状态栏加载天气
        """
        city_weather = weather().return_city_weather()
        if city_weather != None:
            aqi = self.AQI(int(city_weather['aqi']))
            signal = '                 ' + city_weather['cityname'] + '  ' + city_weather['temp'] + '℃' +\
            '  ' + city_weather['weather'] + '  '+ '空气质量：' + aqi + '  '+'降雨概率：'+ city_weather['rain']
        else:
            signal = '                                                  网络错误！请检查网络'
        self.weather_signal.emit(signal)

    def AQI(self, aqi):
        """
        aqi指数返回空气质量
        """
        if aqi >= 0 and aqi <= 50:
            return ' 优 '
        elif aqi >= 51 and aqi <= 100:
            return ' 良 '
        elif aqi >= 101 and aqi <= 150:
            return  '轻度污染'
        elif aqi >= 151 and aqi <= 200:
            return  '中度污染'
        elif aqi >= 201 and aqi <= 300:
            return  '重度污染'
        else:
            return '严重污染'

class SetTimeDlg(QWidget):
    """
    设置关机时间对话框
    """
    saveWindow_signal = pyqtSignal(bool,int,int,int)  # 定义保存窗口信息的信号，发送带有三个值的信号
    def __init__(self, saveValue):
        super().__init__()
        self.saveValue = saveValue
        self.initWidgets()
        self.initLayout()
        if len(self.saveValue):
            self.recoverWindow()
        self.initUI()

    def recoverWindow(self):
        """
        恢复到上次设置的状态
        """
        # 再次启动定时器，但是剩余时间需要更新
        self.seconds = self.saveValue[3]
        self.timer = setTimer(self.refresh)
        self.timer.start()

        self.confirm_btn.setText("取消")
        self.confirm_btn.setStyleSheet("background:red;color:white")
        self.hour_spinBox.setValue(self.saveValue[1])
        self.minute_spinBox.setValue(self.saveValue[2])
        self.lcd.display(self.seconds2time(self.saveValue[3]))
        self.setSpinBoxEnabled(False)


    def initUI(self):
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.setWindowTitle("设置关机时间")
        self.setWindowModality(Qt.ApplicationModal)     # 模态对话框
        self.resize(300,170)
        self.setFixedSize(self.width(), self.height())  # 禁止窗口拉伸
        self.setLayout(self.gridLayout)
        self.show()

    def initLayout(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.lcd, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.hour_spinBox, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.minute_spinBox, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.confirm_btn, 2, 0, 1, 2)
        self.gridLayout.setSpacing(3)

    def initWidgets(self):
        self.lcd = QLCDNumber(self)
        self.lcd.setDigitCount(12)
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.setStyleSheet("border: 2px solid black; color: red; background: black;")
        self.lcd.setFixedHeight(40)
        self.lcd.display("00:00:00")
        self.hour_spinBox = QSpinBox()
        self.hour_spinBox.setFixedHeight(26)
        self.hour_spinBox.setRange(0,11)
        self.hour_spinBox.setSingleStep(1)
        self.minute_spinBox = QSpinBox()
        self.minute_spinBox.setFixedHeight(26)
        self.minute_spinBox.setRange(0,59)
        self.minute_spinBox.setSingleStep(1)
        self.confirm_btn = QPushButton("确认")
        self.confirm_btn.setFont(QFont("微软雅黑", 12))
        self.confirm_btn.setStyleSheet("background:green;color:white")
        self.confirm_btn.setFixedHeight(32)
        self.confirm_btn.clicked.connect(self.setTime)
        self.trayIcon = QSystemTrayIcon()

    def closeEvent(self, QCloseEvent):
        """
        重写窗口关闭事件,
        """
        hours = self.hour_spinBox.value()
        minutes = self.minute_spinBox.value()
        if self.confirm_btn.text() == '取消':     # 关闭子页面如果按钮是取消，说明设置了关机时间，需要保存子窗口信息已备再次打开初始化
            # self.timer.stop()
            setTimeFlag = True
            self.saveWindow_signal[bool,int,int,int].emit(setTimeFlag,hours,minutes,self.seconds)
        else:
            setTimeFlag = False
            self.saveWindow_signal[bool,int,int,int].emit(setTimeFlag,hours,minutes,0)

    def setSpinBoxEnabled(self, bool):
        """
        设置SpinBox可不可用
        """
        self.hour_spinBox.setEnabled(bool)
        self.minute_spinBox.setEnabled(bool)

    def setTime(self):
        """
        确认按钮的响应事件
        """
        hours = self.hour_spinBox.value()
        minutes = self.minute_spinBox.value()
        if self.confirm_btn.text() == '确认' :
            if hours != 0 or minutes != 0:
                self.seconds = 3600*hours + 60*minutes
                self.timer = setTimer(self.refresh)
                self.timer.start()
                self.setSpinBoxEnabled(False)
                self.confirm_btn.setText("取消")
                self.confirm_btn.setStyleSheet("background:red;color:white")
        else:
            self.seconds = 0
            self.lcd.display("00:00:00")
            self.timer.stop()
            self.setSpinBoxEnabled(True)
            self.confirm_btn.setText("确认")
            self.confirm_btn.setStyleSheet("background:green;color:white")

    def seconds2time(self, seconds):
        h = seconds // 3600
        _m = seconds - h * 3600
        m = _m // 60
        s = _m - m * 60
        h = str(h) if h >= 10 else '0' + str(h)
        m = str(m) if m >= 10 else '0' + str(m)
        s = str(s) if s >= 10 else '0' + str(s)
        return h + ':' + m + ':' + s

    def refresh(self):
        """
        刷新LCD时间,时间一到就自动关机
        """
        if self.seconds > 0:
            time = self.seconds2time(self.seconds)
            self.seconds = self.seconds - 1
            self.lcd.display(time)
        else:
            self.lcd.display("00:00:00")
            self.timer.stop()
            os.system("shutdown -s -t 0 -f")

class LoginDlg(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initWidgets()
        self.initLayout()
        self.initUI()
        self.weather_info = None
        self.saveValue = []
        self.timer = None           # 判断是否是第二次进入子窗口

    def initWidgets(self):
        """
        组件初始化
        """
        self.status_textEdit = QTextEdit()      # 显示一些有关登陆的状态信息
        self.status_textEdit.setFixedHeight(90)
        self.status_textEdit.setReadOnly(True)      # 设置属性为只读
        self.head_label = QLabel(self)
        self.head_label.setPixmap(QPixmap(r'D:\Desktop\PyQt learning\Auto_Login\icons\head.jpg'))
        self.id_lineEdit = QLineEdit()
        self.pwd_lineEdit = QLineEdit()
        self.id_lineEdit.setPlaceholderText("学号")
        self.pwd_lineEdit.setPlaceholderText("密码")
        self.id_lineEdit.setFixedHeight(32)
        self.pwd_lineEdit.setFixedHeight(32)
        self.id_lineEdit.setFont(QFont("微软雅黑", 12))
        self.pwd_lineEdit.setFont(QFont("微软雅黑", 12))
        self.pwd_lineEdit.setEchoMode(QLineEdit.Password)
        # self.autorun_checkBox = QCheckBox("开机自启",self)
        self.remember_checkBox = QCheckBox("记住密码",self)
        self.remember_checkBox.stateChanged.connect(self.write_delete_Settings)
        self.login_btn = QPushButton("登录")
        self.login_btn.setFont(QFont("微软雅黑", 12))
        self.login_btn.setFixedHeight(32)
        self.login_btn.setStyleSheet("background:green;color:white")
        self.login_btn.clicked.connect(self.login_logout)
        self.autoshutdown_btn = QPushButton("定时关机")
        self.autoshutdown_btn.setFont(QFont("微软雅黑", 12))
        self.autoshutdown_btn.setFixedHeight(32)
        self.autoshutdown_btn.clicked.connect(self.autoShutDown)
        self.login_btn.setStyleSheet("background:green;color:white")
        self.trayIcon = QSystemTrayIcon()
        self.trayIcon.activated.connect(self.trayClick)

    def initLayout(self):
        """
        设置页面布局
        """
        self.gridLayout = QGridLayout()
        self.gridLayout.addWidget(self.status_textEdit, 0, 0, 1, 3)
        self.gridLayout.addWidget(self.head_label,1, 0, 3, 1)
        self.gridLayout.addWidget(self.id_lineEdit, 1, 1, 1, 2)
        self.gridLayout.addWidget(self.pwd_lineEdit,2, 1, 1, 2)
        # self.gridLayout.addWidget(self.autorun_checkBox , 3, 1, 1, 1)
        self.gridLayout.addWidget(self.remember_checkBox, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.login_btn, 4, 1, 1, 1)
        self.gridLayout.addWidget(self.autoshutdown_btn,4, 2, 1, 1)
        self.gridLayout.setSpacing(3)

    def initUI(self):
        """
        主窗口设计
        """
        myWidget = QWidget()
        self.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        self.resize(485, 325)
        self.setWindowTitle("校园网登陆客户端")
        self.setWindowIcon(QIcon(r"D:\Desktop\PyQt learning\Auto_Login\icons\net_fail.png"))
        myWidget.setLayout(self.gridLayout)
        self.setCentralWidget(myWidget)
        self.setFixedSize(self.width(), self.height())  # 禁止窗口拉伸
        self.setWindowFlag(Qt.Dialog)                   # 最大化按钮失效
        self.thread = TimeThread()                      # 开启显示动态时间的线程
        self.thread.time_signal.connect(self.showCurrentTime)
        self.thread.start()
        self.show()

    def closeEvent(self, QCloseEvent):
        """
        重写窗口关闭事件
        :param QCloseEvent:
        :return:
        """
        self.trayIcon.hide()

    def trayClick(self,reason):
        """
        托盘点击响应事件
        :return:
        """
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()
            self.activateWindow()

    def changeEvent(self, event):
        """
        重写窗口状态改变函数
        :param event:
        :return:
        """
        if self.isMinimized():
            quitAction = QAction(u"退出", self, triggered = qApp.quit)
            menu = QMenu()
            menu.addAction(quitAction)
            if self.login_btn.text() == '登录':
                self.trayIcon.setIcon(QIcon(r"D:\Desktop\PyQt learning\Auto_Login\icons\net_fail.png"))
            else:
                self.trayIcon.setIcon(QIcon(r"D:\Desktop\PyQt learning\Auto_Login\icons\net_success.png"))
            self.trayIcon.setToolTip("校园网客户端")
            self.trayIcon.showMessage("校园网客户端","已最小化至托盘")
            self.trayIcon.setContextMenu(menu)
            self.trayIcon.show()
            self.hide()
            event.ignore()

    def widgetEnable(self, flag):
        """
        控制是否禁用登录lineEdit
        """
        self.id_lineEdit.setReadOnly(flag)
        self.pwd_lineEdit.setReadOnly(flag)

    def getSaveWindowSignal(self, flag, hours, minutes, seconds):
        """
        接收子窗口关闭时的值
        """
        self.saveValue = []
        if flag:
            self.saveValue.append(flag)
            self.saveValue.append(hours)
            self.saveValue.append(minutes)
            self.seconds = seconds
            self.timer = setTimer(self.refresh1)
            self.timer.start()

    def autoShutDown(self):
        """
        定时关机btn响应事件
        """
        if self.timer != None:
            self.timer.stop()
            self.timer = None
            self.saveValue.append(self.seconds)
        self.setTimeDlg = SetTimeDlg(self.saveValue)
        self.setTimeDlg.saveWindow_signal[bool, int, int, int].connect(self.getSaveWindowSignal)        # 接受子窗口的信息


    def login_logout(self):
        """
        button点击响应登录或者注销事件
        """
        id = self.id_lineEdit.text()
        pwd = self.pwd_lineEdit.text()
        if self.login_btn.text() == '登录':
            try:
                assert id and pwd
                if connect.connect_to_network(self, id, pwd):
                    self.weather_info = '                                                  天气信息正在加载...'
                    self.status_textEdit.append(connect.current_time() + '  ' + "登录成功")
                    self.setWindowIcon(QIcon(r"D:\Desktop\PyQt learning\Auto_Login\icons\net_success.png"))
                    self.login_btn.setText('注销')
                    self.login_btn.setStyleSheet("color:white;background:red")
                    self.widgetEnable(True)
                    self.repaint()              # 需要立即重绘窗口

                    self.thread1 = WeatherThread()
                    self.thread1.weather_signal.connect(self.showWeather)
                    self.thread1.start()
            except AssertionError:
                if id == '':
                    self.id_lineEdit.setPlaceholderText("请输入账号")
                if pwd == '':
                    self.pwd_lineEdit.setPlaceholderText("请输入密码")
        else:
            if connect.disconnect_from_network(self, id, pwd):
                self.setWindowIcon(QIcon(r"D:\Desktop\PyQt learning\Auto_Login\icons\net_fail.png"))
                self.widgetEnable(False)
                self.login_btn.setText('登录')
                self.login_btn.setStyleSheet("color:white;background:green")


    def write_delete_Settings(self, state):
        """
        保存已知账号密码和记住密码的CheckBox选中状态
        """
        id = self.id_lineEdit.text()
        pwd = self.pwd_lineEdit.text()
        settings = QSettings("Hu_Soft", "hz")     # 用来记录登录的账号密码
        if state == Qt.Checked:
            try:
                assert id and pwd
                settings.beginGroup("login_info")  # 登录成功后且选中记住密码
                settings.setValue("id", id)
                settings.setValue("pwd", pwd)
                settings.setValue("checked", True)
                settings.endGroup()
            except AssertionError:
                pass
        else:
            settings.beginGroup("login_info")  # 登录成功后且选中记住密码
            settings.setValue("checked", False)
            settings.endGroup()

    def readSettings(self):
        """
        加载保存的账号和密码和checkbox选中状态
        """
        settings = QSettings("Hu_Soft", "hz")
        settings.beginGroup("login_info")
        if settings.value("checked") == 'true':     # 存储是str类型
            self.id_lineEdit.setText(settings.value("id"))
            self.pwd_lineEdit.setText(settings.value("pwd"))
            self.remember_checkBox.toggle()
            settings.endGroup()

    def showCurrentTime(self, time_signal):
        """
        槽函数，信号来自time_signal
        """
        if self.weather_info != None:
            self.statusBar().showMessage(time_signal + self.weather_info)
        else:
            self.statusBar().showMessage(time_signal + "                                                  天气信息正在加载 . . .")

    def showWeather(self, weather_signal):
        """
        槽函数接受weather_signal,来初始化天气信息
        """
        self.weather_info = weather_signal

    def refresh1(self):
        """
        设置时间后子窗口关闭后，seconds继续倒数，如果时间结束那么关机
        """
        if self.seconds > 0:
            if self.seconds == 60:
                self.trayIcon.showMessage("校园网客户端", "一分钟后自动关机！", QSystemTrayIcon.Warning)
            self.seconds = self.seconds - 1
        else:
            self.timer.stop()
            os.system("shutdown -s -t 0 -f")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = LoginDlg()
    login.readSettings()
    # 检测当前客户端是否联网，已联网初始化button为注销,并且获取天气信息
    if connect.net_reachable():
        thread1 = WeatherThread()
        thread1.weather_signal.connect(login.showWeather)
        thread1.start()
        login.setWindowIcon(QIcon(r"D:\Desktop\PyQt learning\Auto_Login\icons\net_success.png"))
        login.widgetEnable(True)
        login.login_btn.setText("注销")
        login.login_btn.setStyleSheet("color:white;background:red")
    else:
        login.weather_info = '                                                  暂无互联网连接'
    sys.exit(app.exec_())


