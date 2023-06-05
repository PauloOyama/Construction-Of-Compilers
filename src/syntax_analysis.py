"""
    Source code of Parser
"""

from treelib import Tree

from src.classes import UnexpectedTokenException, buffer, debug_print, symbol_table
from src.lexer import LexerError, get_token
from src.parser_table import ParseTableSymbol, parser_table
from src.stack import Stack

# https://treelib.readthedocs.io/en/latest/treelib.html#module-treelib.tree


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
                    node = tree.get_node(stack_symbol.uuid)
                    node.data = {
                        "token_attribute": next_token.token_attribute,
                        "token_type": next_token.token_type,
                    }
                    debug_print("Match symbol with next token")
                    popped = stack.pop()
                    debug_print(f"Popped: {popped.value}")
                    lexer_result = get_token(buffer)
                else:
                    raise UnexpectedTokenException(lexer_result)

            elif stack_symbol.is_terminal is None:
                popped = stack.pop()
                debug_print(f"Popped Special Symbol: {popped.value}")
                ## Execute semantic analysis on special symbol
                on_semantic_pop(tree, popped)

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

                # First, will push a special symbol that, when popped, will trigger the execution
                # of semantic analysis for the parent of that symbol
                debug_print(f"Pushing EXEC_{popped.value} to make semantic analysis")
                special_symbol = ParseTableSymbol(
                    value=f"EXEC_{popped.value}",
                    is_terminal=None,
                )
                node = tree.create_node(
                    tag=special_symbol.value, parent=stack_symbol.uuid
                )
                special_symbol.uuid = node.identifier
                special_symbol.prod = symbols
                stack.push(special_symbol)

                # Push all symbols from production in reverse order
                # and add to tree as children of symbol
                parent_id = stack_symbol.uuid
                for child_symbol in copied_symbols:
                    # Set data attribute on tree to be the token when pushing a symbol that is a terminal
                    debug_print(f"Pushing: {child_symbol.value}")
                    node = tree.create_node(
                        tag=child_symbol.value,
                        parent=parent_id,
                    )
                    child_symbol.uuid = node.identifier
                    stack.push(child_symbol)

        if lexer_result is not None:
            raise UnexpectedTokenException(lexer_result)

        debug_print("Recognized Input sequence")
        tree.show()
        return tree
    except UnexpectedTokenException as exception:
        entry = ""
        if exception.token.token_type in ("ID", "CONST_CHAR", "CONST_NUM"):
            entry = symbol_table.table[exception.token.token_attribute].lexemn
        else:
            entry = exception.token.token_type
        print(
            f"Syntax Error: unexpected token from entry ({entry}) at {exception.position[0]}, {exception.position[1]}."
        )
        debug_print("Stack on this moment")
        while stack.is_not_empty():
            debug_print(stack.pop().value)
        return None
    except SyntaxTypeError:
        print(
            "Type Error: an incompatibility was found between expression operator types."
        )
        return None
    except LexerError as exception:
        print(
            f"Name Error: coundn't match token at {exception.position[0]}, {exception.position[1]}."
        )


