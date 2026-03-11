from io import TextIOWrapper


class CodeWriter:
    def __init__(self, file: TextIOWrapper) -> None:
        self.file = file
        self.eqi = 0
        self.gti = 0
        self.lti = 0
        self.buffer: list[str] = list()
        self.file_name_no_ext = self.file.name[:-4].upper()

    def write_arithmetic(self, command: str):
        self.buffer.append(f"// write_arithmetic {command}\n")

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
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  D=D-M\n")
            self.buffer.append(f"  @{self.file_name_no_ext}_ELSE_EQ_{self.eqi}\n")
            self.buffer.append("  D;JNE\n")
            self.buffer.append("  D=-1\n")
            self._push_d()
            self.buffer.append(f"  @{self.file_name_no_ext}_DONE_EQ_{self.eqi}\n")
            self.buffer.append("  0;JMP\n")
            self.buffer.append(f"({self.file_name_no_ext}_ELSE_EQ_{self.eqi})\n")
            self.buffer.append("  D=0\n")
            self._push_d()
            self.buffer.append(f"({self.file_name_no_ext}_DONE_EQ_{self.eqi})\n")
            self.eqi += 1
        elif command == "gt":
            self._pop_d()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  D=M-D\n")
            self.buffer.append(f"  @{self.file_name_no_ext}_ELSE_GT_{self.gti}\n")
            self.buffer.append("  D;JLE\n")
            self.buffer.append("  D=-1\n")
            self._push_d()
            self.buffer.append(f"  @{self.file_name_no_ext}_DONE_GT_{self.gti}\n")
            self.buffer.append("  0;JMP\n")
            self.buffer.append(f"({self.file_name_no_ext}_ELSE_GT_{self.gti})\n")
            self.buffer.append("  D=0\n")
            self._push_d()
            self.buffer.append(f"({self.file_name_no_ext}_DONE_GT_{self.gti})\n")
            self.gti += 1
        elif command == "lt":
            self._pop_d()
            self.buffer.append("  A=M-1\n")
            self.buffer.append("  D=M-D\n")
            self.buffer.append(f"  @{self.file_name_no_ext}_ELSE_LT_{self.lti}\n")
            self.buffer.append("  D;JGE\n")
            self.buffer.append("  D=-1\n")
            self._push_d()
            self.buffer.append(f"  @{self.file_name_no_ext}_DONE_LT_{self.lti}\n")
            self.buffer.append("  0;JMP\n")
            self.buffer.append(f"({self.file_name_no_ext}_ELSE_LT_{self.lti})\n")
            self.buffer.append("  D=0\n")
            self._push_d()
            self.buffer.append(f"({self.file_name_no_ext}_DONE_LT_{self.lti})\n")
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
            self._incSP()

    def write_push_pop(self, command: str, segment: str, index: int):
        if command == "push":
            self._push(segment, index)
        elif command == "pop":
            self._pop(segment, index)

    def write_label(self, label: str):
        self.buffer.append(f"// Label {label}\n")
        self.buffer.append(f"({self.file_name_no_ext}_{label})\n")

    def write_if(self, label: str):
        self.buffer.append(f"// If-goto {label}\n")
        self._pop_d()
        self.buffer.append(f"// Checking if-goto {label}\n")
        self.buffer.append(f"  @{self.file_name_no_ext}_{label}\n")
        self.buffer.append("  D;JNE\n")

    def write_goto(self, label: str):
        self.buffer.append(f"// Goto {label}\n")
        self.buffer.append(f"  @{self.file_name_no_ext}_{label}\n")
        self.buffer.append("  0;JMP\n")

    def write_function(self, function_name: str, numVars: int):
        self.buffer.append(f"// Function {function_name} {numVars}\n")

        self.buffer.append(f"({self.file_name_no_ext}_{function_name})\n")
        for i in range(numVars):
            self.buffer.append(f"// Allocating local {i} for {function_name}\n")
            self.buffer.append("  @0\n")
            self.buffer.append("  D=A\n")
            self._push_d()

    def write_call(self, function_name: str, numVars: int):
        ret_i = 0
        self.buffer.append(f"// Call {function_name} {numVars}\n")
        self.buffer.append(f"  @{function_name}$ret.{ret_i}\n")
        self.buffer.append("  D=A\n")
        self.buffer.append("// Pushing return address to stack\n")
        self._push_d()
        self.buffer.append("  @LCL\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("// Pushing LCL to stack\n")
        self._push_d()
        self.buffer.append("  @ARG\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("// Pushing ARG to stack\n")
        self._push_d()
        self.buffer.append("  @THIS\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("// Pushing THIS to stack\n")
        self._push_d()
        self.buffer.append("  @THAT\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("// Pushing THAT to stack\n")
        self._push_d()
        self.buffer.append("  @SP\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("  @5\n")
        self.buffer.append("  D=D-A\n")
        self.buffer.append(f"  @{numVars}\n")
        self.buffer.append("  D=D-A\n")
        self.buffer.append("  @ARG\n")
        self.buffer.append("// Setting ARG to SP-5-numVars\n")
        self.buffer.append("  M=D\n")
        self.buffer.append("  @SP\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("  @LCL\n")
        self.buffer.append("  M=D\n")
        self.buffer.append(f"  @{self.file_name_no_ext}_{function_name}\n")
        self.buffer.append("  0;JMP\n")
        self.buffer.append(f"({function_name}$ret.{ret_i})\n")
        ret_i += 1

    def write_return(self):
        self.buffer.append("// Return\n")
        self.buffer.append("  @LCL\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("  @R13\n")
        self.buffer.append("  M=D\n")  # Beginning of our frame(R13) = LCL
        self.buffer.append("  @5\n")
        self.buffer.append("  A=D-A\n")
        self.buffer.append("  D=M\n")  # D=*(frame - 5)
        self.buffer.append("  @R14\n")
        self.buffer.append("// Storing returnAddr as LCL-5 into R14\n")
        self.buffer.append("  M=D\n")  # retAddr(R14) = *(frame - 5)
        self._pop_d()
        self.buffer.append("  @ARG\n")
        self.buffer.append("  A=M\n")
        self.buffer.append("// Popping D into ARG dereferenced value\n")
        self.buffer.append("  M=D\n")  # *ARG = pop()
        self.buffer.append("  @ARG\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("  @SP\n")
        self.buffer.append("// SP = Arg + 1\n")
        self.buffer.append("  M=D+1\n")  # SP = ARG + 1

        self.buffer.append("  @R13\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("  @1\n")
        self.buffer.append("  D=D-A\n")
        self.buffer.append("  @THAT\n")
        self.buffer.append("  M=D\n")  # THAT = *(frame - 1)

        self.buffer.append("  @R13\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("  @2\n")
        self.buffer.append("  D=D-A\n")
        self.buffer.append("  @THIS\n")
        self.buffer.append("  M=D\n")  # THIS = *(frame - 2)

        self.buffer.append("  @R13\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("  @3\n")
        self.buffer.append("  D=D-A\n")
        self.buffer.append("  @ARG\n")
        self.buffer.append("  M=D\n")  # ARG = *(frame - 3)

        self.buffer.append("  @R13\n")
        self.buffer.append("  D=M\n")
        self.buffer.append("  @4\n")
        self.buffer.append("  D=D-A\n")
        self.buffer.append("  @LCL\n")
        self.buffer.append("  M=D\n")  # LCL = *(frame - 4)

        self.buffer.append("  @R14\n")
        self.buffer.append("  A=M\n")
        self.buffer.append("  0;JMP\n")  # goto retAddr

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
        self.buffer.append("// Incrementing SP\n")
        self.buffer.append("  @SP\n")
        self.buffer.append("  M=M+1\n")

    def _decSP(self):
        """Decrements stack pointer.  A will be at @SP"""
        self.buffer.append("// Decrementing SP\n")
        self.buffer.append("  @SP\n")
        self.buffer.append("  M=M-1\n")

    def _pop(self, segment: str, index: int):
        self.buffer.append(f"// Pop {segment} {index}\n")

        if segment == "local":
            if index == 0:
                self._store_d_segment("LCL")
            else:
                self._store_d_index("LCL", index)
        elif segment == "argument":
            if index == 0:
                self._store_d_segment("ARG")
            else:
                self._store_d_index("ARG", index)
        elif segment == "pointer":
            self._store_d_segment("THIS" if index == 0 else "THAT")
        elif segment == "temp":
            assert index >= 0 and index <= 7, "Index must be between 0-7"
            self._store_d_ram(f"R{5 + index}")
        elif segment == "static":
            self._store_d_ram(f"{self.file_name_no_ext}_{index}")

    def _push(self, segment: str, index: int):
        self.buffer.append(f"// Push {segment} {index}\n")
        if segment == "local":
            if index == 0:
                self._load_segment_d("LCL")
            else:
                self._load_index_d("LCL", index)
        elif segment == "argument":
            if index == 0:
                self._load_segment_d("ARG")
            else:
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
            self._load_ram_d(f"{self.file_name_no_ext}_{index}")

        self._push_d()

    def _store_d_index(self, segment: str, index: int):
        """Stores D register at base segment + index"""
        # TODO: Can I optimize this without using R13 for storing segment + index?
        self.buffer.append(f"// Storing D at segment '{segment}' index '{index}'\n")
        self.buffer.append(f"  @{index}\n")
        self.buffer.append("  D=A\n")
        self.buffer.append(f"  @{segment}\n")
        self.buffer.append("  D=D+M\n")
        self.buffer.append("  @R13\n")
        self.buffer.append("  M=D\n")

        self._pop_d()

        self.buffer.append(
            f"// Popping D into calculated segment '{segment}' index '{index}'\n"
        )
        self.buffer.append("  @R13\n")
        self.buffer.append("  A=M\n")
        self.buffer.append("  M=D\n")

    def _store_d_segment(self, segment: str):
        """Stores D register at base segment"""
        self.buffer.append(f"// Storing D at segment '{segment}'\n")
        self._pop_d()
        self.buffer.append(f"  @{segment}\n")
        self.buffer.append("  A=M\n")
        self.buffer.append("  M=D\n")

    def _store_d_ram(self, address: str):
        """Goes to RAM[address] and stores D Register there"""
        self.buffer.append(f"// Storing D at RAM['{address}']\n")
        self._pop_d()
        self.buffer.append(f"  @{address}\n")
        self.buffer.append("  M=D\n")

    def _load_index_d(self, segment: str, index: int):
        """Goes to base segment + index and stores value into D Register"""
        self.buffer.append(f"// Loading D from segment '{segment}' index '{index}'\n")
        self.buffer.append(f"  @{index}\n")
        self.buffer.append("  D=A\n")
        self.buffer.append(f"  @{segment}\n")
        self.buffer.append("  A=D+M\n")
        self.buffer.append("  D=M\n")

    def _load_segment_d(self, segment: str):
        """Goes to base segment and stores value into D Register"""
        self.buffer.append(f"// Loading D from segment '{segment}'\n")
        self.buffer.append(f"  @{segment}\n")
        self.buffer.append("  A=M\n")
        self.buffer.append("  D=M\n")

    def _load_ram_d(self, address: str):
        """Goes to RAM[address] and stores value into D Register"""
        self.buffer.append(f"// Loading D from RAM['{address}']\n")
        self.buffer.append(f"  @{address}\n")
        self.buffer.append("  D=M\n")
