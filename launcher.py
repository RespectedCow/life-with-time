#Imports
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTime, QRunnable, QThreadPool, QCoreApplication, QThread, QProcess, Qt
import sys
import os
import time

#variables
defaultTime = QTime(12, 00, 00)
current_running_array = []
widget_entries = []

# function
def addEntry(name, time):
    current_running_array.append([name, time])

    print(current_running_array)

def checkArray(array, check):
    for x in array:
        if x[1] == check:
            return True

    return False

#class
class Ui(QtWidgets.QMainWindow):
    def updateEntries(self):
        self.entryTable.clear()

        for entry in current_running_array:
            time = QTime.toString(entry[1])

            self.entryTable.addItem(f"{entry[0]}  {time}")

    def removeEntryfunction(self):
        name, time = self.entryTable.currentItem().text().split()
        index = 0

        time = QTime.fromString(time)

        for x in current_running_array:
            if x[1] == time:
                current_running_array.pop(index)

            index += 1
        
        self.updateEntries()

    def changeMessage(self, message):
        self.label.setText(message)

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
            QMessageBox.Yes | QMessageBox.Cancel)
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

    def run(self):
        if self.isRunningBack == False:
            self.runbutton.setText("Stop")
            self.isRunningBack = True
        else:
            self.isRunningBack = True
            self.runbutton.setText("Run")

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('./lib/mainapp.ui', self)

        self.EntryTime.setTime(defaultTime)
        self.isRunningBack = False

        #events
        self.removeEntry.clicked.connect(self.removeEntryfunction)
        self.addEntry.clicked.connect(self.compileEntryData)
        self.runbutton.clicked.connect(self.run)

        self.show()

    
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()
    while window.isRunningBack:
        for entry in current_running_array:
            time.sleep(1)
            if QTime.currentTime().hour() == entry[1].hour() and QTime.currentTime().minute() == entry[1].minute():
                print("waw")

    

if __name__ == "__main__":
    main()
