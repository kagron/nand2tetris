import re

from . import code
from .util import print_verbose
from enum import Enum


class InstructionType(Enum):
    A_INSTRUCTION = 1
    C_INSTRUCTION = 2
    L_INSTRUCTION = 3
    INVALID = 4


C_IN_RE = "^(?P<dest>[ADM]+=)?(?P<comp>[-!+&01ADM|]+)(?P<jump>;[A-Z]+)?$"
L_IN_RE = "^\\((?P<symbol>[A-Z]+)\\)$"
A_IN_RE = "^@(?P<symbol>[a-zA-Z0-9]+)$"


class Parser:
    def __init__(self, filename: str, contents: str, symbol_table: dict[str, int]):
        self.filename = filename
        self.contents = contents.splitlines()
        print_verbose(f"Number of lines: {len(self.contents)}")
        print_verbose(f"Contents: {self.contents}")
        self.symbol_line_no = -1
        self.actual_line_no = -1
        self.current_line = ""
        self.parsed_contents: list[str] = []
        self.symbol_table = symbol_table
        self.current_stack_no = 16
        print_verbose(symbol_table)

    def parse(self) -> dict[str, str]:
        # First Pass
        while self.has_more_lines():
            self.advance()
            print_verbose(
                f"First Parsing line {self.actual_line_no + 1}: '{self.current_line}'"
            )
            instruction_type = self.instruction_type()
            if instruction_type is InstructionType.INVALID:
                raise ValueError(
                    f"Invalid instruction type found for '{self.current_line}'"
                )
            if instruction_type is InstructionType.L_INSTRUCTION:
                self.parse_l()

        # Second Pass
        self.current_line = ""
        self.symbol_line_no = -1
        self.actual_line_no = -1
        while self.has_more_lines():
            self.advance()
            print_verbose(
                f"Second parsing line {self.actual_line_no + 1}: '{self.current_line}'"
            )
            instruction_type = self.instruction_type()
            if instruction_type is InstructionType.INVALID:
                raise ValueError(
                    f"Invalid instruction type found for '{self.current_line}'"
                )
            if instruction_type is InstructionType.A_INSTRUCTION:
                self.parse_a()
            if instruction_type is InstructionType.C_INSTRUCTION:
                self.parse_c()
        return dict()

    def has_more_lines(self) -> bool:
        return self.actual_line_no + 1 < len(self.contents)

    def advance(self):
        self.actual_line_no += 1
        self.current_line = re.sub("\\s+", "", self.contents[self.actual_line_no])
        if self.current_line.startswith("//"):
            print_verbose("skipping comment line")
            if self.has_more_lines():
                # Move to next line if comments
                self.advance()
            return
        elif self.instruction_type() is InstructionType.L_INSTRUCTION:
            print_verbose("skipping label line")
            return
        self.symbol_line_no += 1

    def instruction_type(self) -> InstructionType:
        if re.search(A_IN_RE, self.current_line) is not None:
            return InstructionType.A_INSTRUCTION
        elif re.search(L_IN_RE, self.current_line) is not None:
            return InstructionType.L_INSTRUCTION
        elif re.search(C_IN_RE, self.current_line) is not None:
            return InstructionType.C_INSTRUCTION
        return InstructionType.INVALID

    def symbol(self) -> str:
        match = re.match(L_IN_RE, self.current_line)
        group_dict = dict()
        if match is not None:
            group_dict = match.groupdict()
        match = re.match(A_IN_RE, self.current_line)
        if match is not None:
            group_dict = match.groupdict()

        val = group_dict.get("symbol", "")
        if len(val) == 0:
            raise ValueError(
                f"Could not get symbol from instruction at line: {self.actual_line_no}"
            )
        return f"{val}"

    def dest(self) -> str:
        match = re.search(C_IN_RE, self.current_line)
        if match is None:
            raise ValueError(f"Invalid instruction: '{self.current_line}'")
        group_dict = match.groupdict(default="")
        return group_dict["dest"].replace("=", "")

    def comp(self) -> str:
        match = re.match(C_IN_RE, self.current_line)
        if match is None:
            raise ValueError(f"Invalid instruction: '{self.current_line}'")
        group_dict = match.groupdict()
        return group_dict["comp"]

    def jump(self) -> str:
        if self.current_line.find(";") >= 0 and self.current_line[-4:] != "null":
            return self.current_line[-3:]
        return ""

    def parse_a(self):
        symbol_key = self.symbol()
        symbol_val = self.symbol_table.get(symbol_key)
        symbol_key_is_decimal = re.match("\\d+", symbol_key) is not None
        if symbol_val is None and not symbol_key_is_decimal:
            print_verbose(
                f"Adding to symbol table: {symbol_key}={self.current_stack_no}"
            )
            self.symbol_table[symbol_key] = self.current_stack_no
            symbol_val = self.current_stack_no
            self.current_stack_no += 1
        binary = code.print_binary(
            int(symbol_key) if symbol_key_is_decimal else symbol_val, "016b"
        )
        self.parsed_contents.append(binary)

    def parse_c(self):
        binary = f"111{code.comp(self.comp())}{code.dest(self.dest())}{code.jump(self.jump())}"
        self.parsed_contents.append(binary)

    def parse_l(self):
        symbol_key = self.symbol()
        print_verbose(f"Adding to symbol table: {symbol_key}={self.symbol_line_no + 1}")
        self.symbol_table[symbol_key] = self.symbol_line_no + 1
