from stack import Stack
from treelib import Tree


class Symbol:
    """
    Class to represent a terminal or non-terminal symbol
    """

    uuid: str
    value: str
    is_terminal: bool

    def __init__(self, value, is_terminal):
        self.value = value
        self.is_terminal = is_terminal


PROD_VAZIA = []
PROD1 = [
    Symbol("function", True),
    Symbol("ID", True),
    Symbol("(", True),
    Symbol(")", True),
    Symbol("BLOCO", False),
]
PROD2 = [
    Symbol("{", True),
    Symbol("DECLARACOES_VARS", False),
    Symbol("SEQ_COMANDOS", False),
    Symbol("}", True),
]
PROD3 = [
    Symbol("DECLARACAO_VAR", False),
    Symbol("DECLARACOES_VARS", False),
]
PROD4 = PROD_VAZIA
PROD5 = [
    Symbol("TIPO", False),
    Symbol(":", True),
    Symbol("LISTA_IDS", False),
    Symbol(";", True),
]
PROD6 = [
    Symbol("int", True),
]
PROD7 = [
    Symbol("float", True),
]
PROD8 = [
    Symbol("char", True),
]
PROD9 = [
    Symbol("ID", True),
    Symbol("LISTA_IDS'", False),
]
PROD10 = [
    Symbol(",", True),
    Symbol("ID", True),
    Symbol("LISTA_IDS'", False),
]
PROD11 = PROD_VAZIA
PROD12 = [
    Symbol("COMANDO", False),
    Symbol("SEQ_COMANDOS", False),
]
PROD13 = PROD_VAZIA
PROD14 = [Symbol("CMD_ATRIB", False)]
PROD15 = [Symbol("CMD_REPET1", False)]
PROD16 = [Symbol("CMD_REPET2", False)]
PROD17 = [Symbol("CMD_SELECAO", False)]
PROD18 = [
    Symbol("ID", True),
    Symbol("=", True),
    Symbol("EXPRESSAO", False),
    Symbol(";", True),
]
PROD19 = [
    Symbol("enquanto", True),
    Symbol("(", True),
    Symbol("COND", False),
    Symbol(")", True),
    Symbol("faca", True),
    Symbol("CMD_OU_BLOCO", False),
]
PROD20 = [
    Symbol("repita", True),
    Symbol("CMD_OU_BLOCO", False),
    Symbol("ate", True),
    Symbol("(", True),
    Symbol("COND", False),
    Symbol(")", True),
]
PROD21 = [
    Symbol("se", True),
    Symbol("(", True),
    Symbol("COND", False),
    Symbol(")", True),
    Symbol("CMD_OU_BLOCO", False),
    Symbol("CMD_SELECAO'", False),
]
PROD22 = [Symbol("senao", True), Symbol("CMD_OU_BLOCO", False)]
PROD23 = PROD_VAZIA
PROD24 = [Symbol("COMANDO", False)]
PROD25 = [Symbol("BLOCO", False)]
PROD26 = [
    Symbol("EXPRESSAO", False),
    Symbol("op_rel", True),
    Symbol("EXPRESSAO", False),
]
PROD27 = [Symbol("TERMO", False), Symbol("EXPRESSAO'", False)]
PROD28 = [Symbol("+", True), Symbol("TERMO", False), Symbol("EXPRESSAO'", False)]
PROD29 = [Symbol("-", True), Symbol("TERMO", False), Symbol("EXPRESSAO'", False)]
PROD30 = PROD_VAZIA
PROD31 = [Symbol("EXPONENC", False), Symbol("TERMO'", False)]
PROD32 = [Symbol("*", True), Symbol("EXPONENC", False), Symbol("TERMO'", False)]
PROD33 = [Symbol("/", True), Symbol("EXPONENC", False), Symbol("TERMO'", False)]
PROD34 = PROD_VAZIA
PROD35 = [Symbol("FATOR", False), Symbol("EXPONENC'", False)]
PROD36 = [Symbol("^", True), Symbol("FATOR", False), Symbol("EXPONENC'", False)]
PROD37 = PROD_VAZIA
PROD38 = [Symbol("(", True), Symbol("EXPRESSAO", False), Symbol(")", True)]
PROD39 = [Symbol("CONST_CHAR", True)]
PROD40 = [Symbol("CONST_NUM", True)]
PROD41 = [Symbol("ID", True)]

