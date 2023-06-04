import sys
from src.token import Token

BUFFER_SIZE = 512
DEBUG = False


class SymbolTableEntry:
    lexemn: str
    token_type: str
    token_attribute: int
    data_type: str

    def __init__(
        self,
        lexemn,
        token_type,
        token_attribute,
        data_type,
    ):
        self.lexemn = lexemn
        self.token_type = token_type
        self.token_attribute = token_attribute
        self.data_type = data_type


class SymbolTable:
    table: list[SymbolTableEntry]
    keywords: list[str]

    def __init__(self) -> None:
        # Estrutura pensada para a key (lexema, tipo do token, valor, tipo do dado)

        # Make a load from reserverd words
        self.table = [
            SymbolTableEntry("function", "ID", None, None),
            SymbolTableEntry("int", "ID", None, None),
            SymbolTableEntry("float", "ID", None, None),
            SymbolTableEntry("char", "ID", None, None),
            SymbolTableEntry("se", "ID", None, None),
            SymbolTableEntry("entao", "ID", None, None),
            SymbolTableEntry("senao", "ID", None, None),
            SymbolTableEntry("enquanto", "ID", None, None),
            SymbolTableEntry("faca", "ID", None, None),
            SymbolTableEntry("repita", "ID", None, None),
            SymbolTableEntry("ate", "ID", None, None),
        ]
        self.keywords = [
            "function",
            "int",
            "float",
            "char",
            "se",
            "entao",
            "senao",
            "enquanto",
            "faca",
            "repita",
            "ate",
        ]

    def append(self, lexemn: str, token_type: str, value: any, data_type: str) -> int:
        symbol_entry = SymbolTableEntry(lexemn, token_type, value, data_type)
        self.table.append(symbol_entry)
        return len(self.table) - 1

    def lookup(self, lexemn: str) -> int | None:
        for i, entry in enumerate(self.table):
            if entry.lexemn == lexemn:
                return i
        return None


class Point:
    init: int
    prox: int
    line: int
    column: int

    def __init__(self) -> None:
        self.init = -1
        self.prox = -1
        self.column = -1
        self.line = 0

    @property
    def where(self):
        return (self.line, self.column)

    @property
    def position(self):
        return (self.init, self.prox)

    def add_in_line(self):
        self.line += 1
        self.column = 0

    def add_in_column(self):
        self.column += 1

    def step_look_ahead(self):
        self.prox += 1

    def handle_look_ahead(self):
        self.prox -= 1

    def init_take_prox(self):
        self.init = self.prox - 1
        self.prox = self.init


class Buffer:
    buffer_pair: list[list]
    current_buffer: int
    vigilant: Point
    buffer_num: int

    def __init__(self, file="") -> None:
        self.buffer_pair = [[], []]
        self.current_buffer = 0
        self.buffer_num = 0
        self.vigilant = Point()
        self.load(file=file)

    def change(self) -> None:
        if self.current_buffer == 0:
            self.current_buffer = 1
        else:
            self.current_buffer = 0
        debug_print("Att Buffer")

    @property
    def next_char(self) -> str | None:
        """Retorna o próximo caracter no buffer, lidando com a troca de buffers (sentinelas)"""

        self.vigilant.step_look_ahead()
        next_char = self.buffer_pair[self.current_buffer][self.vigilant.prox]

        if next_char == "$":
            #  Pode ser sentinela padrão ou pode ser final de arquivo
            if self.vigilant.prox == BUFFER_SIZE - 1:
                # Sentinela padrão (final de buffer)
                debug_print("Change")
                raise NotImplementedError
            # else: FIM DE ARQUIVO
        return next_char

    def load(self, file: str) -> None:
        with open(file, "r", encoding="utf-8") as file_code:
            # move pointer for where to read
            file_code.seek(self.buffer_num * BUFFER_SIZE)

            buffer_ = file_code.read(BUFFER_SIZE - 1)
            buffer_ = buffer_ + "$"
            # Nao apagar linha abaixo talvez seja bom para testes
            # buffer = repr(buffer)
            debug_print(len(buffer_))
            self.buffer_pair[self.current_buffer] = buffer_

        debug_print("Buffer Loaded")

    def sync(self, handle_lookahead: bool = False) -> str:
        """
        Retorna o lexema definido pelos ponteiros 'init' e 'prox', lidando com lookahead
        se necessário, e preparando os ponteiros para continuar a análise léxica.
        """
        if handle_lookahead:
            self.vigilant.handle_look_ahead()
        token = self.buffer_pair[self.current_buffer][
            (self.vigilant.init + 1) : self.vigilant.prox
        ]
        self.vigilant.init_take_prox()
        return token

    def is_end_of_file(self) -> bool:
        return (
            self.buffer_pair[self.current_buffer][self.vigilant.prox] == "$"
            and self.vigilant.prox != 512
        )


def debug_print(value: str):
    """
    A function to print something if debug parameter is true
    """
    if DEBUG:
        print(value)


class UnexpectedTokenException(Exception):
    """
    Exception for cases of unexpected token from entry
    """

    token: Token

    def __init__(self, token: Token):
        self.token = token


buffer = Buffer(file=sys.argv[1])
symbol_table = SymbolTable()
