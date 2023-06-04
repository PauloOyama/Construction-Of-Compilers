"""
    Source code of Parser
"""

from treelib import Tree

from src.lexer import get_token
from src.parser_table import ParseTableSymbol, parser_table
from src.stack import Stack
from src.classes import debug_print, UnexpectedTokenException, symbol_table, buffer


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

    lexer_result = get_token(buffer)

    try:
        while stack.is_not_empty():
            if lexer_result is not None:
                next_token, _ = lexer_result

            # Take element at the top of the stack
            stack_symbol = stack.peek()

            debug_print(
                f"Stack Top: {stack_symbol.value} | Input token: {next_token.token_type}"
            )

            if stack_symbol.is_terminal:
                match_token = stack_symbol.value == next_token.token_type
                # Check needed because keywords are treated as identifiers
                if next_token.token_type == "ID":
                    lexemn = symbol_table.table[next_token.token_attribute].lexemn
                    debug_print(f"Token Type ID: {lexemn}")

                    # In case that token from lexer is a keyword(function, int, etc)
                    # The match with the symbol on top of stack need to be done with
                    # the lexemn(function, int, etc) and not with the token_type(ID)
                    if lexemn in symbol_table.keywords:
                        match_token = stack_symbol.value == lexemn

                if match_token:
                    debug_print("Match symbol with next token")
                    popped = stack.pop()
                    debug_print(f"Popped: {popped.value}")
                    lexer_result = get_token(buffer)
                else:
                    raise UnexpectedTokenException(lexer_result)

            else:
                debug_print("Not terminal, searching for valid production")
                key_to_search = next_token.token_type
                # Check needed because keywords are treated as identifiers
                if next_token.token_type == "ID":
                    lexemn = symbol_table.table[next_token.token_attribute].lexemn
                    debug_print(f"Token Type ID: {lexemn}")
                    # In case that token from lexer is a keyword(function, int, etc)
                    # we need to search in the parser_table for the keyword
                    # In case token is an ID, we search for "ID"
                    if lexemn in symbol_table.keywords:
                        key_to_search = lexemn

                symbols = parser_table.get(stack_symbol.value, {}).get(
                    key_to_search, None
                )

                if symbols is None:
                    raise UnexpectedTokenException(lexer_result)

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

        if lexer_result is not None:
            raise UnexpectedTokenException(lexer_result)

        print("Recognized Input sequence")
        tree.show()
        return tree
    except UnexpectedTokenException as exception:
        entry = ""
        if exception.token.token_type in ("ID", "CONST_CHAR", "CONST_NUM"):
            entry = symbol_table.table[exception.token.token_attribute].lexemn
        else:
            entry = exception.token.token_type
        print(
            f"Syntax Error: unexpected token from entry ({entry}) at {exception.position[0]}, {exception.position[1]}"
        )
        debug_print("Stack on this moment")
        while stack.is_not_empty():
            debug_print(stack.pop().value)
        return None
