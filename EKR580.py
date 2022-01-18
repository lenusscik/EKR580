import re
#implementaion
def MyReverse(lst):
    temp = []
    for x in range(len(lst), 0, -1):
        temp.append(x)
    return temp

def MyNegation(val):
    temp = '0b'
    for x in bin(val)[2:]:
        temp += str(1 - int(x))
    return int(temp, 2)
    
    
class Register():#Класс для описания регистровых пар
    RegList = []
    
    def __init__(self, name = '', val1 = 0, val2 = 0):
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
                return (Register.RegList[x].val1, Register.RegList[x].val2)
            
    def SetRegByName(regname, val1 = None, val2 = None):
        for x in range(len(Register.RegList)):
            if Register.RegList[x].name[0] == regname:
                Register.RegList[x].val1 = int(val1)
            elif Register.RegList[x].name[1] == regname:
                Register.RegList[x].val2 = int(val1)                        
            elif Register.RegList[x].name == regname:
                Register.RegList[x].val1 = int(val1)
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
            self.DataRowsList.append(DataRecord(addr = x))
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
        lst = []
        if field != '':
            for x in range(self.end_addr - self.start_addr):
                lst.append(getattr(self.DataRowsList[x], field))
            return MyReverse(lst)
        else:
            return MyReverse(self.DataRowsList)
    
    def GetListView(self, field = ''):
        lst = []
        if field != '':
            for x in range(len(self.DataRowsList) - self.start_addr):
                lst.append(getattr(self.DataRowsList[x], field))
            return lst
        else:
            return self.DataRowsList
    
    def SetStackVal(self, val1, val2):
        self.DataRowsList.append(DataRecord(addr = len(self.DataRowsList) + 1, val = val1))
        self.DataRowsList.append(DataRecord(addr = len(self.DataRowsList) + 1, val = val2))
        
    def GetStackVal(self):
        val2 = self.DataRowsList.pop()
        val1 = self.DataRowsList.pop()
        return (val1, val2)
        
    def GetTableView(self, field = ''):
        pass
    
class Tag:
    
    TagList = []
    
    def __init__(self, name, val):
        self.name = name
        self.val = val
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
    
    def GetTagRegister():
        s = Tag.GetTagByName('S')
        z = Tag.GetTagByName('Z')
        ac = Tag.GetTagByName('AC')
        p = Tag.GetTagByName('P')
        c = Tag.GetTagByName('C')
        return int("0b{}{}0{}0{}1{}".format(s, z, ac, p, c),2)
        
    def SetTagRegister(val):
        st = '0b' + bin(val)[2:].zfill(8)
        Tag.SetTagByName('S', int(st[2]))
        Tag.SetTagByName('Z', int(st[3]))
        Tag.SetTagByName('AC', int(st[5]))
        Tag.SetTagByName('P', int(st[7]))
        Tag.SetTagByName('C', int(st[9]))
    
    def CheckTag(val):# обнаружение изменения флагов можно сделать вызовом целеом обьекте
        
        for x in Tag.TagList:
            if x.name == 'C':
                if val > 256 or val < 0 :
                    x.val = 1
                else:
                    x.val = 0

            if x.name == 'S':
                if val > 127:
                    x.val = 1
                else:
                    x.val = 0

            elif x.name == 'Z':
                if val == 0:
                    x.val = 1
                else:
                    x.val = 0

            elif x.name == 'AC':
                pass

            elif x.name == 'P':
                hw = [bin(x).count("1") for x in range(256)]
                if hw[val] % 2 == 0:
                    x.val = 1
                else:
                    x.val = 0

