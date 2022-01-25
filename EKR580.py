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
        self.reg_list = [r_a, r_f, r_b, r_c, r_d, r_e, r_h, r_l, r_af, r_bc, r_de, r_hl, r_sp, r_pc]
                
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
        
    def push_stack(self, low_value, high_value):
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
            return (low_value, high_value)

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
        self.description = description
        
    def do(self):
        if self.reg1 == 'M':
            self.mem_obj.get_mem(self.reg_obj.get_register('HL').value).value = self.reg_obj.get_register(self.reg2).value
        elif self.reg2 =='M':
            self.reg_obj.get_register(self.reg1).value = self.mem_obj.get_mem(self.reg_obj.get_register('HL').value).value
        else:    
            self.reg_obj.get_register(self.reg1).value = self.reg_obj.get_register(self.reg2).value

class cmMVI(Command):
    
    def __init__(self, fullname, code, reg_obj, mem_obj, reg, description = ''):
        self.fullname = fullname
        self.code = code
        self.reg_obj = reg_obj
        self.mem_obj = mem_obj
        self.reg = reg
        self.description = description
        
    def do(self, value):
        if self.reg == 'M':
            self.mem_obj.get_mem(self.reg_obj.get_register('HL').value).value = value
        else:
            self.reg_obj.get_register(self.reg).value = value
        
class cmLDAX(cmMVI): 
        
    def do(self):
        self.reg_obj.get_register('A').value = self.mem_obj.get_mem(self.reg_obj.get_register(self.reg).value).value
        
class cmSTAX(cmMVI):
        
    def do(self):
        self.mem_obj.get_mem(self.reg_obj.get_register(self.reg).value).value = self.reg_obj.get_register('A').value
        
class cmLDA(cmMVI): 
        
    def do(self, high_value, low_value):
        self.reg_obj.get_register('A').value = self.mem_obj.get_mem(256 * high_value + low_value).value
        
class cmSTA(cmMVI):
        
    def do(self, high_value, low_value):
        self.mem_obj.get_mem(256 * high_value + low_value).value = self.reg_obj.get_register('A').value

class cmLXI(cmMVI):
        
    def do(self, high_value, low_value):
        self.reg_obj.get_register(self.reg).value = 256 * high_value + low_value
        
class cmLHLD(cmMVI):
        
    def do(self, high_value, low_value):
        self.reg_obj.get_register('H').value = self.mem_obj.get_mem(256 * high_value + low_value).value
        self.reg_obj.get_register('L').value = self.mem_obj.get_mem(256 * high_value + low_value + 1).value
        
#testing
m1 = Mem_Range(33280, 33300)
r1 = Registers()
r1.get_register('L').value = 100

movaa = cmMOV('MOV A, A', '7F', r1, m1, 'A', 'A')
mvia = cmMVI('MVI A N', '3E', r1, m1, 'A')

mvia.do(100)
print(r1.get_register('A').value)        