def on_semantic_pop(tree: Tree, special_symbol: ParseTableSymbol):
    debug_print(f"Popping {special_symbol.value} | {special_symbol.uuid}")
    # tree.show()
    # print("---------")
    parent = tree.parent(special_symbol.uuid)
    # print(f"Parent ID: {parent_id}")
    sub_tree = tree.subtree(parent.identifier)
    # print(sub_tree.depth())
    # sub_tree.show()
    debug_print("Production: ")
    for prod_symbols in special_symbol.prod:
        debug_print(f"{prod_symbols.value}", end=" ")
    debug_print("")
    debug_print("============")

    children = list(reversed(sub_tree.children(parent.identifier)))

    # parent.tag -> cabeça da produção
    # children -> corpo da produção já executada; referência dos nós da árvore sintática

    if parent.tag == "DECLARACAO_VAR":
        prod_type = children[0]
        prod_ids = children[2]
        update_sym_table_entries(prod_type.data, prod_ids.data)
    elif parent.tag == "TIPO":
        # Ação semântica (genérica p/ TIPO)
        parent.data = special_symbol.prod[0].value
    elif parent.tag == "LISTA_IDS":
        # ID LISTA_IDS'
        prod_id = children[0]  # ID
        prod_lista_ids = children[1]  # LISTA_IDS'
        # List of IDs positions on the symbol table
        parent.data = [prod_id.data["token_attribute"]] + prod_lista_ids.data
    elif parent.tag == "LISTA_IDS'":
        if len(special_symbol.prod) == 0:
            # Ɛ
            parent.data = []
        else:
            # , ID LISTA_IDS'
            prod_id = children[1]
            prod_lista_ids = children[2]
            # List of IDs positions on the symbol table
            parent.data = [prod_id.data["token_attribute"]] + prod_lista_ids.data

    elif parent.tag == "CMD_ATRIB":
        validate_attr_type(
            get_sym_table_entry(children[0].data["token_attribute"]).data_type,
            children[2].data,
        )

    elif parent.tag == "COND":
        # EXPRESSAO op_rel EXPRESSAO
        validate_expr_type(children[0].data, children[2].data)
    elif parent.tag == "EXPRESSAO":
        # TERMO EXPRESSAO'
        parent.data = validate_expr_type(children[0].data, children[1].data)
    elif parent.tag == "EXPRESSAO'":
        if len(special_symbol.prod) == 0:
            # Ɛ
            parent.data = None
        else:
            # + TERMO EXPRESSAO'
            # - TERMO EXPRESSAO'
            parent.data = validate_expr_type(children[1].data, children[2].data)
    elif parent.tag == "TERMO":
        # EXPONENC TERMO'
        parent.data = validate_expr_type(children[0].data, children[1].data)
    elif parent.tag == "TERMO'":
        if len(special_symbol.prod) == 0:
            # Ɛ
            parent.data = None
        else:
            # * EXPONENC TERMO'
            # / EXPONENC TERMO'
            parent.data = validate_expr_type(children[1].data, children[2].data)
    elif parent.tag == "EXPONENC":
        # FATOR EXPONENC'
        parent.data = validate_expr_type(children[0].data, children[1].data)
    elif parent.tag == "EXPONENC'":
        if len(special_symbol.prod) == 0:
            # Ɛ
            parent.data = None
        else:
            # ^ FATOR EXPONENC'
            parent.data = validate_expr_type(children[1].data, children[2].data)
    elif parent.tag == "FATOR":
        if len(special_symbol.prod) >= 3:
            # (EXPRESSAO)
            parent.data = children[1].data
        else:
            # CONST_CHAR
            # CONST_NUM
            # ID
            parent.data = get_sym_table_entry(
                children[0].data["token_attribute"]
            ).data_type

    debug_print(sub_tree.to_json(with_data=True))
    debug_print("============")


def update_sym_table_entries(data_type: str, idxs: list[int]):
    for symbol_idx in idxs:
        entry = symbol_table.table[symbol_idx]
        entry.data_type = data_type


def get_sym_table_entry(position: int):
    return symbol_table.table[position]


class SyntaxTypeError(Exception):
    """Erro de verificação de tipos no Analisador Sintático."""


def validate_expr_type(type1: str, type2: str):
    if type1 is None:
        return type2
    if type2 is None:
        return type1
    if type1 == "char" and type2 != "char":
        raise SyntaxTypeError()
    if type2 == "char" and type1 != "char":
        raise SyntaxTypeError()
    if type1 == "int" and type2 == "float":
        return type2
    if type2 == "int" and type1 == "float":
        return type1
    return type1


def validate_attr_type(id_type: str, expression_type: str):
    if id_type is None:
        return expression_type
    if expression_type is None:
        return id_type
    if id_type == "char" and expression_type != "char":
        raise SyntaxTypeError()
    if expression_type == "char" and id_type != "char":
        raise SyntaxTypeError()
    if id_type == "float" and expression_type == "int":
        return id_type
    if id_type == "int" and expression_type == "float":
        raise SyntaxTypeError()
    return id_type
