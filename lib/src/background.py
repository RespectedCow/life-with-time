# counter.py
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot, QTime
import time

class Counter(QObject):
    finished = pyqtSignal()
    timeMatched = pyqtSignal(int)


    @pyqtSlot()
    def procCounter(self, array): # A slot takes no params
        self.shouldRun = True

        while self.shouldRun:
            time.sleep(1)
            for entry in array:
                if QTime.currentTime().hour() == entry[1].hour() and QTime.currentTime().minute() == entry[1].minute():
                    self.timeMatched.emit(entry[0])   
                    self.shouldRun = False             


        self.finished.emit()