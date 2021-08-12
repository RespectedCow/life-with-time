#Imports
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
import sys
import importlib
loader = importlib.machinery.SourceFileLoader('maingui', 'lib/src/maingui.py')
maingui = loader.load_module('maingui')

# function
def main():
    app = QtGui.QApplication.instance()

    # check apps
    if app is None:
        app = QtGui.QApplication(sys.argv)
    else:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setText("Another instance of the application is running!")
        msg.setWindowTitle("Error!") 
        msg.setStandardButtons(QMessageBox.Yes)

        retval = msg.exec_()

    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("LifeWithTime")
    window = maingui.Ui(app)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
