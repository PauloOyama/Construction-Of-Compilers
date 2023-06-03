RELOP_LT = 1
RELOP_LE = 2
RELOP_EQ = 3
RELOP_NE = 4
RELOP_GT = 5
RELOP_GE = 6


class Token:
    token_type: str
    token_attribute: int | None

    def __init__(self, token_type, token_attribute):
        self.token_type = token_type
        self.token_attribute = token_attribute

    def __repr__(self) -> str:
        return f"TOKEN<{self.token_type}, {self.token_attribute}>"
