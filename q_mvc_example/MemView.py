from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class MemoryView(QMainWindow):
    def __init__( self, inController, inModel, rowCount, parent = None ):
        super().__init__(parent)
        self.mController = inController
        self.mModel = inModel
        self.rowCount = rowCount
        self.ui = MemUi(self.mController, rowCount)
        self.setCentralWidget(self.ui)
        self.mModel.addObserver(self)
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)
        
    def modelIsChanged(self):        
        for row in range(self.rowCount):            
            self.ui.mem.setItemCode(row, self.mModel.getCellCode(row))
            self.ui.mem.setItemCommand(row, self.mModel.getCellCommand(row))
            self.ui.mem.setItemStop(row, self.mModel.getCellStop(row))
            self.ui.mem.setItemCursor(row, self.mModel.getCellCursor(row))
            
class MemUi(QWidget):
    def __init__(self, inController, rowCount, parent=None):
        super().__init__(parent)        
        wingrid = QGridLayout()
        wingrid.setSpacing(10)
        self.mem = MemTable(inController, rowCount)                                                
        wingrid.addWidget(self.mem, 0, 0)
        self.setLayout(wingrid)


class MemTableItem:
    def __init__(self, row):
        self.row = row
        self.addr = QLabel(text='8200')
        self.command = QLineEdit()
        self.code = QLineEdit()
        self.stop = QCheckBox()
        self.cursor = QRadioButton()
    
    def getRow(self):
        return self.row
    
    def getAddr(self):
        return self.addr.text()
    
    def setAddr(self, value):
        self.addr.setText(value)
        
    def getCode(self):
        return self.code.text()
        
    def setCode(self, value):
        self.code.setText(str(value))
        
    def getCommand(self):
        return self.command.text()
        
    def setCommand(self, value):
        self.command.setText(value)
    
    def getStop(self):
        return self.stop.isChecked()
    
    def setStop(self, state):
        self.stop.setChecked(state)
        
    def getCursor(self):
        return self.cursor.isChecked()
    
    def setCursor(self, state):
        self.cursor.setChecked(state)
        
class MemTable(QGroupBox):
    def __init__(self, inContr, rowCount):
        super().__init__(title='Memory')
        self.itemsList = []
        self.rowCount = rowCount
        self.inController = inContr
        self.table = QTableWidget(rowCount, 5)
        self.table.setHorizontalHeaderLabels(["Address", "Command", "Code", "Cursor", "Stop"])
        grid = QGridLayout()  
        grid.addWidget(self.table, 0, 0)
        for row in range(rowCount):
            item = MemTableItem(row)
            self.itemsList.append(item)
            self.table.setCellWidget(row, 0, item.addr)
            self.table.setCellWidget(row, 1, item.command)
            self.table.setCellWidget(row, 2, item.code)
            self.table.setCellWidget(row, 3, item.cursor)
            self.table.setCellWidget(row, 4, item.stop)
            item.stop.stateChanged.connect(lambda row=row: inContr.setMemStop(row))
            item.cursor.clicked.connect(lambda row=row: inContr.setMemCursor(row))
            item.code.editingFinished.connect(lambda row=row: inContr.setMemCode(row))
            item.command.editingFinished.connect(lambda row=row: inContr.setMemCommand(row))
            
        self.setLayout(grid)
        
            
    def getItem(self, row):
        if row<0 or row >= self.rowCount:
            return None
        else:
            return self.itemsList[row]
    
    def setItemCode(self, row, value):
        item = self.getItem(row)
        if not item:
            return
        item.setCode(value)
    
    def getItemCode(self, row):
        item = self.getItem(row)
        if not item:
            return
        return item.getCode()
    
    def setItemCommand(self, row, command):
        item = self.getItem(row)
        if not item:
            return
        item.setCommand(command)
    
    def getItemCommand(self, row):
        item = self.getItem(row)
        if not item:
            return
        return item.getCommand()
    
    def setItemCursor(self, row, state):
        item = self.getItem(row)
        if not item:
            return
        item.setCursor(state) 
        
    def getItemCursor(self, row):
        item = self.getItem(row)
        if not item:
            return        
        return item.getCursor()    
        
    def setItemStop(self, row, state):
        item = self.getItem(row)
        if not item:
            return
        item.setStop(state)
        
    def getItemStop(self, row):
        item = self.getItem(row)
        if not item:
            return
        return item.getStop()        