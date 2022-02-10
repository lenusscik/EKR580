from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class EmuView(QMainWindow):
    def __init__( self, inController, inModel, parent = None ):
        super().__init__(parent)
        self.mController = inController
        self.mModel = inModel
        self.ui = RegUi()
        self.setCentralWidget(self.ui)
        self.mModel.addObserver(self)
        font = QFont()
        font.setPointSize(14)
        self.setFont(font)
        
        self.ui.f_s.setValidator(QIntValidator(0, 1))
        self.ui.f_s.editingFinished.connect(self.mController.setFlagS)
        
        self.ui.f_z.setValidator(QIntValidator(0, 1))
        self.ui.f_z.editingFinished.connect(self.mController.setFlagZ)
        
        self.ui.f_ac.setValidator(QIntValidator(0, 1))
        self.ui.f_ac.editingFinished.connect(self.mController.setFlagAC)
        
        self.ui.f_p.setValidator(QIntValidator(0, 1))
        self.ui.f_p.editingFinished.connect(self.mController.setFlagP)
        
        self.ui.f_c.setValidator(QIntValidator(0, 1))
        self.ui.f_c.editingFinished.connect(self.mController.setFlagC)        
        
        self.ui.r_a.editingFinished.connect(self.mController.setRegA)
        self.ui.r_f.editingFinished.connect(self.mController.setRegF)
        self.ui.r_af.editingFinished.connect(self.mController.setRegAF)
        self.ui.r_b.editingFinished.connect(self.mController.setRegB)
        self.ui.r_c.editingFinished.connect(self.mController.setRegC)
        self.ui.r_bc.editingFinished.connect(self.mController.setRegBC)
        self.ui.r_d.editingFinished.connect(self.mController.setRegD)
        self.ui.r_e.editingFinished.connect(self.mController.setRegE)
        self.ui.r_de.editingFinished.connect(self.mController.setRegDE)
        self.ui.r_h.editingFinished.connect(self.mController.setRegH)
        self.ui.r_l.editingFinished.connect(self.mController.setRegL)
        self.ui.r_hl.editingFinished.connect(self.mController.setRegHL)
        
        self.ui.r_pc.editingFinished.connect(self.mController.setRegPC)
        self.ui.r_sp.editingFinished.connect(self.mController.setRegSP)
        
    def modelIsChanged(self):
        self.ui.f_s.setText(str(self.mModel.flagS))
        self.ui.f_z.setText(str(self.mModel.flagZ))
        self.ui.f_ac.setText(str(self.mModel.flagAC))
        self.ui.f_p.setText(str(self.mModel.flagP))
        self.ui.f_c.setText(str(self.mModel.flagC))

        self.ui.r_af.setValue(self.mModel.regAF)
        self.ui.r_a.setValue(self.mModel.regA)
        self.ui.r_f.setValue(self.mModel.regF)
        self.ui.r_bc.setValue(self.mModel.regBC)
        self.ui.r_b.setValue(self.mModel.regB)
        self.ui.r_c.setValue(self.mModel.regC)
        self.ui.r_de.setValue(self.mModel.regDE)
        self.ui.r_d.setValue(self.mModel.regD)
        self.ui.r_e.setValue(self.mModel.regE)
        self.ui.r_hl.setValue(self.mModel.regHL)
        self.ui.r_h.setValue(self.mModel.regH)
        self.ui.r_l.setValue(self.mModel.regL)
        
        self.ui.r_pc.setValue(self.mModel.regPC)
        self.ui.r_sp.setValue(self.mModel.regSP)

