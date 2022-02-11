from MemModel import MemoryModel
from MemController import MemoryController

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def main():
    app = QApplication(sys.argv)
    rowCnt = 100
    prefix = 0
    model = MemoryModel(rowCnt, prefix)
    controller = MemoryController(model, rowCnt)

    app.exec_()

if __name__ == '__main__':
    sys.exit(main())