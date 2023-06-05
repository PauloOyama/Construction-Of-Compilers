import sys

from src.token import Token

BUFFER_SIZE = 8192
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

    def __repr__(self) -> str:
        return f"SymbolTableEntry({self.lexemn}, {self.token_type}, {self.token_attribute}, {self.data_type})"


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
        self.column = 1
        self.line = 1

    @property
    def location(self):
        return (self.line, self.column)

    def update_location(self, lexem: str):
        lex_lines = lexem.split("\n")
        self.line += max(len(lex_lines) - 1, 0)
        if len(lex_lines) > 1:
            self.column = 1
        self.column += len(lex_lines[-1])

    @property
    def position(self):
        return (self.init, self.prox)

    def step_look_ahead(self):
        self.prox += 1

    def handle_look_ahead(self):
        self.prox -= 1

    def init_take_prox(self):
        self.init = self.prox - 1
        self.prox = self.init


class Buffer:
    buffer_pair: list[str]
    current_buffer: int
    scan_point: Point
    buffer_num: int
    _has_swaped: bool
    file = str

    def __init__(self, file="") -> None:
        self.buffer_pair = [[], []]
        self.current_buffer = 0
        self.buffer_num = 0
        self.scan_point = Point()
        self.file = file
        self.load(file=file)
        self._has_swaped = False

    def change(self) -> None:
        self.scan_point.prox = -1
        self._has_swaped = True
        self.current_buffer = (self.current_buffer + 1) % 2
        debug_print("Att Buffer")

    @property
    def next_char(self) -> str | None:
        """Retorna o próximo caracter no buffer, lidando com a troca de buffers (sentinelas)"""

        self.scan_point.step_look_ahead()
        next_char = self.buffer_pair[self.current_buffer][self.scan_point.prox]

        if next_char == "$":
            #  Pode ser sentinela padrão ou pode ser final de arquivo
            if self.scan_point.prox == BUFFER_SIZE - 1:
                # Sentinela padrão (final de buffer)
                debug_print("Change")
                self.change()
                self.load(file=self.file)
            # else: FIM DE ARQUIVO
        return next_char

    def load(self, file: str) -> None:
        with open(file, "r", encoding="utf-8") as file_code:
            # move pointer for where to read
            file_code.seek(self.buffer_num * BUFFER_SIZE)
            self.buffer_num += 1

            buffer_ = file_code.read(BUFFER_SIZE - 1)
            buffer_ = buffer_ + "$"
            # Nao apagar linha abaixo talvez seja bom para testes
            # buffer = repr(buffer)
            debug_print(len(buffer_))
            self.buffer_pair[self.current_buffer] = buffer_

        debug_print("Buffer Loaded")

    def sync(self, handle_lookahead: bool = False) -> str:
        """
        Retorna o lexema definido pelos ponteiros 'init' e 'prox' e o seu "Point" de início,
        lidando com lookahead se necessário, e preparando os ponteiros para continuar a análise léxica.
        """
        if handle_lookahead:
            self.scan_point.handle_look_ahead()

        lexem = ""

        if self._has_swaped:
            old_buffer = (self.current_buffer + 1) % 2
            first_part = self.buffer_pair[old_buffer][
                (self.scan_point.init + 1) : (BUFFER_SIZE)
            ]
            last_part = self.buffer_pair[self.current_buffer][0 : self.scan_point.prox]
            lexem = first_part + last_part
            self._has_swaped = False
        else:
            lexem = self.buffer_pair[self.current_buffer][
                (self.scan_point.init + 1) : self.scan_point.prox
            ]
        self.scan_point.init_take_prox()
        self.scan_point.update_location(lexem)
        return lexem


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
    position: tuple[int, int]

    def __init__(self, lexer_result: tuple[Token, tuple[int, int]] | None):
        self.token = lexer_result[0]
        self.position = lexer_result[1]


buffer = Buffer(file=sys.argv[1])
symbol_table = SymbolTable()
