class SymbolTable:
    table: dict

    def __init__(self) -> None:
        #Estrutura pensada para a key (lexema, tipo do token, valor do atributo, tipo do dado)
        
        #Make a load from reserverd words
        self.table = {
            'function' : ('function','function','',''),
            '(': ('(','(','',''),
            ')' : (')',')','',''),
            'int':('int','int','',''),
            'float':('float','float','',''),
            'char':('char','char','',''),
            'se':('se','se','',''),
            'entao':('entao','entao','',''),
            'senao':('senao','senao','',''),
            'enquanto': ('enquanto','enquanto','',''),
            'faca': ('faca','faca','',''),
            'repita': ('repita','repita','',''),
            'ate': ('ate','ate','','')
        }

class Point : 
    init: int
    prox: int
    line: int
    column:int
    
    def __init__(self) -> None:
        self.init = 0
        self.prox = -1
        self.column = 0
        self.line = 0

    @property
    def where(self):
        return (self.line,self.column)
    
    def addInLine(self): self.line +=1
    def addInColumn(self): self.column +=1
    def initTakeProx(self): self.init = self.prox
    def stepLookAhead(self): self.prox +=1
        

class Buffer:
    buffer : list[list]
    CURRENT_BUFFER : int
    vigilant : Point

    def __init__(self) -> None:
        self.buffer = [[],[]]
        self.CURRENT_BUFFER = 0
        self.vigilant = Point()
    
    @property
    def lst(self) -> list[list]:
        print(f"Current Buffer ${self.CURRENT_BUFFER + 1}")
        return self.buffer[self.CURRENT_BUFFER]

    def change(self) -> None:
        if self.CURRENT_BUFFER == 0:
            self.CURRENT_BUFFER = 1
        else:
            self.CURRENT_BUFFER = 0
        print("Att Buffer")

    @lst.getter
    def nextChar(self): 
        self.vigilant.stepLookAhead()
        return self.buffer[self.CURRENT_BUFFER][self.vigilant.prox]

    @lst.setter
    def load(self, readed_file: str) -> None:
        self.buffer[self.CURRENT_BUFFER] = readed_file
        print("Buffer Loaded")

    def sync(self): self.vigilant.initTakeProx


