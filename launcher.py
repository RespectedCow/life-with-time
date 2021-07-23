#Imports
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTime
import sys

#variables
defaultTime = QTime(12, 00, 00)
current_running_array = []

# functions
def updateHolding():
    print("bruh")

def addEntry(name, time):
    current_running_array.append([name, time])

    print(current_running_array)

def checkArray(array, check):
    for x in array:
        if x[0] == check:
            return True

    return False

#class
class Ui(QtWidgets.QMainWindow):
    def updateEntries(self):
        for entry in current_running_array:
            print("gayyy")

    def changeMessage(self, message):
        self.label.setText(message)

    def compileEntryData(self):
        name = self.EntryName.text()
        time = self.EntryTime.time()

        self.EntryName.setText("")
        self.EntryTime.setTime(defaultTime)

        if name != "" and checkArray(current_running_array, name) == False:
            addEntry(name, time)
            self.changeMessage("Entry was successfully created")
        elif checkArray(current_running_array, name):
            # Delete previous entry
            index = 0

            for x in current_running_array: 
                if x[0] == name:
                    current_running_array.pop(index)
                index += 1

            reply = QMessageBox.question(self, 'Delete previous entry?', 'Are you sure you want to delete the previous entry?',
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                addEntry(name, time)
        else:
            self.changeMessage("Entries's name is empty!")

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('./lib/mainapp.ui', self)

        self.EntryTime.setTime(defaultTime)

        #events
        self.addEntry.clicked.connect(self.compileEntryData)

        self.show()

    

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()