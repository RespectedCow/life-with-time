from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *
import yaml
import io

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
        
        # Load settings
        self.loadSettings()
        
        # Set triggers
        self.applyButton.clicked.connect(self.saveChanges)
        self.cancelButton.clicked.connect(self.close)
        
    def loadSettings(self):
        # Get settings value
        with open("./lib/data/settings.yaml", 'r') as stream:
            settings = yaml.safe_load(stream)
            
        if settings == None:
            return
            
        # Load settings
        if 'twentyrules' in settings:
            self.twentyrules.setChecked(settings['twentyrules'])
        else:
            self.twentyrules.setChecked(False) # Default value
        if 'timematched' in settings['messages']:
            self.timematchEdit.setPlainText(settings['messages']['timematched'])
        else:
            self.timematchEdit.setPlainText("It's time to {name}. Do you want to change your timetable? ")
        
    def saveChanges(self):
        settings = {}
        print("Saving settings.")
        
        # Get settings
        twentyrules = False
        if self.twentyrules.isChecked():
            twentyrules = True
            
        timeMatchmessage = self.timematchEdit.toPlainText()
        
        # Write settings
        settings = {
            'twentyrules': twentyrules,
            'messages': {
                'timematched': timeMatchmessage
            }
        }
        with io.open('./lib/data/settings.yaml', 'w', encoding='utf8') as outfile:
            yaml.dump(settings, outfile, default_flow_style=False, allow_unicode=True)
        
        print("Applying changes.")
        self.close()
        
    def cancel(self):
        self.close()