import sys
import time
import os

from PyQt5.QtCore import (QTime, QCoreApplication, QObject, QRunnable, QThread,
                          QThreadPool, pyqtSignal)

sys.path.append(os.path.abspath("../../"))
from launcher import current_running_array

while True:
    print("noob")
    time.sleep(1)
    for x in current_running_array:
        print(x)