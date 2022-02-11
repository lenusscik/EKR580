class MemCell:
    def __init__(self, row):        
        self._mRow = row
        self._mCode = 0
        self._mCommand = ''
        self._mComExp = 1
        self._mStop = False
        self._mCursor = False
    
    def getCursor(self):
        return self._mCursor
        
    def setCursor(self, value):
        self._mCursor = value
      
    def getStop(self):
        return self._mStop
    
    def setStop(self, value):
        self._mStop = value
    
    def getCode(self):
        return self._mCode
    
    def setCode(self, value):
        self._mCode = value
     
    def getCommand(self):
        return self._mCommand
       
    def setCommand(self, comName):
        self._mCommand = comName
        #self._mComExp = int(comExp)
    
    @property    
    def comExp(self):
        return self._mComExp

class MemoryModel:
    def __init__(self, rowCount, prefix = 0):
        self.prefix = prefix
        self.rowCount = rowCount
        self.stackPointer = -1
        self.cursor = 0 
        self.memList = []
        self._mObservers = []
        for Row in range(rowCount):
            self.memList.append(MemCell(Row))
            
    def getPrefix(self):
        return self.prefix
    
    @property
    def RowCount(self):
        return self.rowCount
    
    def getCurSP(self):
        return self.prefix + self.rowCount + self.stackPointer
    
    def setCurSP(self, value):
        self.stackPointer = value - self.prefix - self.rowCount
        self.notifyObservers()
    
    def pushStack(self, high_value, low_value):
        for idx in range(self.stackPointer, -1, 2):
            self.memList[idx - 1].value = self.memList[idx + 1].value
            self.memList[idx].value = self.memList[idx + 2].value
        self.memList[-2].value = high_value 
        self.memList[-1].value = low_value
        self.stackPointer -= 2
        self.notifyObservers()
    
    def popStack(self):
        if self.stackPointer < -1:
            low_value = self.memList[-1].value
            high_value = self.memList[-2].value
            for idx in range(-3, self.stackPointer, -2):
                self.memList[idx + 2].value = self.memList[idx].value
                self.memList[idx + 1].value = self.memList[idx - 1].value
                self.memList[idx].value = 0
                self.memList[idx - 1].value = 0
            if self.stackPointer == -3:
                self.memList[-1].value = 0
                self.memList[-2].value = 0
            self.stackPointer += 2
            self.notifyObservers()
            return (high_value, low_value)    
    
    def getCell(self, row):
        if row<0 or row >= self.rowCount:
            return None
        else:
            return self.memList[row]
        
    def setCellCode(self, row, value):
        cell = self.getCell(row)
        if not cell:
            return
        cell.setCode(value)
        self.notifyObservers()
    
    def getCellCode(self, row):
        cell = self.getCell(row)
        if not cell:
            return
        return cell.getCode()
    
    def setCellCommand(self, row, command):
        cell = self.getCell(row)
        if not cell:
            return
        #if row>0:            
            #if self.getCell(row-1).comExp>1 or self.getCell(row-2).comExp==3:
                #cell.setCommand('', 0)
            #else:
        cell.setCommand(command)
        #else:
            #cell.setCommand(command)
        self.notifyObservers()
    
    def getCellCommand(self, row):
        cell = self.getCell(row)
        if not cell:
            return
        return cell.getCommand()
    
    def curCellCursor(self, row):
        cell = self.getCell(row)
        if not cell:
            return
        for x in self.memList:
            x.setCursor(False)
        cell.setCursor(True) 
        self.notifyObservers()
        
    def getCellCursor(self, row):
        return self.prefix + self.cursor
    
    def setCellCursor(self, row, state):
        cell = self.getCell(row)
        if not cell:
            return
        cell.setCursor(state)
        self.notifyObservers()    
    
    def invertCellStop(self, row):
        cell = self.getCell(row)
        if not cell:
            return
        cell.setStop(not cell.getStop())
        self.notifyObservers()
        
    def setCellStop(self, row, state):
        cell = self.getCell(row)
        if not cell:
            return
        cell.setStop(state)
        self.notifyObservers()
        
    def getCellStop(self, row):
        cell = self.getCell(row)
        if not cell:
            return
        return cell.getStop()        
        
    def addObserver(self, inObserver):
        self._mObservers.append(inObserver)
        
    def removeObserver(self, inObserver):
        self._mObservers.remove(inObserver)
        
    def notifyObservers(self):
        for x in self._mObservers:
            x.modelIsChanged()