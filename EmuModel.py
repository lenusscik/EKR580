class EmuModel:
    def __init__(self):
        self._mFlagS = 0
        self._mFlagZ = 0
        self._mFlagAC = 0
        self._mFlagP = 0
        self._mFlagC = 0
        self._mRegisterA = 0
        self._mRegisterF = 0
        self._mRegisterB = 0
        self._mRegisterC = 0
        self._mRegisterD = 0
        self._mRegisterE = 0
        self._mRegisterH = 0
        self._mRegisterL = 0
        self._mRegisterAF = 0 
        self._mRegisterBC = 0
        self._mRegisterDE = 0
        self._mRegisterHL = 0
        self._mRegisterPC = 0
        self._mRegisterSP = 0
        self._mObservers = []
    
    @property
    def flagS(self):
        return self._mFlagS
    
    @flagS.setter
    def flagS(self, value):
        self._mFlagS = value
        self._mRegisterF = int("0b{}{}0{}0{}1{}".format(self._mFlagS,self._mFlagZ,self._mFlagAC,self._mFlagP,self._mFlagC),2)
        self._mRegisterAF = 256*self._mRegisterA + self._mRegisterF
        self.notifyObservers()    
    
    @property
    def flagZ(self):
        return self._mFlagZ
    
    @flagZ.setter
    def flagZ(self, value):
        self._mFlagZ = value
        self._mRegisterF = int("0b{}{}0{}0{}1{}".format(self._mFlagS,self._mFlagZ,self._mFlagAC,self._mFlagP,self._mFlagC),2)
        self._mRegisterAF = 256*self._mRegisterA + self._mRegisterF
        self.notifyObservers()    
    
    @property
    def flagAC(self):
        return self._mFlagAC
    
    @flagAC.setter
    def flagAC(self, value):
        self._mFlagAC = value
        self._mRegisterF = int("0b{}{}0{}0{}1{}".format(self._mFlagS,self._mFlagZ,self._mFlagAC,self._mFlagP,self._mFlagC),2)
        self._mRegisterAF = 256*self._mRegisterA + self._mRegisterF
        self.notifyObservers()    
    
    @property
    def flagP(self):
        return self._mFlagP
    
    @flagP.setter
    def flagP(self, value):
        self._mFlagP = value
        self._mRegisterF = int("0b{}{}0{}0{}1{}".format(self._mFlagS,self._mFlagZ,self._mFlagAC,self._mFlagP,self._mFlagC),2)
        self._mRegisterAF = 256*self._mRegisterA + self._mRegisterF
        self.notifyObservers()    
    
    @property
    def flagC(self):
        return self._mFlagC
    
    @flagC.setter
    def flagC(self, value):
        self._mFlagC = value
        self._mRegisterF = int("0b{}{}0{}0{}1{}".format(self._mFlagS,self._mFlagZ,self._mFlagAC,self._mFlagP,self._mFlagC),2)
        self._mRegisterAF = 256*self._mRegisterA + self._mRegisterF
        self.notifyObservers()    
    
    @property
    def regPC(self):
        return self._mRegisterPC    
    
    @regPC.setter
    def regPC(self, value):
        self._mRegisterPC = value
        self.notifyObservers()
    
    @property
    def regSP(self):
        return self._mRegisterSP    
    
    @regSP.setter
    def regSP(self, value):
        self._mRegisterSP = value
        self.notifyObservers()
                
    @property
    def regA(self):
        return self._mRegisterA
    
    @property
    def regF(self):
        return self._mRegisterF
    
    @property
    def regAF(self):        
        return self._mRegisterAF
    
    @regA.setter
    def regA(self, value):
        self._mRegisterA = value
        self._mRegisterAF = 256*self._mRegisterA + self._mRegisterF
        self.notifyObservers()
        
    @regF.setter    
    def regF(self, value):
        st = bin(value).ljust(10,'0')
        self._mFlagS = int(st[2])
        self._mFlagZ = int(st[3])
        self._mFlagAC = int(st[5])
        self._mFlagP = int(st[7])
        self._mFlagC = int(st[9])
        self._mRegisterF = int("0b{}{}0{}0{}1{}".format(self._mFlagS,self._mFlagZ,self._mFlagAC,self._mFlagP,self._mFlagC),2)
        self._mRegisterAF = 256*self._mRegisterA + self._mRegisterF
        self.notifyObservers()
        
    @regAF.setter
    def regAF(self, value):
        self._mRegisterA = value // 256        
        st = bin(value - self._mRegisterA*256).ljust(10,'0')
        self._mFlagS = int(st[2])
        self._mFlagZ = int(st[3])
        self._mFlagAC = int(st[5])
        self._mFlagP = int(st[7])
        self._mFlagC = int(st[9])
        self._mRegisterF = int("0b{}{}0{}0{}1{}".format(self._mFlagS,self._mFlagZ,self._mFlagAC,self._mFlagP,self._mFlagC),2)                
        self._mRegisterAF = 256*self._mRegisterA + self._mRegisterF
        self.notifyObservers()    
    
    @property
    def regB(self):
        return self._mRegisterB
    
    @property
    def regC(self):
        return self._mRegisterC
    
    @property
    def regBC(self):
        return self._mRegisterBC
    
    @regB.setter
    def regB(self, value):
        self._mRegisterB = value
        self._mRegisterBC = 256*self._mRegisterB + self._mRegisterC
        self.notifyObservers()
        
    @regC.setter    
    def regC(self, value):
        self._mRegisterC = value
        self._mRegisterBC = 256*self._mRegisterB + self._mRegisterC
        self.notifyObservers()
        
    @regBC.setter
    def regBC(self, value):
        self._mRegisterBC = value
        self._mRegisterB = value // 256
        self._mRegisterC = value - self._mRegisterB * 256
        self.notifyObservers()
          
    @property
    def regD(self):
        return self._mRegisterD
    
    @property
    def regE(self):
        return self._mRegisterE
    
    @property
    def regDE(self):
        return self._mRegisterDE
    
    @regD.setter
    def regD(self, value):
        self._mRegisterD = value
        self._mRegisterDE = 256*self._mRegisterD + self._mRegisterE
        self.notifyObservers()
        
    @regE.setter    
    def regE(self, value):
        self._mRegisterE = value
        self._mRegisterDE = 256*self._mRegisterD + self._mRegisterE
        self.notifyObservers()
        
    @regDE.setter
    def regDE(self, value):
        self._mRegisterDE = value
        self._mRegisterD = value // 256
        self._mRegisterE = value - self._mRegisterD * 256
        self.notifyObservers()
        
    @property
    def regH(self):
        return self._mRegisterH
    
    @property
    def regL(self):
        return self._mRegisterL
    
    @property
    def regHL(self):
        return self._mRegisterHL
    
    @regH.setter
    def regH(self, value):
        self._mRegisterH = value
        self._mRegisterHL = 256*self._mRegisterH + self._mRegisterL
        self.notifyObservers()
        
    @regL.setter    
    def regL(self, value):
        self._mRegisterL = value
        self._mRegisterHL = 256*self._mRegisterH + self._mRegisterL
        self.notifyObservers()
        
    @regHL.setter
    def regHL(self, value):
        self._mRegisterHL = value
        self._mRegisterH = value // 256
        self._mRegisterL = value - self._mRegisterH * 256
        self.notifyObservers()    
        
    def addObserver(self, inObserver):
        self._mObservers.append(inObserver)
        
    def removeObserver(self, inObserver):
        self._mObservers.remove(inObserver)
        
    def notifyObservers(self):
        for x in self._mObservers:
            x.modelIsChanged()