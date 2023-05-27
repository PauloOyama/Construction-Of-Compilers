import sys
import string
from classes import Point, Buffer

BUFFER_SIZE = 511
RETURN_TOKEN = ()
buffer = Buffer()
ASCII_CHARS = string.ascii_uppercase + string.ascii_lowercase

#example to run : python lexer.py text.txt

def buffer_load(file:str) -> str:
    """
        Load Buffer and put guard in the last character
    """
    
    with open(file,'r') as file_code:

        buffer = file_code.read(BUFFER_SIZE)
        buffer = buffer + '$'
        #Nao apagar linha abaixo talvez seja bom para testes
        # buff = repr(buff)
        print(len(buffer))

        return buffer

buffer.load = buffer_load(sys.argv[1])
# print(buffer.nextChar)
# print(buffer.nextChar)
# print(buffer.vigilant.where)


#Codificao Direta
MACHINE_STATE = 0
while True:
    c = buffer.nextChar

    if MACHINE_STATE == 0: 
        if c in ASCII_CHARS:
            MACHINE_STATE = 16
        else:
            pass
    elif MACHINE_STATE == 1:
        pass
    elif MACHINE_STATE == 4:
        pass
    elif MACHINE_STATE == 9:
        pass
    elif MACHINE_STATE == 13:
        pass
    elif MACHINE_STATE == 16:
        if c not in ASCII_CHARS:
            pass
        else:
            pass
    elif MACHINE_STATE == 18:
        pass
    elif MACHINE_STATE == 20:
        pass
    elif MACHINE_STATE == 21:
        pass
    elif MACHINE_STATE == 22:
        pass
    elif MACHINE_STATE == 23:
        pass
    elif MACHINE_STATE == 24:
        pass
    elif MACHINE_STATE == 25:
        pass
    elif MACHINE_STATE == 26:
        pass
    elif MACHINE_STATE == 27:
        pass
    elif MACHINE_STATE == 28:
        pass
    elif MACHINE_STATE == 31:
        pass
    elif MACHINE_STATE == 41:
        pass
    elif MACHINE_STATE == 42:
        pass
    
    break

    





