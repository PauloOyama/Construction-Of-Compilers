class ParseTableSymbol:
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
    ParseTableSymbol("function", True),
    ParseTableSymbol("ID", True),
    ParseTableSymbol("(", True),
    ParseTableSymbol(")", True),
    ParseTableSymbol("BLOCO", False),
]
PROD2 = [
    ParseTableSymbol("{", True),
    ParseTableSymbol("DECLARACOES_VARS", False),
    ParseTableSymbol("SEQ_COMANDOS", False),
    ParseTableSymbol("}", True),
]
PROD3 = [
    ParseTableSymbol("DECLARACAO_VAR", False),
    ParseTableSymbol("DECLARACOES_VARS", False),
]
PROD4 = PROD_VAZIA
PROD5 = [
    ParseTableSymbol("TIPO", False),
    ParseTableSymbol(":", True),
    ParseTableSymbol("LISTA_IDS", False),
    ParseTableSymbol(";", True),
]
PROD6 = [
    ParseTableSymbol("int", True),
]
PROD7 = [
    ParseTableSymbol("float", True),
]
PROD8 = [
    ParseTableSymbol("char", True),
]
PROD9 = [
    ParseTableSymbol("ID", True),
    ParseTableSymbol("LISTA_IDS'", False),
]
PROD10 = [
    ParseTableSymbol(",", True),
    ParseTableSymbol("ID", True),
    ParseTableSymbol("LISTA_IDS'", False),
]
PROD11 = PROD_VAZIA
PROD12 = [
    ParseTableSymbol("COMANDO", False),
    ParseTableSymbol("SEQ_COMANDOS", False),
]
PROD13 = PROD_VAZIA
PROD14 = [ParseTableSymbol("CMD_ATRIB", False)]
PROD15 = [ParseTableSymbol("CMD_REPET1", False)]
PROD16 = [ParseTableSymbol("CMD_REPET2", False)]
PROD17 = [ParseTableSymbol("CMD_SELECAO", False)]
PROD18 = [
    ParseTableSymbol("ID", True),
    ParseTableSymbol("=", True),
    ParseTableSymbol("EXPRESSAO", False),
    ParseTableSymbol(";", True),
]
PROD19 = [
    ParseTableSymbol("enquanto", True),
    ParseTableSymbol("(", True),
    ParseTableSymbol("COND", False),
    ParseTableSymbol(")", True),
    ParseTableSymbol("faca", True),
    ParseTableSymbol("CMD_OU_BLOCO", False),
]
PROD20 = [
    ParseTableSymbol("repita", True),
    ParseTableSymbol("CMD_OU_BLOCO", False),
    ParseTableSymbol("ate", True),
    ParseTableSymbol("(", True),
    ParseTableSymbol("COND", False),
    ParseTableSymbol(")", True),
]
PROD21 = [
    ParseTableSymbol("se", True),
    ParseTableSymbol("(", True),
    ParseTableSymbol("COND", False),
    ParseTableSymbol(")", True),
    ParseTableSymbol("CMD_OU_BLOCO", False),
    ParseTableSymbol("CMD_SELECAO'", False),
]
PROD22 = [ParseTableSymbol("senao", True), ParseTableSymbol("CMD_OU_BLOCO", False)]
PROD23 = PROD_VAZIA
PROD24 = [ParseTableSymbol("COMANDO", False)]
PROD25 = [ParseTableSymbol("BLOCO", False)]
PROD26 = [
    ParseTableSymbol("EXPRESSAO", False),
    ParseTableSymbol("op_rel", True),
    ParseTableSymbol("EXPRESSAO", False),
]
PROD27 = [ParseTableSymbol("TERMO", False), ParseTableSymbol("EXPRESSAO'", False)]
PROD28 = [
    ParseTableSymbol("+", True),
    ParseTableSymbol("TERMO", False),
    ParseTableSymbol("EXPRESSAO'", False),
]
PROD29 = [
    ParseTableSymbol("-", True),
    ParseTableSymbol("TERMO", False),
    ParseTableSymbol("EXPRESSAO'", False),
]
PROD30 = PROD_VAZIA
PROD31 = [ParseTableSymbol("EXPONENC", False), ParseTableSymbol("TERMO'", False)]
PROD32 = [
    ParseTableSymbol("*", True),
    ParseTableSymbol("EXPONENC", False),
    ParseTableSymbol("TERMO'", False),
]
PROD33 = [
    ParseTableSymbol("/", True),
    ParseTableSymbol("EXPONENC", False),
    ParseTableSymbol("TERMO'", False),
]
PROD34 = PROD_VAZIA
PROD35 = [ParseTableSymbol("FATOR", False), ParseTableSymbol("EXPONENC'", False)]
PROD36 = [
    ParseTableSymbol("^", True),
    ParseTableSymbol("FATOR", False),
    ParseTableSymbol("EXPONENC'", False),
]
PROD37 = PROD_VAZIA
PROD38 = [
    ParseTableSymbol("(", True),
    ParseTableSymbol("EXPRESSAO", False),
    ParseTableSymbol(")", True),
]
PROD39 = [ParseTableSymbol("CONST_CHAR", True)]
PROD40 = [ParseTableSymbol("CONST_NUM", True)]
PROD41 = [ParseTableSymbol("ID", True)]

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
        "ID": PROD4,
        "enquanto": PROD4,
        "repita": PROD4,
        "se": PROD4,
        "}": PROD4,
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
        "ID": PROD12,
        "enquanto": PROD12,
        "repita": PROD12,
        "se": PROD12,
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
        "ID": PROD23,
        "enquanto": PROD23,
        "repita": PROD23,
        "se": PROD23,
        "}": PROD23,
        "ate": PROD23,
    },
    "CMD_OU_BLOCO": {
        "ID": PROD24,
        "enquanto": PROD24,
        "repita": PROD24,
        "se": PROD24,
        "{": PROD25,
    },
    "COND": {
        "(": PROD26,
        "CONST_CHAR": PROD26,
        "CONST_NUM": PROD26,
        "ID": PROD26,
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
        "op_rel": PROD30,
        ")": PROD30,
        ";": PROD30,
    },
    "TERMO": {
        "(": PROD31,
        "CONST_CHAR": PROD31,
        "CONST_NUM": PROD31,
        "ID": PROD31,
    },
    "TERMO'": {
        "*": PROD32,
        "/": PROD33,
        "+": PROD34,
        "-": PROD34,
        "op_rel": PROD34,
        ")": PROD34,
        ";": PROD34,
    },
    "EXPONENC": {
        "(": PROD35,
        "CONST_CHAR": PROD35,
        "CONST_NUM": PROD35,
        "ID": PROD35,
    },
    "EXPONENC'": {
        "^": PROD36,
        "*": PROD37,
        "/": PROD37,
        "+": PROD37,
        "-": PROD37,
        "op_rel": PROD37,
        ")": PROD37,
        ";": PROD37,
    },
    "FATOR": {
        "(": PROD38,
        "CONST_CHAR": PROD39,
        "CONST_NUM": PROD40,
        "ID": PROD41,
    },
}
