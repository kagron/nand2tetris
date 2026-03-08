from io import TextIOWrapper


class CodeWriter:
    def __init__(self, file: TextIOWrapper) -> None:
        self.file = file
        self.eqi = 0
        self.gti = 0
        self.lti = 0

    def write_arithmetic(self, command: str):
        self.buffer: list[str] = list()
        self.buffer.append(f"// write_arithmetic {command}\n")

        if command == "add":
            self._popSimple()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  M=D+M\n")
        elif command == "sub":
            self._popSimple()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  M=M-D\n")
        elif command == "neg":
            self._popSimple()
            self.buffer.append("  A=M\n")
            self.buffer.append("  M=-D\n")
            self.buffer.append("  @SP\n")
            self.buffer.append("  M=M+1\n")
        elif command == "eq":
            self._popSimple()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  D=D-M\n")
            self.buffer.append(f"  @FALSE_EQ_{self.eqi}\n")
            self.buffer.append("  D;JNE\n")
            self.buffer.append(f"(TRUE_EQ_{self.eqi})\n")
            self.buffer.append("  D=1\n")
            self._pushSimple()
            self.buffer.append(f"  @DONE_EQ_{self.eqi}\n")
            self.buffer.append("  0;JMP\n")
            self.buffer.append(f"(FALSE_EQ_{self.eqi})\n")
            self.buffer.append("  D=0\n")
            self._pushSimple()
            self.buffer.append(f"(DONE_EQ_{self.eqi})\n")
            self.eqi += 1
        elif command == "gt":
            self._popSimple()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  D=M-D\n")
            self.buffer.append(f"  @FALSE_GT_{self.gti}\n")
            self.buffer.append("  D;JLE\n")
            self.buffer.append(f"(TRUE_GT_{self.gti})\n")
            self.buffer.append("  D=1\n")
            self._pushSimple()
            self.buffer.append(f"  @DONE_GT_{self.gti}\n")
            self.buffer.append("  0;JMP\n")
            self.buffer.append(f"(FALSE_GT_{self.gti})\n")
            self.buffer.append("  D=0\n")
            self._pushSimple()
            self.buffer.append(f"(DONE_GT_{self.gti})\n")
            self.gti += 1
        elif command == "lt":
            self._popSimple()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  D=M-D\n")
            self.buffer.append(f"  @FALSE_LT_{self.lti}\n")
            self.buffer.append("  D;JGE\n")
            self.buffer.append(f"(TRUE_LT_{self.lti})\n")
            self.buffer.append("  D=1\n")
            self._pushSimple()
            self.buffer.append(f"  @DONE_LT_{self.lti}\n")
            self.buffer.append("  0;JMP\n")
            self.buffer.append(f"(FALSE_LT_{self.lti})\n")
            self.buffer.append("  D=0\n")
            self._pushSimple()
            self.buffer.append(f"(DONE_LT_{self.lti})\n")
            self.lti += 1
        elif command == "and":
            self._popSimple()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  M=D&M\n")
        elif command == "or":
            self._popSimple()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  M=D|M\n")
        elif command == "not":
            self._popSimple()
            self.buffer.append("  A=M\n")
            self.buffer.append("  M=!D\n")
            self.buffer.append("  @SP\n")
            self.buffer.append("  M=M+1\n")
        self.file.writelines(self.buffer)

    def write_push_pop(self, command: str, segment: str, index: int):
        self.buffer = list()
        if command == "push":
            self.buffer.append(f"  @{index}\n")  # TODO: Currently loading constant
            self.buffer.append("  D=A\n")
            self._pushSimple()
        elif command == "pop":
            self._popSimple()
            self.buffer.append(f"  @{index}\n")  # TODO: Currently only loading index
            self.buffer.append("  M=D\n")
        self.file.writelines(self.buffer)

    def _pushSimple(self):
        """Pushes D register onto stack.  A will be at @SP"""
        self.buffer.append("// Push D\n")
        self.buffer.append("  @SP\n")
        self.buffer.append("  A=M\n")
        self.buffer.append("  M=D\n")
        self.buffer.append("  @SP\n")
        self.buffer.append("  M=M+1\n")

    def _popSimple(self):
        """Pops stack into D register.  A will be at @SP"""
        self.buffer.append("// Pop D\n")
        self.buffer.append("  @SP\n")
        self.buffer.append("  A=M-1\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("  @SP\n")
        self.buffer.append("  M=M-1\n")

    def _pop(self, segment: str, index: int):
        segment_label = ""
        if segment == "local":
            segment_label = "LCL"
        elif segment == "argument":
            segment_label = "ARG"
        elif segment == "this":
            segment_label = "THIS"
        elif segment == "that":
            segment_label = "THAT"

        self.buffer.append(f"// Pop {segment} {index}\n")
        self.buffer.append(f"  @{index}\n")
        self.buffer.append("  D=A\n")
        self.buffer.append(f"  @{segment_label}\n")
        self.buffer.append("  D=D+M\n")  # D = @LCL + @index
        self.buffer.append("  @R13\n")
        self.buffer.append("  M=D\n")  # RAM[13] = dest pointer

        self.buffer.append("  @SP\n")
        self.buffer.append("  A=A-1\n")
        self.buffer.append("  D=M\n")  # D = stack[@SP-1]

        self.buffer.append("  @R13\n")
        self.buffer.append("  A=M\n")  # A = dest pointer

        self.buffer.append("  M=D\n")  # Store data into pointer location

        self.buffer.append("  @SP\n")
        self.buffer.append("  M=M-1\n")  # SP-1

    def _push(self, segment: str, index: str):
        self.buffer.append(f"// Push {segment} {index}\n")
        pass
