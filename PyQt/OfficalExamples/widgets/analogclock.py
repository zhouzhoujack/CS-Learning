#!/usr/bin/env python

from PyQt5.QtCore import QPoint, Qt, QTime, QTimer
from PyQt5.QtGui import QColor, QPainter, QPolygon
from PyQt5.QtWidgets import QApplication, QWidget

class AnalogClock(QWidget):
    hourHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -40)
    ])

    minuteHand = QPolygon([
        QPoint(7, 8),
        QPoint(-7, 8),
        QPoint(0, -60)
    ])

    secondHand = QPolygon([
        QPoint(4, 5),
        QPoint(-4, 5),
        QPoint(0, -75)
    ])

    hourColor = QColor(127, 0, 127)
    minuteColor = QColor(0, 127, 127, 191)
    secondColor = QColor(127, 0, 0, 191)

    def __init__(self, parent=None):
        super(AnalogClock, self).__init__(parent)

        timer = QTimer(self)
        timer.timeout.connect(self.update)
        timer.start(1000)

        self.setWindowTitle("Analog Clock")
        self.resize(400, 400)

    def paintEvent(self, event):
        side = min(self.width(), self.height())
        time = QTime.currentTime()

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)        # 设置渲染
        painter.translate(self.width() / 2, self.height() / 2)  # 设置坐标变换
        painter.scale(side / 200.0, side / 200.0)

        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.secondColor)
        painter.save()
        painter.rotate(6.0 * (time.second()))
        painter.drawConvexPolygon(AnalogClock.secondHand)
        painter.restore()
        painter.setPen(AnalogClock.secondColor)

        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.hourColor)
        painter.save()
        painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
        painter.drawConvexPolygon(AnalogClock.hourHand)
        painter.restore()
        painter.setPen(AnalogClock.hourColor)

        # 时钟的小时标识符
        for i in range(12):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(30.0)
        painter.setPen(Qt.NoPen)
        painter.setBrush(AnalogClock.minuteColor)
        painter.save()
        painter.rotate(6.0 * (time.minute() + time.second() / 60.0))
        painter.drawConvexPolygon(AnalogClock.minuteHand)
        painter.restore()
        painter.setPen(AnalogClock.minuteColor)

        # 时钟的分钟标识符
        for j in range(60):
            if (j % 5) != 0:
                painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    clock = AnalogClock()
    clock.show()
    sys.exit(app.exec_())
