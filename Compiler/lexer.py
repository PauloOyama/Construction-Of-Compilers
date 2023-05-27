import sys
import string
from classes import Point, Buffer

BUFFER_SIZE = 511
RETURN_TOKEN = ()
buffer = Buffer()
ASCII_CHARS = string.ascii_uppercase + string.ascii_lowercase
ASCII_DIGITS = string.digits

#example to run : python lexer.py text.txt

def buffer_load(file:str) -> str:
    """
        Load Buffer and put guard in the last character
    """
    
    with open(file,'r') as file_code:

        buffer = file_code.read(BUFFER_SIZE)
        buffer = buffer + '$'
        #Nao apagar linha abaixo talvez seja bom para testes
        # buffer = repr(buffer)
        print(len(buffer))

        return buffer

#Codificao Direta
def getToken(buffer: Buffer):

    MACHINE_STATE = 0
    while True:
        c = buffer.nextChar

        if MACHINE_STATE == 0: 
            if c == '=':
                MACHINE_STATE = 1
            elif c == '/':
                MACHINE_STATE = 4
            elif c == '<':
                MACHINE_STATE = 9
            elif c == '>':
                MACHINE_STATE = 13
            elif c in ASCII_CHARS: 
                MACHINE_STATE = 16
            elif c == " " or c == "\t" or c == "\n":
                MACHINE_STATE = 18
            elif c == '(':
                MACHINE_STATE = 20
            elif c == ')':
                MACHINE_STATE = 21
            elif c == '+':
                MACHINE_STATE = 22
            elif c == '-':
                MACHINE_STATE = 23
            elif c == '*':
                MACHINE_STATE = 24
            elif c == '^':
                MACHINE_STATE = 43
            elif c == '}':
                MACHINE_STATE = 25
            elif c == '{':
                MACHINE_STATE = 26
            elif c == ';':
                MACHINE_STATE = 27
            elif c == 'seila':
                MACHINE_STATE = 28
            elif c in ASCII_DIGITS:
                MACHINE_STATE = 31
            elif c == ',':
                MACHINE_STATE = 41
            elif c == ':':
                MACHINE_STATE = 42



        elif MACHINE_STATE == 1:
            if c == '=': 
                MACHINE_STATE = 2
            else:
                MACHINE_STATE = 3


        elif MACHINE_STATE == 2:
            return buffer.sync()
        
        elif MACHINE_STATE == 3:
            return buffer.sync()

        elif MACHINE_STATE == 4:
            if c != '*':
                MACHINE_STATE = 5
            else:
                MACHINE_STATE = 6

        elif MACHINE_STATE == 5:
            return buffer.sync()

        elif MACHINE_STATE == 6:
            if c == '*':
                MACHINE_STATE = 7

        elif MACHINE_STATE == 7:
            if c == '/':
                MACHINE_STATE = 8

        elif MACHINE_STATE == 8:
            return buffer.sync()

        elif MACHINE_STATE == 9:
            pass

        elif MACHINE_STATE == 13:
            pass

        elif MACHINE_STATE == 16:
            if c not in ASCII_CHARS:
                return buffer.sync()
            
        elif MACHINE_STATE == 18:
            if c != " " and c != "\t" and c != "\n":
                return buffer.sync()
            
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
        
    # break

    

buffer.load = buffer_load(sys.argv[1])


print(getToken(buffer))
print(getToken(buffer))
print(getToken(buffer))
print(getToken(buffer))
print(getToken(buffer))
print(getToken(buffer))
# print(buffer.nextChar)
# print(buffer.nextChar)
# print(buffer.vigilant.where)




