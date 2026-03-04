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
        self.parsed_contents: list[str] = []
        # self.symbol_table = symbol_table
        self.current_stack_no = 16
        # print_verbose(symbol_table)

    def hasMoreLines(self):
        return

    def advance(self):
        return

    def commandType(self):
        return

    def arg1(self):
        return

    def arg2(self):
        return
