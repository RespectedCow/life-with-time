# counter.py
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QTime
import time
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
import importlib
loader = importlib.machinery.SourceFileLoader('tray', 'lib/src/system_tray_mode.py')
system_tray_mode = loader.load_module('tray')


class Counter(QObject):

    timeMatched = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.__abort = False

    @pyqtSlot()
    def work(self, entries, app):
        self.shouldRun = True

        while self.shouldRun:
            app.processEvents()
            index = 0
            for entry in entries:
                if QTime.currentTime().hour() == entry[1].hour() and QTime.currentTime().minute() == entry[1].minute() and QTime.currentTime().second() == entry[1].second():
                    self.timeMatched.emit(index)
                index += 1

            if self.__abort:
                # note that "step" value will not necessarily be same for every thread
                break   
            

    def abort(self):
        self.__abort = True
