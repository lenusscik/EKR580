#Эмулятор ассемблера попытка 5
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

def int_to_hex(value):
    return hex(value)[2:].upper()

def hex_to_int(value):
    return int(value, 16)

hw = [bin(num).count("1") for num in range(256)]

#Обьявление классов

class Abstract_Flag:
    
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Flag_Z(Abstract_Flag):
    
    def check(self, value):
        if value == 0:
            self.value = 1
        else:
            self.value = 0        
        
class Flag_C(Abstract_Flag):
    
    def check(self, value):
        if value > 256 or value < 0 :
            self.value = 1
        else:
            self.value = 0

class Flag_P(Abstract_Flag):
    
    def check(self, value):

        if hw[value] % 2 == 0:
            self.value = 1
        else:
            self.value = 0       
        
class Flag_S(Abstract_Flag):
    
    def check(self, value):
        if value > 127:
            self.value = 1
        else:
            self.value = 0
            
class Flag_AC(Abstract_Flag):
    
    def check(self, value):
        pass
            
class Flag_Register:
    
    def __init__(self, name):
        self.name = name
        self.s = Flag_S('S', 0)
        self.z = Flag_Z('Z', 0)
        self.ac = Flag_AC('AC', 0)
        self.p = Flag_P('P', 0)
        self.c = Flag_C('C', 0)
    
    @property
    def value(self):
        return int("0b{}{}0{}0{}1{}".format(self.s.value, self.z.value, self.ac.value, self.p.value, self.c.value), 2)
    
    @value.setter
    def value(self, value):
        st = bin(value).zfill(8)
        self.s.value = int(st[2])
        self.z.value = int(st[3])
        self.ac.value = int(st[5])
        self.p.value = int(st[7])
        self.c.value = int(st[9])

class Register_8:
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
    
class Register_2x8:
    
    def __init__(self, high_register, low_register):
        self.name = high_register.name + low_register.name
        self.low_register = low_register
        self.high_register = high_register
    
    @property
    def low_register_value(self):
        return self.low_register.value
    
    @low_register_value.setter
    def low_register_value(self, value):
        self.low_register.value = value
        
    @property
    def high_register_value(self):
        return self.high_register.value
    
    @high_register_value.setter
    def high_register_value(self, value):
        self.high_register.value = value
        
    @property
    def value(self):
        return 256 * self.high_register_value + self.low_register_value
    
    @value.setter
    def value(self, value):
        self.high_register_value = value // 256
        self.low_register_value = value - self.high_register_value * 256
        

class Register_16:
    
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Registers:
    
    def __init__(self):
        r_a = Register_8('A', 0)
        r_f = Flag_Register('F')
        r_b = Register_8('B', 0)
        r_c = Register_8('C', 0)
        r_d = Register_8('D', 0)
        r_e = Register_8('E', 0)
        r_h = Register_8('H', 0)
        r_l = Register_8('L', 0)
        r_af = Register_2x8(r_a, r_f)
        r_bc = Register_2x8(r_b, r_c)
        r_de = Register_2x8(r_d, r_e)
        r_hl = Register_2x8(r_h, r_l)
        r_sp = Register_16('SP', 0)
        r_pc = Register_16('PC', 0)
        self.reg_list = {'A': r_a, 'F': r_f, 'B': r_b, 'C': r_c, 
                         'D': r_d, 'E': r_e, 'H': r_h, 'L': r_l, 
                         'AF': r_af, 'BC': r_bc, 'DE': r_de, 
                         'HL': r_hl, 'SP': r_sp, 'PC': r_pc}
                
    def get_register(self, name):
        for element in self.reg_list:
            if element.name == name:
                return element


class Mem_Cell: #класс ячейка памяти - вид строки адрес, значение, команда, флаг точки останова
    
    def __init__(self, index = 0, value = 0, comand = None, breakpoint = False):
        self.index = index
        self.value = value
        self.comand = comand
        self.breakpoint = breakpoint

