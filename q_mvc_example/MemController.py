from MemView import MemoryView

class MemoryController:
    def __init__(self, inModel, rowCount):
        self.mModel = inModel
        self.mView = MemoryView(self, self.mModel, rowCount)
        self.mView.modelIsChanged()
        self.mView.show()

    def setMemCode(self, row):
        self.mModel.setCellCode(row, self.mView.ui.mem.getItemCode(row))
    
    def setMemCommand(self, row):
        self.mModel.setCellCommand(row, self.mView.ui.mem.getItemCommand(row))
        
    def setMemStop(self, row):
        #self.mModel.invertCellStop(row)
        self.mModel.setCellStop(row, self.mView.ui.mem.getItemStop(row))
        
    def setMemCursor(self, row):
        #self.mModel.setCellCursor(row, self.mView.ui.mem.getItemCursor(row))
        self.mModel.curCellCursor(row)    
        
    def updateMemCode(self):
        for row in range(self.mModel.getRowCount()):            
            self.mModel.setCellStop(row, self.mView.getItemStop(row))
    
    def updateMemCommand(self):
        for row in range(self.mModel.getRowCount()):            
            self.mModel.setCellCommand(row, self.mView.getItemCommand(row))
            
    def updateMemStop(self):
        for row in range(self.mModel.getRowCount()):            
            self.mModel.setCellStop(row, self.mView.getItemStop(row))
            
    def updateMemCursor(self):
        for row in range(self.mModel.getRowCount()):            
            self.mModel.setCellCursor(row, self.mView.getItemStop(row))    
    
    def setRegB(self):
        b = self.mView.ui.r_b.value()
        self.mModel.regB = b

    def setRegC(self):
        c = self.mView.ui.r_c.value()
        self.mModel.regC = c
    
    def setRegBC(self):
        bc = self.mView.ui.r_bc.value()
        self.mModel.regBC = bc    