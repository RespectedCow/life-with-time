#Imports
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTime, QRunnable, QThreadPool, QCoreApplication, QThread, QProcess, Qt
import sys
import os
import time
import importlib
loader = importlib.machinery.SourceFileLoader('maingui', 'lib/src/maingui.py')
maingui = loader.load_module('maingui')

# function
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = maingui.Ui()
    app.exec_()

if __name__ == "__main__":
    main()