class Mem_Range:
    
    def __init__(self, initial_address, final_address):
        self.mem_list = []
        self.prefix = initial_address
        for idx in range(0, final_address - initial_address+1):
            self.mem_list.append(Mem_Cell(idx))
        self.stack_range = MyReverse(self.mem_list)
        self.initial_address = initial_address
        self.final_address = final_address
        self.command_pointer = 0
        self.stack_pointer = -1
    
    def extend_mem_range(self, initial_address, final_address):
        pass
    
    def reduce_mem_range(self, initial_address, final_address):
        pass
    
    def get_mem(self, address):
        return self.mem_list[address-self.prefix]
    
    def show_mem(self, attribute = ''):
        lst = []
        if attribute != '':
            for idx in range(len(self.mem_list)):
                lst.append(getattr(self.mem_list[idx], attribute))
            return lst
        
    def push_stack(self, high_value, low_value):
        for idx in range(self.stack_pointer, -1, 2):
            self.mem_list[idx - 1].value = self.mem_list[idx + 1].value
            self.mem_list[idx].value = self.mem_list[idx + 2].value
        self.mem_list[-2].value = high_value 
        self.mem_list[-1].value = low_value
        self.stack_pointer -= 2
        pass
    
    def pop_stack(self):
        if self.stack_pointer < -1:
            low_value = self.mem_list[-1].value
            high_value = self.mem_list[-2].value
            for idx in range(-3, self.stack_pointer, -2):
                self.mem_list[idx + 2].value = self.mem_list[idx].value
                self.mem_list[idx + 1].value = self.mem_list[idx - 1].value
                self.mem_list[idx].value = 0
                self.mem_list[idx - 1].value = 0
            if self.stack_pointer == -3:
                self.mem_list[-1].value = 0
                self.mem_list[-2].value = 0
            self.stack_pointer += 2    
            return (high_value, low_value)

#Классы команд
class Command:
    pass

class cmMOV(Command):
    
    def __init__(self, fullname, code, reg_obj, mem_obj, reg1, reg2, description = ''):
        self.fullname = fullname
        self.code = code
        self.reg_obj = reg_obj
        self.mem_obj = mem_obj
        self.reg1 = reg1
        self.reg2 = reg2
        self.arg_num = 0
        self.description = description
        
    def do(self):
        if self.reg1 == 'M':
            self.mem_obj.get_mem(self.reg_obj.reg_list['HL'].value).value = self.reg_obj.reg_list[self.reg2].value
        elif self.reg2 =='M':
            self.reg_obj.reg_list[self.reg1].value = self.mem_obj.get_mem(self.reg_obj.reg_list['HL'].value).value
        else:
            self.reg_obj.reg_list[self.reg1].value = self.reg_obj.reg_list[self.reg2].value

class cmMVI(Command):
    
    def __init__(self, fullname, code, reg_obj, mem_obj, reg = '', arg = 0, description = ''):
        self.fullname = fullname
        self.code = code
        self.reg_obj = reg_obj
        self.mem_obj = mem_obj
        self.reg = reg
        self.arg_num = arg 
        self.description = description
        
    def do(self, value):
        if self.reg == 'M':
            self.mem_obj.get_mem(self.reg_obj.reg_list['HL'].value).value = value
        else:
            self.reg_obj.reg_list[self.reg].value = value
        
class cmLDAX(cmMVI):         
    def do(self):
        self.reg_obj.reg_list['A'].value = self.mem_obj.get_mem(self.reg_obj.reg_list[self.reg].value).value
        
class cmSTAX(cmMVI):        
    def do(self):
        self.mem_obj.get_mem(self.reg_obj.reg_list[self.reg].value).value = self.reg_obj.reg_list['A'].value
        
class cmLDA(cmMVI):         
    def do(self, high_value, low_value):
        self.reg_obj.reg_list['A'].value = self.mem_obj.get_mem(256 * high_value + low_value).value
        
class cmSTA(cmMVI):        
    def do(self, high_value, low_value):
        self.mem_obj.get_mem(256 * high_value + low_value).value = self.reg_obj.reg_list['A'].value

class cmLXI(cmMVI):        
    def do(self, high_value, low_value):
        self.reg_obj.reg_list[self.reg].value = 256 * high_value + low_value
        
class cmLHLD(cmMVI):        
    def do(self, high_value, low_value):
        self.reg_obj.reg_list['H'].value = self.mem_obj.get_mem(256 * high_value + low_value).value
        self.reg_obj.reg_list['L'].value = self.mem_obj.get_mem(256 * high_value + low_value + 1).value

class cmSHLD(cmMVI):       
    def do(self, high_value, low_value):
        self.mem_obj.get_mem(256 * high_value + low_value).value = self.reg_obj.reg_list['H'].value
        self.mem_obj.get_mem(256 * high_value + low_value + 1).value = self.reg_obj.reg_list['L'].value

class cmSPHL(cmMVI):        
    def do(self):
        self.reg_obj.reg_list['SP'].value = self.reg_obj.reg_list['HL'].value

class cmPCHL(cmMVI):        
    def do(self):
        self.reg_obj.reg_list['PC'].value = self.reg_obj.reg_list['HL'].value
        
class cmXCHG(cmMVI):        
    def do(self):
        temp = self.reg_obj.reg_list['DE'].value
        self.reg_obj.reg_list['DE'].value = self.reg_obj.reg_list['HL'].value
        self.reg_obj.reg_list['HL'].value = temp
        
