#implementaion
def MyReverse(lst):
    temp=[]
    for x in range(len(lst), 0, -1):
        temp.append(x)
    return temp
# обявление классов    
class Register():#Класс для описания регистровых пар
    RegList=[]
    
    def __init__(self, name='', val1=0, val2=0):
        self.name = name
        self.val1 = val1
        self.val2 = val2
        Register.RegList.append(self)
        pass
    
    def GetRegByName(regname):
        for x in range(len(Register.RegList)):
            if Register.RegList[x].name[0] == regname:
                return Register.RegList[x].val1
            elif Register.RegList[x].name[1] == regname:
                return Register.RegList[x].val2
            elif Register.RegList[x].name == regname:
                return (Register.RegList[x].val1,Register.RegList[x].val2)
            
    def SetRegByName(regname, val1=None, val2=None):
        for x in range(len(Register.RegList)):
            if Register.RegList[x].name == regname:
                if val1!=None and val2 ==None:
                    Register.RegList[x].val1 = int(val1)
                elif val1==None and val2 !=None:
                    Register.RegList[x].val2 = int(val2)                        
                    
class DataRecord():#класс записи памяти(строка)
    
    def __init__(self, addr = 0 , val = 0, cmd = None, brpt = False, crsr = False):
        self.addr = addr
        self.val = val
        self.comand = cmd
        self.breakpoint = brpt
        self.cursor = crsr
        
class DataArea():# Класс область памяти
    
    def __init__(self, name, strt_addr, end_addr):
        self.name = name
        self.start_addr = strt_addr
        self.end_addr = end_addr
        self.DataRowsList = []
        self.stack_cursor = end_addr

    def CreateDataArea(self):
        for x in range(self.end_addr - self.start_addr):
            self.DataRowsList.append(DataRecord(addr=x))
        self.stack_cursor = len(self.DataRowsList) 
            
    def GetValByAddr(self, addr):
        for x in range(len(self.DataRowsList)):
            if self.DataRowsList[x].addr == addr:
                return self.DataRowsList[x].val
    
    def SetValByAddr(self, addr, val):
        for x in range(len(self.DataRowsList)):
            if self.DataRowsList[x].addr == addr:
                self.DataRowsList[x].val = val
    
    def GetStackView(self, field = ''):
        lst=[]
        if field != '':
            for x in range(self.end_addr - self.start_addr):
                lst.append(getattr(self.DataRowsList[x],field))
            return MyReverse(lst)
        else:
            return MyReverse(self.DataRowsList)
    
    def GetListView(self, field = ''):
        lst=[]
        if field != '':
            for x in range(len(self.DataRowsList) - self.start_addr):
                lst.append(getattr(self.DataRowsList[x],field))
            return lst
        else:
            return self.DataRowsList
    
    def SetStack(self, val1, val2):
        self.DataRowsList.append(DataRecord(addr=len(self.DataRowsList)+1, val=val1))
        self.DataRowsList.append(DataRecord(addr=len(self.DataRowsList)+1, val=val2))
        
    def GetStack(self):
        val2 = self.DataRowsList.pop()
        val1 = self.DataRowsList.pop()
        return (val1, val2)
        
    def GetTableView(self, field = ''):
        pass
    
    
        
    
class Tag:# Признаки
    
    TagList=[]
    
    def __init__(self, name, val):
        self.name=name
        self.val=val
        Tag.TagList.append(self)
        
    def GetTagByName(name):
        for x in Tag.TagList:
            if x.name == name:
                return x.val
    
    def SetTagByName(name, val):
        for x in Tag.TagList:
            if x.name == name:
                x.val = val
                return
    
    def CheckTag(val, oldval = 0, result = 0, oper = ''):
        
        for x in Tag.TagList:
            if x.name == 'C':
                if (val+result > 256 and oper=='+') or (result-val<0 and oper =='-'):
                    x.val = 1
                else:
                    x.val = 0

            if x.name =='S':
                if val > 127:
                    x.val = 1
                else:
                    x.val = 0

            elif x.name =='Z':
                if val ==0:
                    x.val = 1
                else:
                    x.val = 0

            elif x.name =='AC':
                pass

            elif x.name =='P':
                hw = [bin(x).count("1") for x in range(256)]
                if hw[val] % 2 == 0:
                    x.val = 1
                else:
                    x.val = 0

class Command:
    
    CmdList=[]
    
    def __init__(self, name, code, arg1 = 0, arg2 = 0, regname1='', regname2=''):
        self.name = name
        self.code = code
        self.arg1 = arg1
        self.arg2 = arg2
        self.regname1 = regname1
        self.regname2 = regname2
        Command.CmdList.append(self)
    
    def DoCmd(self):
        if self.name == 'MOV':
            Register.SetRegByName(self.regname1,Register.GetRegByName(self.regname2))
        elif self.name == 'MVI':
            Register.SetRegByName(self.regname1,self.regname2)
        elif self.name == 'LDAX':
            Register.SetRegByName('AF', DataArea.GetValByAddr(Register.GetRegByName(self.regname1)))
        elif self.name == 'STAX':
            DataArea.SetValByAddr(Register.GetRegByName(self.regname1),Register.GetRegByName('A'))
        elif self.name == 'LDA':
            Register.SetRegByName('AF', DataArea.GetValByAddr(self.arg1*256+self.arg2)) 
        elif self.name == 'STA':
            DataArea.SetValByAddr(self.arg1*256+self.arg2, Register.GetRegByName('A'))
        elif self.name == 'SPHL':
            Register.SetRegByName('SP',Register.GetRegByName('H'),Register.GetRegByName('L'))
        elif self.name == 'PCHL':
            Register.SetRegByName('PC',Register.GetRegByName('H'),Register.GetRegByName('L'))
        elif self.name == 'LHLD':
            Register.SetRegByName('HL',DataArea.GetValByAddr(self.arg1*256+self.arg2),DataArea.GetValByAddr(self.arg1*256+self.arg2+1))
        elif self.name == 'SHLD':
            DataArea.SetValByAddr(self.arg1*256+self.arg2, Register.GetRegByName('H'))
            DataArea.SetValByAddr(self.arg1*256+self.arg2+1, Register.GetRegByName('L'))
        elif self.name == 'LXI':
            Register.SetRegByName(self.regname1, self.arg1, self.arg2)
        elif self.name == 'XCHG':
            temp = Register.GetRegByName('HL')
            Register.SetRegByName('HL',Register.GetRegByName('D'),Register.GetRegByName('E'))
            Register.SetRegByName('DE', temp[0], temp[1])
            del temp
           
# To be continued...
        


