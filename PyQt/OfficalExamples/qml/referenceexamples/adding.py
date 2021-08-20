#!/usr/bin/env python

import sys

from PyQt5.QtCore import pyqtProperty, QCoreApplication, QObject, QUrl
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine


QML = b'''
import People 1.0

Person {
    name: "Bob Jones"
    shoeSize: 12
}
'''

class Person(QObject):
    def __init__(self, parent=None):
        super(Person, self).__init__(parent)

        self._name = ''
        self._shoeSize = 0

    @pyqtProperty(str)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @pyqtProperty(int)
    def shoeSize(self):
        return self._shoeSize

    @shoeSize.setter
    def shoeSize(self, shoeSize):
        self._shoeSize = shoeSize


app = QCoreApplication(sys.argv)

qmlRegisterType(Person, "People", 1, 0, "Person")

engine = QQmlEngine()

component = QQmlComponent(engine)
component.setData(QML, QUrl())

person = component.create()

if person is not None:
    print("The person's name is \"%s\"" % person.name)
    print("They wear a %d sized shoe" % person.shoeSize)
else:
    print("Unable to create component instance")
    for e in component.errors():
        print("Error:", e.toString());
