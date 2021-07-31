#Imports
from PyQt5 import QtWidgets
import sys
import importlib
loader = importlib.machinery.SourceFileLoader('maingui', 'lib/src/maingui.py')
maingui = loader.load_module('maingui')

# function
def main():
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.setApplicationName("LifeWithTime")
    window = maingui.Ui(app)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
