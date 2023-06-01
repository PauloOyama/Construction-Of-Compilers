import string
import sys

from classes import Buffer, Point

BUFFER_SIZE = 511
RETURN_TOKEN = ()
buffer = Buffer()
ASCII_CHARS = string.ascii_uppercase + string.ascii_lowercase
ASCII_DIGITS = string.digits

# example to run : python lexer.py text.txt


def buffer_load(file: str) -> str:
    """
    Load Buffer and put guard in the last character
    """

    with open(file, "r") as file_code:
        buffer = file_code.read(BUFFER_SIZE)
        buffer = buffer + "$"
        # Nao apagar linha abaixo talvez seja bom para testes
        # buffer = repr(buffer)
        print(len(buffer))

        return buffer


# Codificao Direta
def get_token(buffer: Buffer):
    machine_state = 0
    while True:
        char = buffer.nextChar

        if machine_state == 0:
            if char == "=":
                machine_state = 1
            elif char == "/":
                machine_state = 4
            elif char == "<":
                machine_state = 9
            elif char == ">":
                machine_state = 13
            elif char in ASCII_CHARS:
                machine_state = 16
            elif char == " " or char == "\t" or char == "\n":
                machine_state = 18
            elif char == "(":
                machine_state = 20
            elif char == ")":
                machine_state = 21
            elif char == "+":
                machine_state = 22
            elif char == "-":
                machine_state = 23
            elif char == "*":
                machine_state = 24
            elif char == "^":
                machine_state = 43
            elif char == "}":
                machine_state = 25
            elif char == "{":
                machine_state = 26
            elif char == ";":
                machine_state = 27
            elif char == "'":
                machine_state = 28
            elif char in ASCII_DIGITS:
                machine_state = 31
            elif char == ",":
                machine_state = 41
            elif char == ":":
                machine_state = 42
            else:
                break  # erro

        elif machine_state == 1:
            if char == "=":
                machine_state = 2
            else:
                machine_state = 3

        elif machine_state == 2:
            return buffer.sync()

        elif machine_state == 3:
            return buffer.sync()

        elif machine_state == 4:
            if char != "*":
                machine_state = 5
            else:
                machine_state = 6

        elif machine_state == 5:
            return buffer.sync()

        elif machine_state == 6:
            if char == "*":
                machine_state = 7
            # else continue

        elif machine_state == 7:
            if char == "/":
                machine_state = 8
            else:
                break  # erro

        elif machine_state == 8:
            return buffer.sync()

        elif machine_state == 9:
            if char == "=":
                machine_state = 11
            elif char == ">":
                machine_state = 12
            else:
                machine_state = 10

        elif machine_state == 10:
            return buffer.sync()

        elif machine_state == 11:
            return buffer.sync()

        elif machine_state == 12:
            return buffer.sync()

        elif machine_state == 13:
            if char == "=":
                machine_state = 14
            else:
                machine_state = 15

        elif machine_state == 14:
            return buffer.sync()

        elif machine_state == 15:
            return buffer.sync()

        elif machine_state == 16:
            if char not in ASCII_CHARS:
                machine_state = 17
            # else continue

        elif machine_state == 17:
            return buffer.sync()

        elif machine_state == 18:
            if char not in " \t\n":
                return buffer.sync()
            # else continue

        elif machine_state == 20:
            return buffer.sync()
        elif machine_state == 21:
            return buffer.sync()
        elif machine_state == 22:
            return buffer.sync()
        elif machine_state == 23:
            return buffer.sync()
        elif machine_state == 24:
            return buffer.sync()
        elif machine_state == 25:
            return buffer.sync()
        elif machine_state == 26:
            return buffer.sync()
        elif machine_state == 27:
            return buffer.sync()
        elif machine_state == 28:
            if char != "'":
                machine_state = 29
            else:
                break  # erro

        elif machine_state == 29:
            if char == "'":
                return buffer.sync()
            else:
                break  # erro

        elif machine_state == 30:
            return buffer.sync()

        elif machine_state == 31:
            if char == ".":
                machine_state = 33
            elif char == "E":
                machine_state == 37
            elif char not in ASCII_DIGITS:
                machine_state = 32
            # else continue

        # TODO: 32, 33, 34, 35, 37, 38, 39, 40

        elif machine_state == 41:
            return buffer.sync()
        elif machine_state == 42:
            return buffer.sync()
        elif machine_state == 43:
            # vem do estado 0 após ler "^"
            # é o "segundo 24"
            return buffer.sync()
        else:
            break  # erro

    print("ERROR")


buffer.load = buffer_load(sys.argv[1])


print(get_token(buffer))
print(get_token(buffer))
print(get_token(buffer))
print(get_token(buffer))
print(get_token(buffer))
print(get_token(buffer))
# print(buffer.nextChar)
# print(buffer.nextChar)
# print(buffer.vigilant.where)
