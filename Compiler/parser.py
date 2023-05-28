from stack import Stack
from treelib import Tree


tokens = ["a", "b", "c", "d", "a", "d", "$"]

DEBUG = False
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

    table = {
        "S": {
            "a": [Symbol("A", False), Symbol("S", False)],
            "b": [Symbol("B", False), Symbol("A", False)],
            "c": [Symbol("A", False), Symbol("S", False)],
            "d": [Symbol("B", False), Symbol("A", False)],
        },
        "A": {
            "a": [Symbol("a", True), Symbol("B", False)],
            "c": [Symbol("C", False)],
        },
        "B": {
            "b": [Symbol("b", True), Symbol("A", False)],
            "d": [Symbol("d", True)],
        },
        "C": {
            "c": [Symbol("c", True)],
        },
    }

    # Initial production to start the syntatic analysis
    initial_symbol = Symbol(
        value="S",
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
    else:
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


if __name__ == "__main__":
    parser()


# IDEIA: Criar um arquivo que conterá as variáveis globais(count de linha, coluna, etc.)
# Dessa forma, é possível colocar o analisador sintático e léxico em arquivos diferentes
# e ter uma organização melhor