class cmXTHL(cmMVI):        
    def do(self):
        temp = self.mem_obj.pop_stack()
        self.mem_obj.pop_stack(self.reg_obj.reg_list['H'].value, self.reg_obj.reg_list['L'].value)
        self.reg_obj.reg_list['H'].value = temp[0]
        self.reg_obj.reg_list['L'].value = temp[1]
        
class cmADD(cmMVI):        
    def do(self, value = None):
        if self.reg == 'M':
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value + self.mem_obj.get_mem(self.reg_obj.reg_list['HL'].value).value
        elif value != None:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value + value
        else:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value + self.reg_obj.reg_list[self.reg].value

class cmADC(cmMVI):        
    def do(self, value = None):
        if self.reg == 'M':
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value + self.mem_obj.get_mem(self.reg_obj.reg_list['HL'].value).value + self.reg_obj.reg_list['F'].c.value
        elif value != None:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value + value + self.reg_obj.reg_list['F'].c.value
        else:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value + self.reg_obj.reg_list[self.reg].value + self.reg_obj.reg_list['F'].c.value

class cmSUB(cmMVI):        
    def do(self, value = None):
        if self.reg == 'M':
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value - self.mem_obj.get_mem(self.reg_obj.reg_list['HL'].value).value
        elif value != None:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value - value
        else:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value - self.reg_obj.reg_list[self.reg].value

class cmSBB(cmMVI):        
    def do(self, value = None):
        if self.reg == 'M':
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value - self.mem_obj.get_mem(self.reg_obj.reg_list['HL'].value).value - self.reg_obj.reg_list['F'].c.value
        elif value != None:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value - value - self.reg_obj.reg_list['F'].c.value
        else:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value - self.reg_obj.reg_list[self.reg].value - self.reg_obj.reg_list['F'].c.value            

class cmDAD(cmMVI):        
    def do(self):
        self.reg_obj.reg_list['HL'].value = self.reg_obj.reg_list['HL'].value + self.reg_obj.reg_list[self.reg].value

class cmINR(cmMVI):        
    def do(self):
        self.reg_obj.reg_list[self.reg].value = self.reg_obj.reg_list[self.reg].value + 1
        
class cmDCR(cmMVI):        
    def do(self):
        self.reg_obj.reg_list[self.reg].value = self.reg_obj.reg_list[self.reg].value - 1
        
class cmANA(cmMVI):        
    def do(self, value = None):
        if value != None:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value & value
        else:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value & self.reg_obj.reg_list[self.reg].value

class cmORA(cmMVI):        
    def do(self, value = None):
        if value != None:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value | value
        else:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value | self.reg_obj.reg_list[self.reg].value
            
class cmXRA(cmMVI):        
    def do(self, value = None):
        if value != None:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value ^ value
        else:
            self.reg_obj.reg_list['A'].value = self.reg_obj.reg_list['A'].value ^ self.reg_obj.reg_list[self.reg].value

