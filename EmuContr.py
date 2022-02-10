from EmuView import EmuView

class EmuController:
    def __init__(self, inModel):
        self.mModel = inModel
        self.mView = EmuView(self, self.mModel)
        self.mView.show()

    def setFlagS(self):
        self.mModel.flagS = int(self.mView.ui.f_s.text())    
    
    def setFlagZ(self):
        self.mModel.flagZ = int(self.mView.ui.f_z.text())
        
    def setFlagAC(self):
        self.mModel.flagAC = int(self.mView.ui.f_ac.text())    
    
    def setFlagP(self):
        self.mModel.flagP = int(self.mView.ui.f_p.text())
        
    def setFlagC(self):
        self.mModel.flagC = int(self.mView.ui.f_c.text())    
       
    
    def setRegA(self):
        self.mModel.regA = self.mView.ui.r_a.value()

    def setRegF(self):
        self.mModel.regF = self.mView.ui.r_f.value()
    
    def setRegAF(self):
        self.mModel.regAF = self.mView.ui.r_af.value()
        
    def setRegB(self):
        self.mModel.regB = self.mView.ui.r_b.value()

    def setRegC(self):
        self.mModel.regC = self.mView.ui.r_c.value()

    def setRegBC(self):
        self.mModel.regBC = self.mView.ui.r_bc.value()
        
    def setRegD(self):
        self.mModel.regD = self.mView.ui.r_d.value()

    def setRegE(self):
        self.mModel.regE = self.mView.ui.r_e.value()

    def setRegDE(self):
        self.mModel.regDE = self.mView.ui.r_de.value()
        
    def setRegH(self):
        self.mModel.regH = self.mView.ui.r_h.value()

    def setRegL(self):
        self.mModel.regL = self.mView.ui.r_l.value()

    def setRegHL(self):
        self.mModel.regHL = self.mView.ui.r_hl.value()
        
    def setRegPC(self):
        self.mModel.regPC = self.mView.ui.r_pc.value()
        
    def setRegSP(self):
        self.mModel.regSP = self.mView.ui.r_sp.value()    