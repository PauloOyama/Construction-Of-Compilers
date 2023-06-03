import string
import sys

from src import token as tk
from src.classes import Buffer, Point

ASCII_CHARS = string.ascii_uppercase + string.ascii_lowercase
ASCII_DIGITS = string.digits


# example to run : python lexer.py text.txt

# TODO: rever as ações do autômato na especificação


def relop_token(op_code: int) -> tk.Token:
    return tk.Token("op_rel", op_code)


def common_symbol(symbol: str) -> tk.Token:
    return tk.Token(symbol, None)


def set_id(identifier: str) -> tk.Token:
    # TODO: lógica da tabela de símbolos
    return tk.Token("ID", -1)


def set_char(character: str) -> tk.Token:
    # TODO: lógica da tabela de símbolos
    return tk.Token("CONST_CHAR", -1)


def set_int(integer: str) -> tk.Token:
    # TODO: lógica da tabela de símbolos
    return tk.Token("CONST_NUM", -1)


def set_frac(fractional_nbr: str) -> tk.Token:
    # TODO: lógica da tabela de símbolos
    return tk.Token("CONST_NUM", -1)


def set_exp(exp: str) -> tk.Token:
    # TODO: lógica da tabela de símbolos
    return tk.Token("CONST_NUM", -1)


# Codificao Direta
def get_token(buffer: Buffer) -> tk.Token | None:
    """
    Função principal no lexer. Retorna o próximo token lido no arquivo.
    Caso seja final do arquivo, retorna None.
    """
    machine_state = 0

    char = ""
    while True:
        char = buffer.next_char
        # print("MACHINE STATE =", machine_state, "; CHAR =", repr(char))

        match machine_state:
            case 0:
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
                elif char in (" ", "\t", "\n"):
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
                    machine_state = 99
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

            case 1:
                if char == "=":
                    machine_state = 2
                else:
                    machine_state = 3

            case 2:
                buffer.sync()
                return relop_token(tk.RELOP_EQ)

            case 3:
                return common_symbol(buffer.sync(handle_lookahead=True))

            case 4:
                if char != "*":
                    machine_state = 5
                else:
                    machine_state = 6

            case 5:
                return common_symbol(buffer.sync(handle_lookahead=True))

            case 6:
                if char == "*":
                    machine_state = 7
                # else continue

            case 7:
                if char == "/":
                    machine_state = 8
                else:
                    break  # erro

            case 8:
                buffer.sync()
                machine_state = 0  # reinicia a funcao pra ignorar comentários

            case 9:
                if char == "=":
                    machine_state = 11
                elif char == ">":
                    machine_state = 12
                else:
                    machine_state = 10

            case 10:
                buffer.sync(handle_lookahead=True)
                return relop_token(tk.RELOP_LT)

            case 11:
                buffer.sync()
                return relop_token(tk.RELOP_LE)

            case 12:
                buffer.sync()
                return relop_token(tk.RELOP_NE)

            case 13:
                if char == "=":
                    machine_state = 14
                else:
                    machine_state = 15

            case 14:
                buffer.sync()
                return relop_token(tk.RELOP_GE)

            case 15:
                buffer.sync(handle_lookahead=True)
                return relop_token(tk.RELOP_GT)

            case 16:
                if char not in ASCII_CHARS:
                    machine_state = 17
                # else continue

            case 17:
                return set_id(buffer.sync(handle_lookahead=True))

            case 18:
                if char not in " \t\n":
                    machine_state = 19
                # else continue

            case 19:
                buffer.sync(handle_lookahead=True)
                machine_state = 0  # reinicia a funcao pra ignorar comentários
            case 20:
                return common_symbol(buffer.sync())
            case 21:
                return common_symbol(buffer.sync())
            case 22:
                return common_symbol(buffer.sync())
            case 23:
                return common_symbol(buffer.sync())
            case 24:
                return common_symbol(buffer.sync())
            case 25:
                return common_symbol(buffer.sync())
            case 26:
                return common_symbol(buffer.sync())
            case 27:
                return common_symbol(buffer.sync())

            case 28:
                if char != "'":
                    machine_state = 29
                else:
                    break  # erro

            case 29:
                if char == "'":
                    machine_state = 30
                else:
                    break  # erro

            case 30:
                return set_char(buffer.sync())

            case 31:
                if char == ".":
                    machine_state = 33
                elif char == "E":
                    machine_state = 37
                elif char not in ASCII_DIGITS:
                    machine_state = 32
                # else continue

            case 32:
                return set_int(buffer.sync(handle_lookahead=True))

            case 33:
                if char in ASCII_DIGITS:
                    machine_state = 34
                else:
                    break  # erro

            case 34:
                if char == "E":
                    machine_state = 37
                elif char in ASCII_DIGITS:
                    continue
                elif char != ".":
                    machine_state = 35
                else:
                    break  # erro

            case 35:
                return set_frac(buffer.sync(handle_lookahead=True))

            case 37:
                if char in "+-":
                    machine_state = 38
                elif char in ASCII_DIGITS:
                    machine_state = 39
                else:
                    break  # erro

            case 38:
                if char in ASCII_DIGITS:
                    machine_state = 39
                else:
                    break  # erro

            case 39:
                if char not in (ASCII_DIGITS + "." + "E"):
                    machine_state = 40
                else:
                    break  # erro

            case 40:
                return set_exp(buffer.sync(handle_lookahead=True))
            case 41:
                return common_symbol(buffer.sync())
            case 42:
                return common_symbol(buffer.sync())

            case 99:
                # vem do estado 0 após ler "^"
                # é o "segundo 24"
                return common_symbol(buffer.sync())

            case _:
                break  # erro

    if machine_state == 0 and char == "$":
        return None
    raise Exception("Lexer Error")


def main():
    buffer_ = Buffer(file=sys.argv[1])

    i = 0
    while True:
        token = get_token(buffer_)
        if token is None:
            print("EOF")
            return None
        print(i, repr(token))
        i += 1


if __name__ == "__main__":
    main()
