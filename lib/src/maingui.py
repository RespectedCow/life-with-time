#Imports
from PyQt5 import uic, QtGui
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTime, QRunnable, QThreadPool, QCoreApplication, QThread, QProcess, Qt, pyqtSignal, QSize
import sys
import importlib
loader = importlib.machinery.SourceFileLoader('background', 'lib/src/background.py')
background = loader.load_module('background')

loader = importlib.machinery.SourceFileLoader('system_tray_mode', 'lib/src/system_tray_mode.py')
system_tray_mode = loader.load_module('system_tray_mode')

loader = importlib.machinery.SourceFileLoader('filemanager', 'lib/src/file_manager.py')
FileManager = loader.load_module('filemanager')

#variables
defaultTime = QTime(12, 00, 00)
current_running_array = []
widget_entries = []

#functions
def addEntry(name, time):
    current_running_array.append([name, time])

    print(current_running_array)

def checkArray(array, check):
    for x in array:
        if x[1] == check:
            return True

    return False

#class
class Ui(QMainWindow):
    tray_icon = None
    sig_abort_workers = pyqtSignal()
    NUM_THREADS = 1

    def closeProgram(self):
        reply = QMessageBox.question(self, "Close Program", "Do you really want to exit the program?", QMessageBox.Yes | QMessageBox.No)

        if reply == QMessageBox.Yes:
            reply = QMessageBox.question(self, 'Edit Timetable?', 'Do you want to edit the timetable?',
            QMessageBox.Yes | QMessageBox.No) 
            if reply == QMessageBox.Yes:
                self.show()
            else:
                sys.exit()
            self.worker.shouldRun = False
            self.tray_icon.hide()
            self.thread.quit()
        if QMessageBox.No:
            print("Returning to normal functions")

    def timeMatched(self, index):
        name = current_running_array[index][0]
        time = current_running_array[index][0]

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(f"It's time to {name}. Do you want to change your timetable?")
        msg.setWindowTitle(name) 
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        retval = msg.exec_()

        if retval == QMessageBox.Yes:
           self.show()
           self.thread.quit()
           self.worker.shouldRun = False 

    def updateEntries(self):
        self.entryTable.clear()

        for entry in current_running_array:
            time = QTime.toString(entry[1])
            entry = QTreeWidgetItem(self.entryTable, [entry[0], time])

    def removeEntryfunction(self):
        time = self.entryTable.currentItem().text(1)
        
        print(time)
        index = 0

        time = QTime.fromString(time)

        for x in current_running_array:
            if x[1] == time:
                current_running_array.pop(index)

            index += 1
        
        self.updateEntries()

    def changeMessage(self, message):
        self.label.setText(message)

    def openTimetable(self):
        new_array = FileManager.OpenFile(self)

        #clear array
        index = 0
        for x in current_running_array:
            current_running_array.pop(index)
            index += 1

        # assign
        for x in new_array:
            current_running_array.append([x[0], x[1]])

        self.updateEntries()
        self.changeMessage("Successfully opened a timetable file!")

    def compileEntryData(self):
        name = self.EntryName.text()
        time = self.EntryTime.time()

        self.EntryName.setText("")
        self.EntryTime.setTime(defaultTime)

        if name != "" and checkArray(current_running_array, time) == False and len(name.split()) == 1:
            addEntry(name, time)
            self.updateEntries()
            self.changeMessage("Entry was successfully created")
        elif checkArray(current_running_array, time):
            # Delete previous entry
            reply = QMessageBox.question(self, 'Delete previous entry(Time conflict)', 'Are you sure you want to delete the previous entry?',
            QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                index = 0

                for x in current_running_array: 
                    if x[1] == time:
                        current_running_array.pop(index)
                    index += 1                

                addEntry(name, time)
                self.updateEntries()
        elif len(name.split()) != 1:
            reply = QMessageBox.question(self, 'System Error', 'Only one word allowed!',
            QMessageBox.Ok)
        else:
            self.changeMessage("Entries's name is empty!")

    def run(self, app):
        self.tray_icon.show()
        self.tray_icon.showMessage("Counting started", "The app will start matching the current time to your timetable.", QSystemTrayIcon.Information, 2000)
        qApp.processEvents()
        
        #values
        self.__threads = []

        # Start background thread
        self.worker = background.Counter()
        self.thread = QThread()
        self.__threads.append((self.thread, self.worker))  # need to store worker too otherwise will be gc'd
        self.worker.moveToThread(self.thread)

        # control worker:
        self.sig_abort_workers.connect(self.worker.abort)
        self.worker.timeMatched.connect(self.timeMatched)
        self.hide()

        self.thread.started.connect(lambda: self.worker.work(current_running_array, app))
        self.thread.start()

    def __init__(self, app):
        QMainWindow.__init__(self)
        uic.loadUi('./lib/mainapp.ui', self)
        self.setWindowTitle("LifeWithTime")

        #Icons
        app_icon = QtGui.QIcon()
        app_icon.addFile('icon.png', QSize(16,16))
        self.setWindowIcon(app_icon)

        # Create system tray app
        self.tray_icon = system_tray_mode.Tray(self)

        #events
        self.removeEntry.clicked.connect(self.removeEntryfunction)
        self.addEntry.clicked.connect(self.compileEntryData)
        self.runbutton.clicked.connect(lambda: self.run(app))

        self.actionSave.triggered.connect(lambda: FileManager.saveFile(current_running_array, self))
        self.actionOpen.triggered.connect(self.openTimetable)

        #Stuff
        self.EntryTime.setTime(defaultTime)
        self.__threads = None
        self.__objs = None

        self.show()

def main():
    app = QApplication([])
    mw = Ui(app)
    mw.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()