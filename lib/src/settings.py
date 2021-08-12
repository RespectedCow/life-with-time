from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *

class Settings(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # Create UI
        uic.loadUi('./lib/settings.ui', self)

        # Set window attrs
        app_icon = QIcon()
        app_icon.addFile('icon.png', QSize(16,16))
        self.setWindowIcon(app_icon)

        self.setWindowTitle("Settings")