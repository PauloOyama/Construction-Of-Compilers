from treelib import Tree

from src.classes import SymbolTable, UnexpectedTokenException
from src.parser_table import ParseTableSymbol, table
from src.stack import Stack
from src.token import Token

tokens: list[Token | None] = [
    Token("ID", 0),  # function
    Token("ID", 11),  # main
    Token("(", None),
    Token(")", None),
    Token("{", None),
    Token("ID", 1),  # int
    Token(":", None),
    Token("ID", 12),  # x
    Token(",", None),
    Token("ID", 13),  # y
    Token(",", None),
    Token("ID", 14),  # z
    Token(";", None),
    Token("ID", 12),  # x
    Token("=", None),
    Token("ID", 13),  # y
    Token(";", None),
    Token("}", None),
    None,
]

DEBUG = True
COUNT = 0

symbol_table = SymbolTable()
print(symbol_table.append("main", "ID", None, None))
print(symbol_table.append("x", "ID", None, None))
print(symbol_table.append("y", "ID", None, None))
print(symbol_table.append("z", "ID", None, None))


def lexer() -> Token | None:
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
    initial_symbol = ParseTableSymbol(
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

    try:
        while stack.is_not_empty():
            # Take element at the top of the stack
            stack_symbol = stack.peek()

            debug_print(
                f"Stack Top: {stack_symbol.value} | Input token: {next_token.token_type}"
            )

            if stack_symbol.is_terminal:
                match_token = False
                if next_token.token_type == "ID":
                    lexemn = symbol_table.table[next_token.token_attribute].lexemn
                    debug_print(f"Token Type ID: {lexemn}")

                    if lexemn in symbol_table.keywords:
                        match_token = stack_symbol.value == lexemn
                    else:
                        match_token = stack_symbol.value == next_token.token_type
                elif stack_symbol.value == next_token.token_type:
                    match_token = True

                # if stack_symbol.value == next_token.token_type:
                if match_token:
                    debug_print("Match symbol with next token")
                    popped = stack.pop()
                    debug_print(f"Popped: {popped.value}")
                    next_token = lexer()
                else:
                    raise UnexpectedTokenException(next_token.token_type)

            else:
                debug_print("Not terminal, searching for valid production")
                key_to_search = next_token.token_type
                if next_token.token_type == "ID":
                    lexemn = symbol_table.table[next_token.token_attribute].lexemn
                    debug_print(f"Token Type ID: {lexemn}")
                    key_to_search = lexemn

                symbols = table.get(stack_symbol.value, {}).get(key_to_search, None)

                if symbols is None:
                    raise UnexpectedTokenException(next_token.token_type)

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
                    node = tree.create_node(
                        tag=child_symbol.value, parent=stack_symbol.uuid
                    )
                    child_symbol.uuid = node.identifier
                    stack.push(child_symbol)

        if next_token is not None:
            raise UnexpectedTokenException(next_token.token_type)

        print("Recognized Input sequence")
        tree.show()
        return tree
    except UnexpectedTokenException as exception:
        print(f"Syntax Error: unexpected token from entry ({exception})")
        debug_print("Stack on this moment")
        while stack.is_not_empty():
            debug_print(stack.pop().value)
        return None


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
