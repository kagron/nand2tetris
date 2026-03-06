from enum import Enum
from .util import print_verbose


class CommandType(Enum):
    C_ARITHMETIC = 0
    C_PUSH = 1
    C_POP = 2
    C_LABEL = 3
    C_GOTO = 4
    C_IF = 5
    C_FUNCTION = 6
    C_RETURN = 7
    C_CALL = 8
    C_INVALID = 9


# C_IN_RE = "^(?P<dest>[ADM]+=)?(?P<comp>[-!+&01ADM|]+)(?P<jump>;[A-Z]+)?$"
# L_IN_RE = "^\\((?P<symbol>[A-Z]+)\\)$"
# A_IN_RE = "^@(?P<symbol>[a-zA-Z0-9]+)$"


class Parser:
    def __init__(self, filename: str, contents: str):
        self.filename = filename
        self.contents = contents.splitlines()
        print_verbose(f"Number of lines: {len(self.contents)}")
        print_verbose(f"Contents: {self.contents}")
        self.symbol_line_no = -1
        self.actual_line_no = -1
        self.current_line = ""
        # self.parsed_contents: list[str] = []
        # self.symbol_table = symbol_table
        self.current_stack_no = 16
        # print_verbose(symbol_table)

    def hasMoreLines(self) -> bool:
        return self.actual_line_no + 1 < len(self.contents)

    def advance(self):
        self.current_line = self.contents[self.actual_line_no]
        self.actual_line_no += 1
        if self.current_line.find("//") > -1:
            return
        # TODO: Add symbols / functions
        self.tokens = self.current_line.split("//")[0].strip().split(" ")

    def commandType(self) -> CommandType:
        for token in self.tokens:
            if ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"].__contains__(
                token
            ):
                return CommandType.C_ARITHMETIC
            if token.find("push") > -1:
                return CommandType.C_PUSH
            if token.find("pop") > -1:
                return CommandType.C_POP
            if token.find("label") > -1:
                return CommandType.C_LABEL
            if token.find("function") > -1:
                return CommandType.C_FUNCTION
            if token.find("return") > -1:
                return CommandType.C_RETURN
            if token.find("call") > -1:
                return CommandType.C_CALL
            if token.find("if") > -1:
                return CommandType.C_IF
            if token.find("goto") > -1:
                return CommandType.C_GOTO

        return CommandType.C_INVALID

    def arg1(self) -> str:
        return self.tokens[1:2][0] if len(self.tokens) > 1 else self.tokens[1]

    def arg2(self) -> int:
        assert len(self.tokens) > 2, (
            "arg2 should only be called when using pop, push, function, or call"
        )
        token = self.tokens[2:3][0]
        assert token.isdigit(), f"Index '{token}' must be integer"
        return int(self.tokens[2:3][0])
