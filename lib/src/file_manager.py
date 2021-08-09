from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QTime

def OpenFile(gui):
    # Create File browser
    fileName = QFileDialog.getOpenFileName(gui, "Select timetable", "",filter=("*.txt"))

    array = []

    gui.setWindowTitle("Life With Time - " + fileName[1])

    if fileName[0] != "":
        f = open(fileName[0])

        for line in f:
            datapacked = line.split()
            if datapacked != []:
                time = QTime.fromString(datapacked[1])
                print(datapacked[0])

                array.append([datapacked[0], time])                

        
        return array
    else:
        reply = QMessageBox.warning(gui, 'Error', 'Something did not work.',
            QMessageBox.Ok)

        return "Unsuccessful"    
            

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
    gui.setWindowTitle("Life With Time - " + fileName[0])