class cmCMP(cmMVI):        
    def do(self, value = None):
        if value != None:
            temp = self.reg_obj.reg_list['A'].value - value
        else:
            temp = self.reg_obj.reg_list['A'].value - self.reg_obj.reg_list[self.reg].value
            print('temp'+ str(temp)
        if temp == 0:
            self.reg_obj.reg_list['F'].z.value = 1
        elif temp < 0:
            self.reg_obj.reg_list['F'].c.value = 1
            
class cmRLC(cmMVI):        
    def do(self):
        st = re.split('', bin(self.reg_obj.reg_list['A'].value)[2:])[1:-1]
        self.reg_obj.reg_list['F'].c.value = int(st[0])
        st.append(st.pop(0))
        st.insert(0, '0b')
        self.reg_obj.reg_list['A'].value = int("".join(st), 2)                       

class cmRRC(cmMVI):        
    def do(self):
        st = re.split('', bin(self.reg_obj.reg_list['A'].value)[2:])[1:-1]
        self.reg_obj.reg_list['F'].c.value = int(st[-1])
        st.insert(0, st[-1])
        st.insert(0, '0b')
        st.pop()
        self.reg_obj.reg_list['A'].value = int("".join(st), 2)                      

class cmRAL(cmMVI):        
    def do(self):
        st = re.split('', bin(self.reg_obj.reg_list['A'].value)[2:])[1:-1]
        st.append(str(self.reg_obj.reg_list['F'].c.value))
        self.reg_obj.reg_list['F'].c.value = int(st[0])
        st.pop(0)
        st.insert(0, '0b')
        self.reg_obj.reg_list['A'].value = int("".join(st), 2)
                      
class cmRAR(cmMVI):        
    def do(self):
        st = re.split('', bin(self.reg_obj.reg_list['A'].value)[2:])[1:-1]
        st.insert(0, str(self.reg_obj.reg_list['F'].c.value))
        self.reg_obj.reg_list['F'].c.value = int(st[-1])
        st.pop()
        st.insert(0, '0b')
        self.reg_obj.reg_list['A'].value = int("".join(st), 2)
                      
class cmJMP(cmMVI):       
    def do(self, high_value, low_value):
        if self.reg == '':
            self.reg_obj.reg_list['PC'].value = 256 * high_value + low_value
        elif self.reg == 'c':
            if self.reg_obj.reg_list['F'].c.value == 1:
                self.reg_obj.reg_list['PC'].value = 256 * high_value + low_value
            else:
                self.reg_obj.reg_list['PC'].value = self.reg_obj.reg_list['PC'].value + 1
        elif self.reg == 'nc':
            if self.reg_obj.reg_list['F'].c.value == 0:
                self.reg_obj.reg_list['PC'].value = 256 * high_value + low_value
            else:
                self.reg_obj.reg_list['PC'].value = self.reg_obj.reg_list['PC'].value + 1
        elif self.reg == 'z':
            if self.reg_obj.reg_list['F'].z.value == 1:
                self.reg_obj.reg_list['PC'].value = 256 * high_value + low_value
            else:
                self.reg_obj.reg_list['PC'].value = self.reg_obj.reg_list['PC'].value + 1
        elif self.reg == 'nz':
            if self.reg_obj.reg_list['F'].z.value == 0:
                self.reg_obj.reg_list['PC'].value = 256 * high_value + low_value
            else:
                self.reg_obj.reg_list['PC'].value = self.reg_obj.reg_list['PC'].value + 1 
        elif self.reg == 'm':
            if self.reg_obj.reg_list['F'].s.value == 1:
                self.reg_obj.reg_list['PC'].value = 256 * high_value + low_value
            else:
                self.reg_obj.reg_list['PC'].value = self.reg_obj.reg_list['PC'].value + 1
        elif self.reg == 'p':
            if self.reg_obj.reg_list['F'].s.value == 0:
                self.reg_obj.reg_list['PC'].value = 256 * high_value + low_value
            else:
                self.reg_obj.reg_list['PC'].value = self.reg_obj.reg_list['PC'].value + 1              
        elif self.reg == 'pe':
            if self.reg_obj.reg_list['F'].p.value == 1:
                self.reg_obj.reg_list['PC'].value = 256 * high_value + low_value
            else:
                self.reg_obj.reg_list['PC'].value = self.reg_obj.reg_list['PC'].value + 1
        elif self.reg == 'po':
            if self.reg_obj.reg_list['F'].p.value == 0:
                self.reg_obj.reg_list['PC'].value = 256 * high_value + low_value
            else:
                self.reg_obj.reg_list['PC'].value = self.reg_obj.reg_list['PC'].value + 1                            
                      
class cmPOP(cmMVI):       
    def do(self):
        temp = self.mem_obj.pop_stack()
        self.reg_obj.reg_list[self.reg].value = 256 * temp[0] + temp[1]             

class cmPUSH(cmMVI):       
    def do(self):
        self.mem_obj.push_stack(self.reg_obj.reg_list[self.reg].high_value, self.reg_obj.reg_list[self.reg].low_value)

class cmCMC(cmMVI):
    def do(self):
        self.reg_obj.reg_list['F'].c.value = 1 - self.reg_obj.reg_list['F'].c.value
        
class cmCMA(cmMVI):
    def do(self):
        self.reg_obj.reg_list['A'].value = MyNegation(self.reg_obj.reg_list['A'].value)
        
class cmSTC(cmMVI):
    def do(self):
        self.reg_obj.reg_list['F'].c.value = 1

class cmdDict:
    
    def __init__(self, reg_obj, mem_obj):
        self.reg = reg_obj
        self.mem = mem_obj
        self.dct = {'40':cmMOV('MOV B, B', '40', self.reg, self.mem, 'B', 'B'),                  
                  '41':cmMOV('MOV B, C', '41', self.reg, self.mem, 'B', 'C'),
                  '42':cmMOV('MOV B, D', '42', self.reg, self.mem, 'B', 'D'),
                  '43':cmMOV('MOV B, E', '43', self.reg, self.mem, 'B', 'E'),
                  '44':cmMOV('MOV B, H', '44', self.reg, self.mem, 'B', 'H'),
                  '45':cmMOV('MOV B, L', '45', self.reg, self.mem, 'B', 'L'),
                  '46':cmMOV('MOV B, M', '46', self.reg, self.mem, 'B', 'M'),
                  '47':cmMOV('MOV B, A', '47', self.reg, self.mem, 'B', 'A'),
                  '48':cmMOV('MOV C, B', '48', self.reg, self.mem, 'C', 'B'),
                  '49':cmMOV('MOV C, C', '49', self.reg, self.mem, 'C', 'C'),
                  '4A':cmMOV('MOV C, D', '4A', self.reg, self.mem, 'C', 'D'),
                  '4B':cmMOV('MOV C, E', '4B', self.reg, self.mem, 'C', 'E'),
                  '4C':cmMOV('MOV C, H', '4C', self.reg, self.mem, 'C', 'H'),
                  '4D':cmMOV('MOV C, L', '4D', self.reg, self.mem, 'C', 'L'),
                  '4E':cmMOV('MOV C, M', '4E', self.reg, self.mem, 'C', 'M'),
                  '4F':cmMOV('MOV C, A', '4F', self.reg, self.mem, 'C', 'A'),
                  '50':cmMOV('MOV D, B', '50', self.reg, self.mem, 'D', 'B'),
                  '51':cmMOV('MOV D, C', '51', self.reg, self.mem, 'D', 'C'),
                  '52':cmMOV('MOV D, D', '52', self.reg, self.mem, 'D', 'D'),
                  '53':cmMOV('MOV D, E', '53', self.reg, self.mem, 'D', 'E'),
                  '54':cmMOV('MOV D, H', '54', self.reg, self.mem, 'D', 'H'),
                  '55':cmMOV('MOV D, L', '55', self.reg, self.mem, 'D', 'L'),
                  '56':cmMOV('MOV D, M', '56', self.reg, self.mem, 'D', 'M'),
                  '57':cmMOV('MOV D, A', '57', self.reg, self.mem, 'D', 'A'),
                  '58':cmMOV('MOV E, B', '58', self.reg, self.mem, 'E', 'B'),
                  '59':cmMOV('MOV E, C', '59', self.reg, self.mem, 'E', 'C'),
                  '5A':cmMOV('MOV E, D', '5A', self.reg, self.mem, 'E', 'D'),
                  '5B':cmMOV('MOV E, E', '5B', self.reg, self.mem, 'E', 'E'),
                  '5C':cmMOV('MOV E, H', '5C', self.reg, self.mem, 'E', 'H'),
                  '5D':cmMOV('MOV E, L', '5D', self.reg, self.mem, 'E', 'L'),
                  '5E':cmMOV('MOV E, M', '5E', self.reg, self.mem, 'E', 'M'),
                  '5F':cmMOV('MOV E, A', '5F', self.reg, self.mem, 'E', 'A'),
                  '60':cmMOV('MOV H, B', '60', self.reg, self.mem, 'H', 'B'),
                  '61':cmMOV('MOV H, C', '61', self.reg, self.mem, 'H', 'C'),
                  '62':cmMOV('MOV H, D', '62', self.reg, self.mem, 'H', 'D'),
                  '63':cmMOV('MOV H, E', '63', self.reg, self.mem, 'H', 'E'),
                  '64':cmMOV('MOV H, H', '64', self.reg, self.mem, 'H', 'H'),
                  '65':cmMOV('MOV H, L', '65', self.reg, self.mem, 'H', 'L'),
                  '66':cmMOV('MOV H, M', '66', self.reg, self.mem, 'H', 'M'),
                  '67':cmMOV('MOV H, A', '67', self.reg, self.mem, 'H', 'A'),
                  '68':cmMOV('MOV L, B', '68', self.reg, self.mem, 'L', 'B'),
                  '69':cmMOV('MOV L, C', '69', self.reg, self.mem, 'L', 'C'),
                  '6A':cmMOV('MOV L, D', '6A', self.reg, self.mem, 'L', 'D'),
                  '6B':cmMOV('MOV L, E', '6B', self.reg, self.mem, 'L', 'E'),
                  '6C':cmMOV('MOV L, H', '6C', self.reg, self.mem, 'L', 'H'),
                  '6D':cmMOV('MOV L, L', '6D', self.reg, self.mem, 'L', 'L'),
                  '6E':cmMOV('MOV L, M', '6E', self.reg, self.mem, 'L', 'M'),
                  '6F':cmMOV('MOV L, A', '6F', self.reg, self.mem, 'L', 'A'),
                  '70':cmMOV('MOV M, B', '70', self.reg, self.mem, 'M', 'B'),
                  '71':cmMOV('MOV M, C', '71', self.reg, self.mem, 'M', 'C'),
                  '72':cmMOV('MOV M, D', '72', self.reg, self.mem, 'M', 'D'),
                  '73':cmMOV('MOV M, E', '73', self.reg, self.mem, 'M', 'E'),
                  '74':cmMOV('MOV M, H', '74', self.reg, self.mem, 'M', 'H'),
                  '75':cmMOV('MOV M, L', '75', self.reg, self.mem, 'M', 'L'),
                  '76':cmMOV('MOV M, M', '76', self.reg, self.mem, 'M', 'M'),
                  '77':cmMOV('MOV M, A', '77', self.reg, self.mem, 'M', 'A'),
                  '78':cmMOV('MOV A, B', '78', self.reg, self.mem, 'A', 'B'),
                  '79':cmMOV('MOV A, C', '79', self.reg, self.mem, 'A', 'C'),
                  '7A':cmMOV('MOV A, D', '7A', self.reg, self.mem, 'A', 'D'),
                  '7B':cmMOV('MOV A, E', '7B', self.reg, self.mem, 'A', 'E'),
                  '7C':cmMOV('MOV A, H', '7C', self.reg, self.mem, 'A', 'H'),
                  '7D':cmMOV('MOV A, L', '7D', self.reg, self.mem, 'A', 'L'),
                  '7E':cmMOV('MOV A, M', '7E', self.reg, self.mem, 'A', 'M'),
                  '7F':cmMOV('MOV A, A', '7F', self.reg, self.mem, 'A', 'A'),
                  '80':cmADD('ADD B', '80', self.reg, self.mem, 'B'),
                  '81':cmADD('ADD C', '81', self.reg, self.mem, 'C'),
                  '82':cmADD('ADD D', '82', self.reg, self.mem, 'D'),
                  '83':cmADD('ADD E', '83', self.reg, self.mem, 'E'),
                  '84':cmADD('ADD H', '84', self.reg, self.mem, 'H'),
                  '85':cmADD('ADD L', '85', self.reg, self.mem, 'L'),
                  '86':cmADD('ADD M', '86', self.reg, self.mem, 'M'),
                  '87':cmADD('ADD A', '87', self.reg, self.mem, 'A'),
                  '88':cmADC('ADC B', '88', self.reg, self.mem, 'B'),
                  '89':cmADC('ADC C', '89', self.reg, self.mem, 'C'),
                  '8A':cmADC('ADC D', '8A', self.reg, self.mem, 'D'),
                  '8B':cmADC('ADC E', '8B', self.reg, self.mem, 'E'),
                  '8C':cmADC('ADC H', '8C', self.reg, self.mem, 'H'),
                  '8D':cmADC('ADC L', '8D', self.reg, self.mem, 'L'),
                  '8E':cmADC('ADC M', '8E', self.reg, self.mem, 'M'),
                  '8F':cmADC('ADC A', '8F', self.reg, self.mem, 'A'),
                  '90':cmSUB('SUB B', '90', self.reg, self.mem, 'B'),
                  '91':cmSUB('SUB C', '91', self.reg, self.mem, 'C'),
                  '92':cmSUB('SUB D', '92', self.reg, self.mem, 'D'),
                  '93':cmSUB('SUB E', '93', self.reg, self.mem, 'E'),
                  '94':cmSUB('SUB H', '94', self.reg, self.mem, 'H'),
                  '95':cmSUB('SUB L', '95', self.reg, self.mem, 'L'),
                  '96':cmSUB('SUB M', '96', self.reg, self.mem, 'M'),
                  '97':cmSUB('SUB A', '97', self.reg, self.mem, 'A'),
                  '98':cmSBB('SBB B', '98', self.reg, self.mem, 'B'),
                  '99':cmSBB('SBB C', '99', self.reg, self.mem, 'C'),
                  '9A':cmSBB('SBB D', '9A', self.reg, self.mem, 'D'),
                  '9B':cmSBB('SBB E', '9B', self.reg, self.mem, 'E'),
                  '9C':cmSBB('SBB H', '9C', self.reg, self.mem, 'H'),
                  '9D':cmSBB('SBB L', '9D', self.reg, self.mem, 'L'),
                  '9E':cmSBB('SBB M', '9E', self.reg, self.mem, 'M'),
                  '9F':cmSBB('SBB A', '9F', self.reg, self.mem, 'A'),
                  'A0':cmANA('ANA B', 'A0', self.reg, self.mem, 'B'),
                  'A1':cmANA('ANA C', 'A1', self.reg, self.mem, 'C'),
                  'A2':cmANA('ANA D', 'A2', self.reg, self.mem, 'D'),
                  'A3':cmANA('ANA E', 'A3', self.reg, self.mem, 'E'),
                  'A4':cmANA('ANA H', 'A4', self.reg, self.mem, 'H'),
                  'A5':cmANA('ANA L', 'A5', self.reg, self.mem, 'L'),
                  'A6':cmANA('ANA M', 'A6', self.reg, self.mem, 'M'),
                  'A7':cmANA('ANA A', 'A7', self.reg, self.mem, 'A'),
                  'A8':cmXRA('XRA B', 'A8', self.reg, self.mem, 'B'),
                  'A9':cmXRA('XRA C', 'A9', self.reg, self.mem, 'C'),
                  'AA':cmXRA('XRA D', 'AA', self.reg, self.mem, 'D'),
                  'AB':cmXRA('XRA E', 'AB', self.reg, self.mem, 'E'),
                  'AC':cmXRA('XRA H', 'AC', self.reg, self.mem, 'H'),
                  'AD':cmXRA('XRA L', 'AD', self.reg, self.mem, 'L'),
                  'AE':cmXRA('XRA M', 'AE', self.reg, self.mem, 'M'),
                  'AF':cmXRA('XRA A', 'AF', self.reg, self.mem, 'A'),
                  'B0':cmORA('ORA B', 'B0', self.reg, self.mem, 'B'),
                  'B1':cmORA('ORA C', 'B1', self.reg, self.mem, 'C'),
                  'B2':cmORA('ORA D', 'B2', self.reg, self.mem, 'D'),
                  'B3':cmORA('ORA E', 'B3', self.reg, self.mem, 'E'),
                  'B4':cmORA('ORA H', 'B4', self.reg, self.mem, 'H'),
                  'B5':cmORA('ORA L', 'B5', self.reg, self.mem, 'L'),
                  'B6':cmORA('ORA M', 'B6', self.reg, self.mem, 'M'),
                  'B7':cmORA('ORA A', 'B7', self.reg, self.mem, 'A'),
                  'B8':cmCMP('CMP B', 'B8', self.reg, self.mem, 'B'),
                  'B9':cmCMP('CMP C', 'B9', self.reg, self.mem, 'C'),
                  'BA':cmCMP('CMP D', 'BA', self.reg, self.mem, 'D'),
                  'BB':cmCMP('CMP E', 'BB', self.reg, self.mem, 'E'),
                  'BC':cmCMP('CMP H', 'BC', self.reg, self.mem, 'H'),
                  'BD':cmCMP('CMP L', 'BD', self.reg, self.mem, 'L'),
                  'BE':cmCMP('CMP M', 'BE', self.reg, self.mem, 'M'),
                  'BF':cmCMP('CMP A', 'BF', self.reg, self.mem, 'A'),
                  '01':cmLXI('LXI B', '01', self.reg, self.mem, 'BC'),
                  '11':cmLXI('LXI D', '11', self.reg, self.mem, 'DE'),
                  '21':cmLXI('LXI H', '21', self.reg, self.mem, 'HL'),
                  '31':cmLXI('LXI SP', '31', self.reg, self.mem, 'SP'),
                  '02':cmSTAX('STAX B', '02', self.reg, self.mem, 'BC'),
                  '12':cmSTAX('STAX D', '12', self.reg, self.mem, 'DE'),
                  '22':cmSHLD('SHLD', '22', self.reg, self.mem, '', 2),
                  '32':cmSTA('STA NN', '32', self.reg, self.mem, '', 2),
                  '03':cmINR('INX B', '03', self.reg, self.mem, 'BC'),
                  '13':cmINR('INX D', '13', self.reg, self.mem, 'DE',),
                  '23':cmINR('INX H', '23', self.reg, self.mem, 'HL',),
                  '33':cmINR('INX SP', '33', self.reg, self.mem, 'SP'),
                  '04':cmINR('INR B', '04', self.reg, self.mem, 'B'),
                  '14':cmINR('INR D', '14', self.reg, self.mem, 'D'),
                  '24':cmINR('INR H', '24', self.reg, self.mem, 'H'),
                  '34':cmINR('INR M', '34', self.reg, self.mem, 'M'),
                  '05':cmDCR('DCR B', '05', self.reg, self.mem, 'B'),
                  '15':cmDCR('DCR D', '15', self.reg, self.mem, 'D'),
                  '25':cmDCR('DCR H', '25', self.reg, self.mem, 'H'),
                  '35':cmDCR('DCR M', '35', self.reg, self.mem, 'M'),
                  '06':cmMVI('MVI B', '06', self.reg, self.mem, 'B', 1),
                  '16':cmMVI('MVI D', '16', self.reg, self.mem, 'D', 1),
                  '26':cmMVI('MVI H', '26', self.reg, self.mem, 'H', 1),
                  '36':cmMVI('MVI M', '36', self.reg, self.mem, 'M', 1),
                  '07':cmRLC('RLC', '07', self.reg, self.mem),
                  '17':cmRAL('RAL', '17', self.reg, self.mem),
                  '37':cmSTC('STC', '37', self.reg, self.mem),
                  '09':cmDAD('DAD B', '09', self.reg, self.mem, 'BC'),
                  '19':cmDAD('DAD D', '19', self.reg, self.mem, 'DE'),
                  '29':cmDAD('DAD H', '29', self.reg, self.mem, 'HL'),
                  '39':cmDAD('DAD SP', '39', self.reg, self.mem, 'SP'),
                  '0A':cmLDAX('LDAX B', '0A', self.reg, self.mem, 'BC'),
                  '1A':cmLDAX('LDAX D', '1A', self.reg, self.mem, 'DE'),
                  '2A':cmLHLD('LHLD', '2A', self.reg, self.mem, '', 2),
                  '3A':cmLDA('LDA NN', '3A', self.reg, self.mem, '', 2),
                  '0B':cmDCR('DCX B', '0B', self.reg, self.mem, 'BC'),
                  '1B':cmDCR('DCX D', '1B', self.reg, self.mem, 'DE'),
                  '2B':cmDCR('DCX H', '2B', self.reg, self.mem, 'HL'),
                  '3B':cmDCR('DCX SP', '3B', self.reg, self.mem, 'SP'),
                  '0C':cmINR('INR C', '0C', self.reg, self.mem, 'C'),
                  '1C':cmINR('INR E', '1C', self.reg, self.mem, 'E'),
                  '2C':cmINR('INR L', '2C', self.reg, self.mem, 'L'),
                  '3C':cmINR('INR A', '3C', self.reg, self.mem, 'A'),
                  '0D':cmDCR('DCR C', '0D', self.reg, self.mem, 'C'),
                  '1D':cmDCR('DCR E', '1D', self.reg, self.mem, 'E'),
                  '2D':cmDCR('DCR L', '2D', self.reg, self.mem, 'L'),
                  '3D':cmDCR('DCR A', '3D', self.reg, self.mem, 'A'),
                  '0E':cmMVI('MVI C', '0E', self.reg, self.mem, 'C', 1),
                  '1E':cmMVI('MVI E', '1E', self.reg, self.mem, 'E', 1),
                  '2E':cmMVI('MVI L', '2E', self.reg, self.mem, 'L', 1),
                  '3E':cmMVI('MVI A', '3E', self.reg, self.mem, 'A', 1),
                  '0F':cmRRC('RRC', '0F', self.reg, self.mem),
                  '1F':cmRAR('RAR', '1F', self.reg, self.mem),
                  '2F':cmCMA('CMA', '2F', self.reg, self.mem),
                  '3F':cmCMC('CMC', '3F', self.reg, self.mem),
                  'C1':cmPOP('POP B', 'C1', self.reg, self.mem, 'BC'),
                  'D1':cmPOP('POP D', 'D1', self.reg, self.mem, 'DE'),
                  'E1':cmPOP('POP H', 'E1', self.reg, self.mem, 'HL'),
                  'F1':cmPOP('POP PSW', 'F1', self.reg, self.mem, 'AF'),
                  'C2':cmJMP('JNZ NN', 'C2', self.reg, self.mem, 'nz', 2),
                  'D2':cmJMP('JNC NN', 'D2', self.reg, self.mem, 'nc', 2),
                  'E2':cmJMP('JPO NN', 'E2', self.reg, self.mem, 'po', 2),
                  'F2':cmJMP('JP NN', 'F2', self.reg, self.mem, 'p', 2),
                  'C3':cmJMP('JMP NN', 'C3', self.reg, self.mem, '', 2),
                  'E3':cmXTHL('XTHL', 'E3', self.reg, self.mem),
                  'C5':cmPUSH('PUSH B', 'C5', self.reg, self.mem, 'BC'),
                  'D5':cmPUSH('PUSH D', 'E5', self.reg, self.mem, 'DE'),
                  'E5':cmPUSH('PUSH H', 'E5', self.reg, self.mem, 'HL'),
                  'F5':cmPUSH('PUSH PSW', 'F5', self.reg, self.mem, 'AF'),
                  'C6':cmADD('ADI N', 'C6', self.reg, self.mem, '', 1),
                  'D6':cmSUB('SUI N', 'D6', self.reg, self.mem, '', 1),
                  'E6':cmANA('ANI N', 'E6', self.reg, self.mem, '', 1),
                  'F6':cmORA('ORI N', 'F6', self.reg, self.mem, '', 1),
                  'E9':cmPCHL('PCHL', 'E9', self.reg, self.mem),
                  'F9':cmSPHL('SPHL', 'F9', self.reg, self.mem),
                  'CA':cmJMP('JZ NN', 'CA', self.reg, self.mem, 'z', 2),
                  'DA':cmJMP('JC NN', 'DA', self.reg, self.mem, 'c', 2),
                  'EA':cmJMP('JPE NN', 'EA', self.reg, self.mem, 'pe', 2),
                  'FA':cmJMP('JM NN', 'FA', self.reg, self.mem, 'm', 2),
                  'EB':cmXCHG('XCHG', 'EB', self.reg, self.mem),
                  'CE':cmADC('ACI N', 'CE', self.reg, self.mem, '', 1),
                  'DE':cmSBB('SBI N', 'DE', self.reg, self.mem, '', 1),
                  'EE':cmXRA('XRI N', 'EE', self.reg, self.mem, '', 1),
                  'FE':cmCMP('CPI N', 'FE', self.reg, self.mem, '', 1),              
        }
    
