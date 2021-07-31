import fileinput as fi
import glob
import os.path
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QTime

def OpenFile(gui):
    # Create File browser
    fileName = QFileDialog.getOpenFileName(gui, "Select timetable", "",filter=("*.txt"))

    array = []

    if fileName:
        f = open(fileName[0])

        for line in f:
            if line != "":
                name, time = line.split()
                time = QTime.fromString(time)

                array.append([name, time])                

        
        return array
    else:
        reply = QMessageBox.warning(gui, 'Error', 'Something did not work.',
            QMessageBox.Ok)

    gui.setWindowTitle("Life With Time - " + fileName[1])
            

def saveFile(array, gui):
    # Check if there is anything in the array
    index = 0
    for _ in array:
        index += 1

    if index == 0:
        reply = QMessageBox.warning(gui, 'Array Error!', 'There is nothing in the timetable! Insert something!',
            QMessageBox.Ok)
        return

    # Add text to it
    fileName = QFileDialog.getSaveFileName(gui, 'Export', "timetable", filter=('*.txt'))
    if fileName[0] != "":   
        with open(fileName[0], 'w') as f:
                for x in array:
                    f.write(f"\n{x[0]} {QTime.toString(x[1])}")

    #Rename the window
    gui.setWindowTitle("Life With Time - " + fileName)