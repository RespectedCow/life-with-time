# counter.py
from PyQt5 import QtCore, QtGui, QtWidgets, QtTest
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QTime
import time
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
import importlib
loader = importlib.machinery.SourceFileLoader('tray', 'lib/src/system_tray_mode.py')
system_tray_mode = loader.load_module('tray')
import yaml
import threading


class Counter(QObject):

    timeMatched = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.__abort = False

    @pyqtSlot()
    def work(self, entries, app, window):
        self.shouldRun = True
        self.window = window
        self.twentyrulesTimer = 0
        with open("./lib/data/settings.yaml", 'r') as stream:
            settings = yaml.safe_load(stream)
        
        while self.shouldRun:
            app.processEvents()
            index = 0
            for entry in entries:
                if QTime.currentTime().hour() == entry[1].hour() and QTime.currentTime().minute() == entry[1].minute() and QTime.currentTime().second() == entry[1].second():
                    self.timeMatched.emit(index)
                index += 1
                
            # Additional features
            threading.Thread(target=self.twentyrules(settings)).start()

            if self.__abort:
                # note that "step" value will not necessarily be same for every thread
                break   
            
    def twentyrules(self, settings):
        if settings['twentyrules']:
            self.twentyrulesTimer += 1
                
            if self.twentyrulesTimer >= 1200:
                self.twentyrulesTimer = 0
                    
                # Notify the user
                QMessageBox.warning(self.window, "Look out now!", "It's time to look out now, nerd!", QMessageBox.Ok)
                    
            QtTest.QTest.qWait(1000)
            
    def abort(self):
        self.__abort = True
        self.worker.__del__