table = {
    "INICIO": {
        "function": PROD1,
    },
    "BLOCO": {
        "{": PROD2,
    },
    "DECLARACOES_VARS": {
        "int": PROD3,
        "char": PROD3,
        "float": PROD3,
        "senao": PROD4,
        "enquanto": PROD4,
        "repita": PROD4,
        "ID": PROD4,
    },
    "DECLARACAO_VAR": {
        "int": PROD5,
        "char": PROD5,
        "float": PROD5,
    },
    "TIPO": {
        "int": PROD6,
        "char": PROD7,
        "float": PROD8,
    },
    "LISTA_IDS": {
        "ID": PROD9,
    },
    "LISTA_IDS'": {
        ",": PROD10,
        ";": PROD11,
    },
    "SEQ_COMANDOS": {
        "se": PROD12,
        "senao": PROD12,
        "enquanto": PROD12,
        "repita": PROD12,
        "ID": PROD12,
        "}": PROD13,
    },
    "COMANDO": {
        "ID": PROD14,
        "enquanto": PROD15,
        "repita": PROD16,
        "se": PROD17,
    },
    "CMD_ATRIB": {
        "ID": PROD18,
    },
    "CMD_REPET1": {
        "enquanto": PROD19,
    },
    "CMD_REPET2": {
        "repita": PROD20,
    },
    "CMD_SELECAO": {
        "se": PROD21,
    },
    "CMD_SELECAO'": {
        "senao": PROD22,
        "se": PROD23,
        "enquanto": PROD23,
        "repita": PROD23,
        "ID": PROD23,
    },
    "CMD_OU_BLOCO": {
        "senao": PROD24,
        "se": PROD24,
        "enquanto": PROD24,
        "repita": PROD24,
        "ID": PROD24,
        "{": PROD25,
    },
    "COND": {
        "(": PROD26,
        "ID": PROD26,
        "CONST_CHAR": PROD26,
        "CONST_NUM": PROD26,
    },
    "EXPRESSAO": {
        "(": PROD27,
        "ID": PROD27,
        "CONST_CHAR": PROD27,
        "CONST_NUM": PROD27,
    },
    "EXPRESSAO'": {
        "+": PROD28,
        "-": PROD29,
        ")": PROD30,
        "op_rel": PROD30,
        ";": PROD30,
    },
    "TERMO": {
        "(": PROD31,
        "ID": PROD31,
        "CONST_CHAR": PROD31,
        "CONST_NUM": PROD31,
    },
    "TERMO'": {
        "*": PROD32,
        "/": PROD33,
        "+": PROD34,
        "-": PROD34,
    },
    "EXPONENC": {
        "(": PROD35,
        "ID": PROD35,
        "CONST_CHAR": PROD35,
        "CONST_NUM": PROD35,
    },
    "EXPONENC'": {
        "^": PROD36,
        "*": PROD37,
        "/": PROD37,
    },
    "FATOR": {
        "(": PROD38,
        "ID": PROD41,
        "CONST_CHAR": PROD39,
        "CONST_NUM": PROD40,
    },
}


tokens = [
    "function",
    "main",
    "(",
    ")",
    "{",
    "int",
    ":",
    "x",
    ",",
    "y",
    ",",
    "z",
    ";",
    "}",
    "$",
]

DEBUG = True
COUNT = 0


def lexer():
    """Mocked lexer"""
    global COUNT
    token = tokens[COUNT]
    COUNT += 1
    return token


def parser():
    """
    Function to parse the given code and return the syntax tree
    """

    # Initial production to start the syntatic analysis
    initial_symbol = Symbol(
        value="INICIO",
        is_terminal=False,
    )

    # Creation of stack
    stack = Stack()
    stack.push(initial_symbol)

    # Creation of tree
    tree = Tree()
    node = tree.create_node(tag=initial_symbol.value)
    initial_symbol.uuid = node.identifier

    next_token = lexer()

    while stack.is_not_empty():
        # Take element at the top of the stack
        symbol = stack.peek()

        debug_print(f"Stack Top: {symbol.value} | Input token: {next_token}")

        if symbol.is_terminal:
            if symbol.value == next_token:
                debug_print("Match symbol with next token")
                popped = stack.pop()
                debug_print(f"Popped: {popped.value}")
                next_token = lexer()
            else:
                print(f"Syntax Error: unexpected token from entry ({next_token})")
                return None

        else:
            debug_print("Not terminal, searching for valid production")
            symbols = table.get(symbol.value, {}).get(next_token, None)

            if symbols is None:
                print(f"Syntax Error: unexpected token from entry ({next_token})")
                break

            popped = stack.pop()
            debug_print(f"Popped: {popped.value}")

            # Copy needed bc of reverse is a destructive method
            # and change the table by reference passing
            copied_symbols = symbols.copy()
            copied_symbols.reverse()

            # Push all symbols from production in reverse order
            # and add to tree as children of symbol
            for child_symbol in copied_symbols:
                debug_print(f"Pushing: {child_symbol.value}")
                node = tree.create_node(tag=child_symbol.value, parent=symbol.uuid)
                child_symbol.uuid = node.identifier
                stack.push(child_symbol)

    if next_token != "$":
        print(f"Syntax Error: unexpected token from entry ({next_token})")
        return None

    print("Recognized Input sequence")
    tree.show()
    return tree


# Estrutura de dados:
# Deverá representar tanto terminais quanto não-terminais


def debug_print(value: str):
    """
    A function to print if debug parameter is true
    """
    if DEBUG:
        print(value)


if __name__ == "__main__":
    parser()


# IDEIA: Criar um arquivo que conterá as variáveis globais(count de linha, coluna, etc.)
# Dessa forma, é possível colocar o analisador sintático e léxico em arquivos diferentes
# e ter uma organização melhor
