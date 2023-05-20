from stack import Stack


tokens = ["a", "b", "c", "d", "a", "d", "$"]


def lexer(token_num):
    """aaa"""
    token = tokens[token_num]
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
    stack = Stack()
    initial_symbol = Symbol(
        value="S",
        is_terminal=False,
    )
    stack.push(initial_symbol)
    token_num = 0
    next_token = lexer(token_num)

    token_num += 1
    while stack.is_not_empty():
        symbol = stack.peek()
        print(f"=> Stack: {symbol.value}({symbol.is_terminal}) | Input: {next_token}")

        if symbol.is_terminal:
            if symbol.value == next_token:
                print("Match symbol with next token")
                popped = stack.pop()
                print(f"Popped: {popped.value}")
                next_token = lexer(token_num)
                token_num += 1
            else:
                print("error")
                break
        else:
            symbols = table.get(symbol.value, {}).get(next_token, None)

            if symbols is None:
                print("Error")
                break
            else:
                popped = stack.pop()
                print(f"Popped: {popped.value}")
                copy_symbols = symbols.copy()
                copy_symbols.reverse()
                for s in copy_symbols:
                    print(f"Pushing: {s.value}")
                    stack.push(s)
    if next_token != "$":
        print("Error")
    else:
        print("Recognized")


# Estrutura de dados:
# Deverá representar tanto terminais quanto não-terminais


class Symbol:
    """
    Class to represent a terminal or non-terminal symbol
    """

    value: str
    is_terminal: bool

    def __init__(self, value, is_terminal):
        self.value = value
        self.is_terminal = is_terminal


if __name__ == "__main__":
    parser()
