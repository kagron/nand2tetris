import re
from enum import Enum


class InstructionType(Enum):
    A_INSTRUCTION = 1
    C_INSTRUCTION = 2
    L_INSTRUCTION = 3
    INVALID = 4


class Parser:
    def __init__(self, filename: str, contents: str):
        self.filename = filename
        self.contents = contents.splitlines()
        print(f"Number of lines: {len(self.contents)}")
        print(f"Contents: {self.contents}")
        self.symbol_line_no = -1
        self.actual_line_no = -1
        self.current_line = ""
        self.parsed_contents: list[str] = []

    def parse(self) -> dict[str, str]:
        while self.has_more_lines():
            self.advance()
            print(f"Parsing line {self.actual_line_no + 1}: '{self.current_line}'")
            instruction_type = self.instruction_type()
            if instruction_type is InstructionType.A_INSTRUCTION:
                self.parse_a()
            elif instruction_type is InstructionType.C_INSTRUCTION:
                self.parse_c()
            elif instruction_type is InstructionType.L_INSTRUCTION:
                self.parse_l()
            else:
                print(
                    f"Invalid Instruction type on line {self.actual_line_no + 1}: '{self.current_line}'"
                )

        return dict()

    def has_more_lines(self) -> bool:
        return self.actual_line_no + 1 < len(self.contents)

    def advance(self):
        self.actual_line_no += 1
        self.current_line = re.sub("\s+", "", self.contents[self.actual_line_no])
        if self.current_line.startswith("//"):
            print("skipping comment line")
            return
        elif self.current_line.startswith("("):
            print("skipping label line")
            return
        self.symbol_line_no += 1

    def instruction_type(self) -> InstructionType:
        if re.search("^@[a-zA-Z]+[a-zA-Z0-9]*$", self.current_line) is not None:
            return InstructionType.A_INSTRUCTION
        elif re.search("^\\([A-Z]+\\)+$", self.current_line) is not None:
            return InstructionType.L_INSTRUCTION
        elif (
            re.search("^([ADM]=)?([!-+&|01ADM]+)(;[A-Z]+)?$", self.current_line)
            is not None
        ):
            return InstructionType.C_INSTRUCTION
        return InstructionType.INVALID

    def symbol(self) -> str:
        return ""

    def dest(self) -> str:
        return ""

    def comp(self) -> str:
        return ""

    def jump(self) -> str:
        return ""

    def parse_a(self):
        self.parsed_contents.append(self.current_line)

    def parse_c(self):
        self.parsed_contents.append(self.current_line)

    def parse_l(self):
        self.parsed_contents.append(self.current_line)
