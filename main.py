from EmuModel import EmuModel
from EmuContr import EmuController

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

def main():
    app = QApplication( sys.argv )
    model = EmuModel()
    controller = EmuController(model)

    app.exec_()

if __name__ == '__main__':
    sys.exit(main())