class Command:
    
    CmdList = []
    
    def __init__(self, name, code, arg1 = 0, arg2 = 0, regnm1 = '', regnm2 = '', tagnm = ''):
        self.name = name
        self.code = code
        self.arg1 = arg1
        self.arg2 = arg2
        self.regname1 = regnm1
        self.regname2 = regnm2
        self.tagname = tagnm
        Command.CmdList.append(self)
    
    def ExecCmd(self):
        if self.name == 'MOV':# пересылка из регистра в регистр
            Register.SetRegByName(self.regname1, Register.GetRegByName(self.regname2))
        elif self.name == 'MVI':# загрузка  второго байта команды в регистр R
            Register.SetRegByName(self.regname1, self.arg1)
        elif self.name == 'LDAX':# пересылка из ячейки памяти, адрес которой записан в  регистровой паре ВС (DE), в аккумулятор
            temp = Register.GetRegByName(self.regname1)
            Register.SetRegByName('A', DataArea.GetValByAddr(temp[0] * 256 + temp[1]))
            del temp
        elif self.name == 'STAX':# пересылка из аккумулятора в ячейку памяти, адрес которой записан в регистровой паре BC (DE)
            DataArea.SetValByAddr(Register.GetRegByName(self.regname1), Register.GetRegByName('A'))
        elif self.name == 'LDA':# пересылка из ячейки памяти, адрес  которой записан во втором и третьем байтах команды, в аккумулятор
            Register.SetRegByName('A', DataArea.GetValByAddr(self.arg1 * 256 + self.arg2)) 
        elif self.name == 'STA':# пересылка из аккумулятора в ячейку памяти, адрес которой указан во втором и третьем байтах команды
            DataArea.SetValByAddr(self.arg1*256+self.arg2, Register.GetRegByName('A'))
        elif self.name == 'SPHL':# пересылка данных из регистровой пары HL в указатель стека
            temp = Register.GetRegByName('HL')
            Register.SetRegByName('SP',temp[0],temp[1])
        elif self.name == 'PCHL':# пересылка данных из регистровой пары HL в счетчик команд
            Register.SetRegByName('PC',temp[0],temp[1])
        elif self.name == 'LHLD':# пересылка данных из ячеек памяти с адресами, записанным во втором и третьем байтах команды и на единицу большем, в регистровую пару HL
            Register.SetRegByName('HL',DataArea.GetValByAddr(self.arg1*256+self.arg2),DataArea.GetValByAddr(self.arg1*256+self.arg2+1))
        elif self.name == 'SHLD':# пересылка данных из регистровой пары HL в ячейки памяти с адресами, записанными во втором и третьем байтах команды и на единицу большем
            temp = Register.GetRegByName('HL')
            DataArea.SetValByAddr(self.arg1 * 256 + self.arg2, temp[0])
            DataArea.SetValByAddr(self.arg1*256 + self.arg2+1, temp[1])
        elif self.name == 'LXI':# загрузка второго и третьего байтов команды в регистровую пару BС (DЕ,HL)
            Register.SetRegByName(self.regname1, self.arg1, self.arg2)
        elif self.name == 'XCHG':# обмен данными между парами регистров HL и DE
            temp = Register.GetRegByName('HL')
            Register.SetRegByName('HL', Register.GetRegByName('D'), Register.GetRegByName('E'))
            Register.SetRegByName('DE', temp[0], temp[1])
            del temp
        elif self.name == 'XTHL':# обмен данными между парой регистров HL и вершиной стека (L) <-> [УC], (H) <-> [УC+1]
            tempSt = DataArea.GetStackVal() 
            tempRg = Register.GetRegByName('HL')
            Register.SetRegByName('HL', tempSt[0], tempSt[1])
            DataArea.SetStackVal(tempRg[1])
            DataArea.SetStackVal(tempRg[0])
            del tempSt, tempRg
        elif self.name == 'ADD':# сложение содержимого аккумулятора с содержимым регистра R
            Register.SetRegByName('A', Register.GetRegByName('A') + Register.GetRegByName(self.regname1))
        elif self.name == 'ADI':# сложение содержимого аккумулятора со вторым байтом команды
            Register.SetRegByName('A', Register.GetRegByName('A') + self.arg1)
        elif self.name == 'ADC':# сложение содержимого аккумулятора с содержимым регистра R и признаком (С)
            Register.SetRegByName('A', Register.GetRegByName('A') + Register.GetRegByName(self.regname1) + Tag.GetTagByName('C'))
        elif self.name == 'ACI':# сложение содержимого аккумулятора со вторым байтом команды и признаком (С)
            Register.SetRegByName('A', Register.GetRegByName('A') + self.arg1 + Tag.GetTagByName('C'))
        elif self.name == 'DAD':# сложение содержимого пары регистров HL с содержимым пары регистров BC (DE или HL  или указателем стека) и запись результата в пару HL
            temp = Register.GetRegByName(self.regname1)
            tempRg = Register.GetRegByName('HL') 
            Register.SetRegByName('HL', temp[0] + tempRg[0], temp[1] + tempRg[1])
            del temp, tempRg
        elif self.name == 'SUB':# вычитание из содержимого  аккумулятора содержимого регистра R
            Register.SetRegByName('A', Register.GetRegByName('A') - Register.GetRegByName(self.regname1))
        elif self.name == 'SUI':# вычитание из содержимого аккумулятора  второго байта команды
            Register.SetRegByName('A', Register.GetRegByName('A') - self.arg1)
        elif self.name == 'SBB':# вычитание из содержимого аккумулятора содержимого регистра R и признака (С)
            Register.SetRegByName('A', Register.GetRegByName('A') - Register.GetRegByName(self.regname1) - Tag.GetTagByName('C'))
        elif self.name == 'SBI':# вычитание из содержимого аккумулятора второго байта команды и признака (С)
            Register.SetRegByName('A', Register.GetRegByName('A') - self.arg1 + Tag.GetTagByName('C'))
        elif self.name == 'INR':# увеличение   содержимого  регистра на 1
            Register.SetRegByName(self.regname1, Register.GetRegByName(self.regname1) + 1)
        elif self.name == 'INX':# увеличение содержимого пары регистров BC (DE), (HL), (SP) на 1
            Register.SetRegByName(self.regname1, Register.GetRegByName(self.regname1) + 1)
        elif self.name == 'DCR':# уменьшение содержимого регистра R на 1
            Register.SetRegByName(self.regname1, Register.GetRegByName(self.regname1) - 1)
        elif self.name == 'DCX':# уменьшение содержимого пары регистров BC  (DE), (HL), (SP) на 1 
            Register.SetRegByName(self.regname1, Register.GetRegByName(self.regname1) - 1)
        elif self.name == 'ANA':# операция “И” между содержимым аккумулятора и содержимым регистра
            Register.SetRegByName('A', Register.GetRegByName('A') & Register.GetRegByName(self.regname1))
        elif self.name == 'ANI':# операция “И” между содержимым аккумулятора и вторым байтом команды
            Register.SetRegByName('A', Register.GetRegByName('A') & self.arg1)
        elif self.name == 'ORA':# операция “ИЛИ” между содержимым аккумулятора и содержимым регистра R
            Register.SetRegByName('A', Register.GetRegByName('A') | Register.GetRegByName(self.regname1))
        elif self.name == 'ORI':# операция  “ИЛИ” между содержимым аккумулятора и вторым байтом команды
            Register.SetRegByName('A', Register.GetRegByName('A') | self.arg1)
        elif self.name == 'XRA':# операция “ИЛИ-НЕ” между содержимым аккумулятора и содержимым регистра R
            Register.SetRegByName('A', Register.GetRegByName('A') ^ Register.GetRegByName(self.regname1))
        elif self.name == 'XRI':# операция  “ИЛИ-НЕ” между содержимым аккумулятора и вторым байтом команды
            Register.SetRegByName('A', Register.GetRegByName('A') ^ self.arg1)
        elif self.name == 'CMP':# операция  (A) – (R); если (A) = (R), то Z = 1; если (А) <(R), то С=1
            a = Register.GetRegByName('A')
            temp = a - Register.GetRegByName(self.regname1)
            if temp < 0:
                Teg.SetTagByName('C', 1)
            elif temp == a:
                Teg.SetTagByName('Z', 1)
            del temp
        elif self.name == 'CPI':# операция  (А) – B2; если (A) = B2, то Z = 1; если (A)< B2, то С=1
            a = Register.GetRegByName('A')
            temp = a - self.arg1
            if temp < 0:
                Teg.SetTagByName('C', 1)
            elif temp == a:
                Teg.SetTagByName('Z', 1)
            del temp
        elif self.name == 'RLC':# сдвиг влево (каждый бит сдвигается на один разряд влево, а 7 бит переносится в 0 и одновременно записывается в признак (С))
            st = re.split('', bin(r)[2:])[1:-1]
            Tag.SetTagByName('C', st[0])
            st += '0b' + st.append(st.pop(0))
            Register.SetRegByName('A', int(st,2))
            