class RegUi(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        wingrid = QGridLayout()
        wingrid.setSpacing(10)
        
        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        #self.table.resize(500, 200)
        self.tree.setHeaderLabels(['Элемент', 'Значение'])
        
        self.f_s = QLineEdit(text='0')
        self.f_z = QLineEdit(text='0')
        self.f_ac = QLineEdit(text='0')
        self.f_p = QLineEdit(text='0')
        self.f_c = QLineEdit(text='0')
        
        self.r_pc = QSpinBox(value=0, displayIntegerBase=16, maximum = 65535)
        self.r_sp = QSpinBox(value=0, displayIntegerBase=16, maximum = 65535)
        
        self.r_a = QSpinBox(value=0, displayIntegerBase=16, maximum = 255)
        self.r_f = QSpinBox(value=0, displayIntegerBase=16, maximum = 255)
        self.r_af = QSpinBox(value=0, displayIntegerBase=16, maximum = 65535)
        self.r_b = QSpinBox(value=0, displayIntegerBase=16, maximum = 255)
        self.r_c = QSpinBox(value=0, displayIntegerBase=16, maximum = 255)
        self.r_bc = QSpinBox(value=0, displayIntegerBase=16, maximum = 65535)
        self.r_d = QSpinBox(value=0, displayIntegerBase=16, maximum = 255)
        self.r_e = QSpinBox(value=0, displayIntegerBase=16, maximum = 255)
        self.r_de = QSpinBox(value=0, displayIntegerBase=16, maximum = 65535)
        self.r_h = QSpinBox(value=0, displayIntegerBase=16, maximum = 255)
        self.r_l = QSpinBox(value=0, displayIntegerBase=16, maximum = 255)
        self.r_hl = QSpinBox(value=0, displayIntegerBase=16, maximum = 65535)        
        
        flags = QTreeWidgetItem(['Флаги',''])
        flagS_item = QTreeWidgetItem(['S', ''])
        flagZ_item = QTreeWidgetItem(['Z', ''])
        flagAC_item = QTreeWidgetItem(['AC', ''])
        flagP_item = QTreeWidgetItem(['P', ''])
        flagC_item = QTreeWidgetItem(['C', ''])
        flags.addChild(flagS_item)
        flags.addChild(flagZ_item)
        flags.addChild(flagAC_item)
        flags.addChild(flagP_item)
        flags.addChild(flagC_item)
        self.tree.setItemWidget(flagS_item, 1, self.f_s)
        self.tree.setItemWidget(flagZ_item, 1, self.f_z)
        self.tree.setItemWidget(flagAC_item, 1, self.f_ac)
        self.tree.setItemWidget(flagP_item, 1, self.f_p)
        self.tree.setItemWidget(flagC_item, 1, self.f_c)
        self.tree.addTopLevelItem(flags)
        
        
        pointers = QTreeWidgetItem(["Указатели", ''])
        regPC_item = QTreeWidgetItem(['PC', ''])
        regSP_item = QTreeWidgetItem(['SP', ''])        
        pointers.addChild(regPC_item)
        pointers.addChild(regSP_item)
        
        self.tree.setItemWidget(regPC_item, 1, self.r_pc)
        self.tree.setItemWidget(regSP_item, 1, self.r_sp)
        self.tree.addTopLevelItem(pointers)        
        
        
        registers = QTreeWidgetItem(["Регистры", ''])
        regA_item = QTreeWidgetItem(['A', ''])
        regF_item = QTreeWidgetItem(['F', ''])
        regAF_item = QTreeWidgetItem(['AF', ''])
        regAF_item.addChild(regA_item)
        regAF_item.addChild(regF_item)
        registers.addChild(regAF_item)
        regB_item = QTreeWidgetItem(['B', ''])
        regC_item = QTreeWidgetItem(['C', ''])
        regBC_item = QTreeWidgetItem(['BC', ''])
        regBC_item.addChild(regB_item)
        regBC_item.addChild(regC_item)
        registers.addChild(regBC_item)
        regD_item = QTreeWidgetItem(['D', ''])
        regE_item = QTreeWidgetItem(['E', ''])
        regDE_item = QTreeWidgetItem(['DE', ''])
        regDE_item.addChild(regD_item)
        regDE_item.addChild(regE_item)
        registers.addChild(regDE_item)
        regH_item = QTreeWidgetItem(['H', ''])
        regL_item = QTreeWidgetItem(['L', ''])
        regHL_item = QTreeWidgetItem(['HL', ''])
        regHL_item.addChild(regH_item)
        regHL_item.addChild(regL_item)
        registers.addChild(regHL_item)        
        
        self.tree.setItemWidget(regA_item, 1, self.r_a)
        self.tree.setItemWidget(regF_item, 1, self.r_f)
        self.tree.setItemWidget(regAF_item, 1, self.r_af)
        self.tree.setItemWidget(regB_item, 1, self.r_b)
        self.tree.setItemWidget(regC_item, 1, self.r_c)
        self.tree.setItemWidget(regBC_item, 1, self.r_bc)        
        self.tree.setItemWidget(regD_item, 1, self.r_d)
        self.tree.setItemWidget(regE_item, 1, self.r_e)
        self.tree.setItemWidget(regDE_item, 1, self.r_de)        
        self.tree.setItemWidget(regH_item, 1, self.r_h)
        self.tree.setItemWidget(regL_item, 1, self.r_l)
        self.tree.setItemWidget(regHL_item, 1, self.r_hl)        
        self.tree.addTopLevelItem(registers)                
        
        
        wingrid.addWidget(self.tree, 0, 0)
        
        self.setLayout(wingrid)        