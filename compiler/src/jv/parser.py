from enum import Enum, auto
from .util import print_verbose


class CommandType(Enum):
    C_ARITHMETIC = auto()
    C_PUSH = auto()
    C_POP = auto()
    C_LABEL = auto()
    C_GOTO = auto()
    C_IF = auto()
    C_FUNCTION = auto()
    C_RETURN = auto()
    C_CALL = auto()
    C_INVALID = auto()


class Parser:
    def __init__(self, filename: str, contents: str):
        self.filename = filename
        self.contents = contents.splitlines()
        print_verbose(f"Number of lines: {len(self.contents)}")
        print_verbose(f"Contents: {self.contents}")
        self.symbol_line_no = -1
        self.actual_line_no = -1
        self.current_line = ""

    def hasMoreLines(self) -> bool:
        return self.actual_line_no + 1 < len(self.contents)

    def advance(self):
        self.actual_line_no += 1
        self.current_line = self.contents[self.actual_line_no]
        print_verbose(f"current_line: {self.current_line}")
        self.tokens = self.current_line.split("//")[0].strip().split(" ")
        print_verbose(f"tokens: {self.tokens}")

    def command_type(self) -> CommandType:
        """Returns `CommandType` of current line"""
        assert self.tokens is not None, "Must not call this in comment line"
        for token in self.tokens:
            if ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"].__contains__(
                token
            ):
                return CommandType.C_ARITHMETIC
            elif token.find("push") > -1:
                return CommandType.C_PUSH
            elif token.find("pop") > -1:
                return CommandType.C_POP
            elif token.find("label") > -1:
                return CommandType.C_LABEL
            elif token.find("function") > -1:
                return CommandType.C_FUNCTION
            elif token.find("return") > -1:
                return CommandType.C_RETURN
            elif token.find("call") > -1:
                return CommandType.C_CALL
            # Order matters here since if will succeed first before goto
            elif token.find("if") > -1:
                return CommandType.C_IF
            elif token.find("goto") > -1:
                return CommandType.C_GOTO

        return CommandType.C_INVALID

    def arg1(self) -> str:
        """Returns first argument of current line"""
        assert self.tokens is not None, "Must not call this in comment line"
        return self.tokens[1:2][0] if len(self.tokens) > 1 else self.tokens[0]

    def arg2(self) -> int:
        """Returns second argument of current line"""
        assert self.tokens is not None, "Must not call this in comment line"
        assert len(self.tokens) > 2, (
            "arg2 should only be called when using pop, push, function, or call"
        )
        token = self.tokens[2:3][0]
        assert token.isdigit(), f"Index '{token}' must be integer"
        return int(token)
