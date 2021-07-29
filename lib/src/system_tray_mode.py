import time
import sys

from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from PyQt5 import QtGui


class Tray(QSystemTrayIcon):
    def __init__(self, creator):
        QSystemTrayIcon.__init__(self)
        #Icons
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon.png"), QtGui.QIcon.Selected, QtGui.QIcon.On)
        self.setIcon(icon)
        
        quit_action = QAction("Exit", creator)
        quit_action.triggered.connect(creator.closeProgram)
        tray_menu = QMenu()
        tray_menu.addAction(quit_action)
        self.setContextMenu(tray_menu)
        self.hide()