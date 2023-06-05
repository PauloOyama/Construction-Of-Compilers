import string

from src import token as tk
from src.classes import Buffer, buffer, debug_print, symbol_table

ASCII_CHARS = string.ascii_uppercase + string.ascii_lowercase
ASCII_DIGITS = string.digits


class LexerError(Exception):
    """Errors on Lexer"""

    position: tuple[int, int]

    def __init__(self, position: tuple[int, int]) -> None:
        self.position = position


# example to run : python lexer.py text.txt


def relop_token(op_code: int) -> tk.Token:
    return tk.Token("op_rel", op_code)


def common_symbol(symbol: str) -> tk.Token:
    return tk.Token(symbol, None)


def set_id(identifier: str) -> tk.Token:
    position = symbol_table.lookup(identifier)
    if position is None:
        position = symbol_table.append(identifier, "ID", None, None)
    return tk.Token("ID", position)


def set_char(character: str) -> tk.Token:
    position = symbol_table.lookup(character)
    if position is None:
        position = symbol_table.append(
            lexemn=character, token_type="CONST_CHAR", value=character, data_type="char"
        )
    return tk.Token("CONST_CHAR", position)


def set_int(integer: str) -> tk.Token:
    position = symbol_table.lookup(integer)
    if position is None:
        position = symbol_table.append(
            lexemn=integer, token_type="CONST_NUM", value=integer, data_type="int"
        )
    return tk.Token("CONST_NUM", position)


def set_frac(fractional_nbr: str) -> tk.Token:
    position = symbol_table.lookup(fractional_nbr)
    if position is None:
        position = symbol_table.append(
            lexemn=fractional_nbr,
            token_type="CONST_NUM",
            value=fractional_nbr,
            data_type="float",
        )
    return tk.Token("CONST_NUM", position)


def set_exp(exp: str) -> tk.Token:
    position = symbol_table.lookup(exp)
    if position is None:
        position = symbol_table.append(
            lexemn=exp,
            token_type="CONST_NUM",
            value=exp,
            data_type="float",
        )
    return tk.Token("CONST_NUM", position)


# Codificao Direta
def get_token(buffer: Buffer) -> tuple[tk.Token, tuple[int, int]] | None:
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
                location = buffer.scan_point.location
                buffer.sync()
                return relop_token(tk.RELOP_EQ), location

            case 3:
                location = buffer.scan_point.location
                return common_symbol(buffer.sync(handle_lookahead=True)), location

            case 4:
                if char != "*":
                    machine_state = 5
                else:
                    machine_state = 6

            case 5:
                location = buffer.scan_point.location
                return common_symbol(buffer.sync(handle_lookahead=True)), location

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
                location = buffer.scan_point.location
                buffer.sync(handle_lookahead=True)
                return relop_token(tk.RELOP_LT), location

            case 11:
                location = buffer.scan_point.location
                buffer.sync()
                return relop_token(tk.RELOP_LE), location

            case 12:
                location = buffer.scan_point.location
                buffer.sync()
                return relop_token(tk.RELOP_NE), location

            case 13:
                if char == "=":
                    machine_state = 14
                else:
                    machine_state = 15

            case 14:
                location = buffer.scan_point.location
                buffer.sync()
                return relop_token(tk.RELOP_GE), location

            case 15:
                location = buffer.scan_point.location
                buffer.sync(handle_lookahead=True)
                return relop_token(tk.RELOP_GT), location

            case 16:
                if char not in ASCII_CHARS:
                    machine_state = 17
                # else continue

            case 17:
                location = buffer.scan_point.location
                return set_id(buffer.sync(handle_lookahead=True)), location

            case 18:
                if char not in " \t\n":
                    machine_state = 19
                # else continue

            case 19:
                buffer.sync(handle_lookahead=True)
                machine_state = 0  # reinicia a funcao pra ignorar comentários
            case 20:
                location = buffer.scan_point.location
                return common_symbol(buffer.sync()), location
            case 21:
                location = buffer.scan_point.location
                return common_symbol(buffer.sync()), location
            case 22:
                location = buffer.scan_point.location
                return common_symbol(buffer.sync()), location
            case 23:
                location = buffer.scan_point.location
                return common_symbol(buffer.sync()), location
            case 24:
                location = buffer.scan_point.location
                return common_symbol(buffer.sync()), location
            case 25:
                location = buffer.scan_point.location
                return common_symbol(buffer.sync()), location
            case 26:
                location = buffer.scan_point.location
                return common_symbol(buffer.sync()), location
            case 27:
                location = buffer.scan_point.location
                return common_symbol(buffer.sync()), location

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
                location = buffer.scan_point.location
                return set_char(buffer.sync()), location

            case 31:
                if char == ".":
                    machine_state = 33
                elif char == "E":
                    machine_state = 37
                elif char not in ASCII_DIGITS:
                    machine_state = 32
                # else continue

            case 32:
                location = buffer.scan_point.location
                return set_int(buffer.sync(handle_lookahead=True)), location

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
                location = buffer.scan_point.location
                return set_frac(buffer.sync(handle_lookahead=True)), location

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
                location = buffer.scan_point.location
                return set_exp(buffer.sync(handle_lookahead=True)), location
            case 41:
                location = buffer.scan_point.location
                return common_symbol(buffer.sync()), location
            case 42:
                location = buffer.scan_point.location
                return common_symbol(buffer.sync()), location

            case 99:
                # vem do estado 0 após ler "^"
                # é o "segundo 24"
                location = buffer.scan_point.location
                return common_symbol(buffer.sync()), location

            case _:
                break  # erro

    if machine_state == 0 and char == "$":
        # Final de Arquivo
        return None
    raise LexerError(buffer.scan_point.location)


if __name__ == "__main__":
    i = 0
    while True:
        token = get_token(buffer)
        if token is None:
            break
        debug_print(i, repr(token))
        i += 1