print("".join(st))
        elif self.name == 'RRC':# сдвиг вправо (каждый бит сдвигается на один разряд вправо, а 0 бит переносится в 7 и одновременно записывается в признак (С))
            pass
        elif self.name == 'RAL':# сдвиг влево через перенос (каждый бит сдвигается на один разряд влево, 7 бит записывается в признак (С), а бит из (С) записывается в 0 бит)
            pass
        elif self.name == 'RAR':# сдвиг вправо через перенос (каждый бит сдвигается на один разряд вправо, 0 бит записывается в признак (С), а бит из (С) записывается в 7 бит)
            pass
#перейти по адресу, записанному во втором и третьем байтах команды,иначе перейти к следующей команде
        elif self.name == 'JMP':
            Register.SetRegByName('PC', self.arg1, self.arg2)
        elif self.name == 'JNC':# если признак c = 0
            if Tag.GetTagByName('C') == 0:
                Register.SetRegByName('PC', self.arg1, self.arg2)
            else:
                temp = Register.GetRegByName('PC') + 3
                Register.SetRegByName('PC', temp[0], temp[1])
                del temp
        elif self.name == 'JC':# если признак c = 1
            if Tag.GetTagByName('C') == 1:
                Register.SetRegByName('PC', self.arg1, self.arg2)
            else:
                temp = Register.GetRegByName('PC') + 3
                Register.SetRegByName('PC', temp[0], temp[1])
                del temp
        elif self.name == 'JNZ':# если признак z = 0
            if Tag.GetTagByName('Z') == 0:
                Register.SetRegByName('PC', self.arg1, self.arg2)
            else:
                temp = Register.GetRegByName('PC') + 3
                Register.SetRegByName('PC', temp[0], temp[1])
                del temp
        elif self.name == 'JZ':# если признак z = 1
            if Tag.GetTagByName('Z') == 1:
                Register.SetRegByName('PC', self.arg1, self.arg2)
            else:
                temp = Register.GetRegByName('PC') + 3
                Register.SetRegByName('PC', temp[0], temp[1])
                del temp
        elif self.name == 'JPO':# если признак p = 0
            if Tag.GetTagByName('P') == 0:
                Register.SetRegByName('PC', self.arg1, self.arg2)
            else:
                temp = Register.GetRegByName('PC') + 3
                Register.SetRegByName('PC', temp[0], temp[1])
                del temp
        elif self.name == 'JPE':# если признак p = 1
            if Tag.GetTagByName('P') == 1:
                Register.SetRegByName('PC', self.arg1, self.arg2)
            else:
                temp = Register.GetRegByName('PC') + 3
                Register.SetRegByName('PC', temp[0], temp[1])
                del temp
        elif self.name == 'JP':# если признак s = 0
            if Tag.GetTagByName('S') == 0:
                Register.SetRegByName('PC', self.arg1, self.arg2)
            else:
                temp = Register.GetRegByName('PC') + 3
                Register.SetRegByName('PC', temp[0], temp[1])
                del temp
        elif self.name == 'JM':# если признак s = 1
            if Tag.GetTagByName('S') == 1:
                Register.SetRegByName('PC', self.arg1, self.arg2)
            else:
                temp = Register.GetRegByName('PC') + 3
                Register.SetRegByName('PC', temp[0], temp[1])
                del temp
        elif self.name == 'PUSH':
            if self.regname1 == 'PSW':
                DataArea.SetStackVal(Register.GetRegByName("A"), Tag.GetTagRegister())
            else:
                DataArea.SetStackVal(Register.GetRegByName(self.regname1[0]), Register.GetRegByName(self.regname1[1]))
        elif self.name == 'POP':
            temp =  DataArea.GetStackVal()
            if self.regname1 == 'PSW':
                Register.SetRegByName('A', temp[1])
                Tag.SetTagRegister(temp[0])
            else:
                Register.SetRegByName(self.regname[0], temp[1])
                Register.SetRegByName(self.regname[1], temp[0])
            del temp
        elif self.name == 'CMA':#
            Register.SetRegByName('A', MyNegation(Register.GetRegByName('A')))
        elif self.name == 'CMC':#
            Tag.SetTagByName('C', 1-Tag.GetTagByName('C'))
        elif self.name == 'STC':#
            Tag.SetTagByName('C', 1)
        elif self.name == 'NOP':#
            pass
        elif self.name == 'HLT':#
            pass
        elif self.name == '':
            pass
        elif self.name == '':
            pass
        elif self.name == '':
            pass
        elif self.name == '':
            pass
        elif self.name == '':
            pass
        

#Testing

tag_s = Tag('S', 0)
tag_z = Tag('Z', 0)
tag_ac = Tag('AC', 0)
tag_p = Tag('P', 0)
tag_c = Tag('C', 0)
                
reg_af = Register(name = 'AF', val2 = Tag.TagList)
reg_bc = Register(name = 'BC')
reg_de = Register(name = 'DE')
reg_hl = Register(name = 'HL')
reg_pc = Register(name = 'PC')
reg_sp = Register(name = 'SP')


area1 = DataArea('area1', 0, 10)
area1.CreateDataArea()

'''
Register.RegList[0].val2[1].val = 1
Register.GetRegByName('F')[1].val = 1
Tag.TagList[1].val = 1
reg_af.val2[1].val = 1
tag_c.val = 1'''

c = 0
r = 21

st = re.split('', bin(r)[2:])[1:-1]
print(st)
t, c = st[0], st[0]
st.append(st.pop(0))
print("".join(st))


