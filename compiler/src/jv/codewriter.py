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
        file_name_no_ext = self.file.name[:-4].upper()

        if command == "add":
            self._pop_d()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  M=D+M\n")
        elif command == "sub":
            self._pop_d()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  M=M-D\n")
        elif command == "neg":
            self._pop_d()
            self.buffer.append("  A=M\n")
            self.buffer.append("  M=-D\n")
            self.buffer.append("  @SP\n")
            self.buffer.append("  M=M+1\n")
        elif command == "eq":
            self._pop_d()
            # TODO: Can I optimize this without conditions?
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  D=D-M\n")
            self.buffer.append(f"  @{file_name_no_ext}_FALSE_EQ_{self.eqi}\n")
            self.buffer.append("  D;JNE\n")
            self.buffer.append(f"({file_name_no_ext}_TRUE_EQ_{self.eqi})\n")
            self.buffer.append("  D=1\n")
            self._push_d()
            self.buffer.append(f"  @{file_name_no_ext}_DONE_EQ_{self.eqi}\n")
            self.buffer.append("  0;JMP\n")
            self.buffer.append(f"({file_name_no_ext}_FALSE_EQ_{self.eqi})\n")
            self.buffer.append("  D=0\n")
            self._push_d()
            self.buffer.append(f"({file_name_no_ext}_DONE_EQ_{self.eqi})\n")
            self.eqi += 1
        elif command == "gt":
            self._pop_d()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  D=M-D\n")
            self.buffer.append(f"  @{file_name_no_ext}_FALSE_GT_{self.gti}\n")
            self.buffer.append("  D;JLE\n")
            self.buffer.append(f"({file_name_no_ext}_TRUE_GT_{self.gti})\n")
            self.buffer.append("  D=1\n")
            self._push_d()
            self.buffer.append(f"  @{file_name_no_ext}_DONE_GT_{self.gti}\n")
            self.buffer.append("  0;JMP\n")
            self.buffer.append(f"({file_name_no_ext}_FALSE_GT_{self.gti})\n")
            self.buffer.append("  D=0\n")
            self._push_d()
            self.buffer.append(f"({file_name_no_ext}_DONE_GT_{self.gti})\n")
            self.gti += 1
        elif command == "lt":
            self._pop_d()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  D=M-D\n")
            self.buffer.append(f"  @{file_name_no_ext}_FALSE_LT_{self.lti}\n")
            self.buffer.append("  D;JGE\n")
            self.buffer.append(f"({file_name_no_ext}_TRUE_LT_{self.lti})\n")
            self.buffer.append("  D=1\n")
            self._push_d()
            self.buffer.append(f"  @{file_name_no_ext}_DONE_LT_{self.lti}\n")
            self.buffer.append("  0;JMP\n")
            self.buffer.append(f"({file_name_no_ext}_FALSE_LT_{self.lti})\n")
            self.buffer.append("  D=0\n")
            self._push_d()
            self.buffer.append(f"({file_name_no_ext}_DONE_LT_{self.lti})\n")
            self.lti += 1
        elif command == "and":
            self._pop_d()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  M=D&M\n")
        elif command == "or":
            self._pop_d()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  M=D|M\n")
        elif command == "not":
            self._pop_d()
            self.buffer.append("  A=M\n")
            self.buffer.append("  M=!D\n")
            self.buffer.append("  @SP\n")
            self.buffer.append("  M=M+1\n")

        self.file.writelines(self.buffer)

    def write_push_pop(self, command: str, segment: str, index: int):
        self.buffer = list()
        if command == "push":
            self._push(segment, index)
        elif command == "pop":
            self._pop(segment, index)
        self.file.writelines(self.buffer)

    def _push_d(self):
        """Pushes D register onto stack.  A will be at @SP"""
        self.buffer.append("// Push D\n")
        self.buffer.append("  @SP\n")
        self.buffer.append("  A=M\n")
        self.buffer.append("  M=D\n")
        self._incSP()

    def _pop_d(self):
        """Pops stack into D register.  A will be at @SP"""
        self.buffer.append("// Pop D\n")
        self.buffer.append("  @SP\n")
        self.buffer.append("  A=M-1\n")
        self.buffer.append("  D=M\n")
        self._decSP()

    def _incSP(self):
        """Incremenets stack pointer.  A will be at @SP"""
        self.buffer.append("  @SP\n")
        self.buffer.append("  M=M+1\n")

    def _decSP(self):
        """Decrements stack pointer.  A will be at @SP"""
        self.buffer.append("  @SP\n")
        self.buffer.append("  M=M-1\n")

    def _pop(self, segment: str, index: int):
        self.buffer.append(f"// Pop {segment} {index}\n")
        # self._pop_d()

        if segment == "local":
            self._store_d_index("LCL", index)
        elif segment == "argument":
            self._store_d_index("ARG", index)
        elif segment == "pointer":
            self._store_d_segment("THIS" if index == 0 else "THAT")
        elif segment == "temp":
            assert index >= 0 and index <= 7, "Index must be between 0-7"
            self._store_d_ram(f"R{5 + index}")
        elif segment == "static":
            self._store_d_ram(f"{self.file.name[:-4].upper()}_{index}")

    def _push(self, segment: str, index: int):
        self.buffer.append(f"// Push {segment} {index}\n")
        if segment == "local":
            self._load_index_d("LCL", index)
        elif segment == "argument":
            self._load_index_d("ARG", index)
        elif segment == "pointer":
            self._load_segment_d("THIS" if index == 0 else "THAT")
        elif segment == "constant":
            assert index >= 0 and index < 2**15, "Index must be between 0-32767"
            self.buffer.append(f"  @{index}\n")
            self.buffer.append("  D=A\n")
        elif segment == "temp":
            assert index >= 0 and index <= 7, "Index must be between 0-7"
            self._load_ram_d(f"R{5 + index}")
        elif segment == "static":
            # assert index >= 16 and index <= 255, "Index must be between 16-255"
            self._load_ram_d(f"{self.file.name[:-4].upper()}_{index}")

        self._push_d()

    def _store_d_index(self, segment: str, index: int):
        """Stores D register at base segment + index"""
        # TODO: Can I optimize this without using R13 for storing segment + index?
        self.buffer.append(f"  @{index}\n")
        self.buffer.append("  D=A\n")
        self.buffer.append(f"  @{segment}\n")
        self.buffer.append("  D=D+M\n")
        self.buffer.append("  @R13\n")
        self.buffer.append("  M=D\n")

        self._pop_d()

        self.buffer.append("  @R13\n")
        self.buffer.append("  A=M\n")
        self.buffer.append("  M=D\n")

    def _store_d_segment(self, segment: str):
        """Stores D register at base segment"""
        self._pop_d()
        self.buffer.append(f"  @{segment}\n")
        self.buffer.append("  A=M")
        self.buffer.append("  M=D")

    def _store_d_ram(self, address: str):
        """Goes to RAM[address] and stores D Register there"""
        self._pop_d()
        self.buffer.append(f"  @{address}\n")
        self.buffer.append("  M=D\n")

    def _load_index_d(self, segment: str, index: int):
        """Goes to base segment + index and stores value into D Register"""
        self.buffer.append(f"  @{index}\n")
        self.buffer.append("  D=A\n")
        self.buffer.append(f"  @{segment}\n")
        self.buffer.append("  A=D+M\n")
        self.buffer.append("  D=M\n")

    def _load_segment_d(self, segment: str):
        """Goes to base segment and stores value into D Register"""
        self.buffer.append(f"  @{segment}\n")
        self.buffer.append("  A=M\n")
        self.buffer.append("  D=M\n")

    def _load_ram_d(self, address: str):
        """Goes to RAM[address] and stores value into D Register"""
        self.buffer.append(f"  @{address}\n")
        self.buffer.append("  D=M\n")
