from jv.util import append_verbose

ret_i_dict: dict[str, int] = dict()


class CodeWriter:
    def __init__(self, filename: str) -> None:
        self.filename = filename[:-3]
        self.eqi = 0
        self.gti = 0
        self.lti = 0
        self.buffer: list[str] = list()

    def write_arithmetic(self, command: str, current_fun: str):
        """
        Writes assembly instructions for arithmetic instructions `add`, `sub`
        `neg`, `eq`, `gt`, `lt`, `and`, `or`, and `not`
        """
        self._write_verbose(f"// write_arithmetic {command}")

        if command == "add":
            self._pop_d()
            self._write_line("  A=M-1")
            self._write_line("  M=D+M")
        elif command == "sub":
            self._pop_d()
            self._write_line("  A=M-1")
            self._write_line("  M=M-D")
        elif command == "neg":
            self._pop_d()
            self._write_line("  A=M")
            self._write_line("  M=-D")
            self._write_line("  @SP")
            self._write_line("  M=M+1")
        elif command == "eq":
            self._pop_d()
            self._write_line("  A=M-1")
            self._write_line("  D=D-M")
            self._decSP()
            self._write_line(f"  @{current_fun}$ELSE_EQ_{self.eqi}")
            self._write_line("  D;JNE")
            self._write_line("  D=-1")
            self._push_d()
            self._write_line(f"  @{current_fun}$DONE_EQ_{self.eqi}")
            self._write_line("  0;JMP")
            self._write_line(f"({current_fun}$ELSE_EQ_{self.eqi})")
            self._write_line("  D=0")
            self._push_d()
            self._write_line(f"({current_fun}$DONE_EQ_{self.eqi})")
            self.eqi += 1
        elif command == "gt":
            self._pop_d()
            self._write_line("  A=M-1")
            self._write_line("  D=M-D")
            self._decSP()
            self._write_line(f"  @{current_fun}$ELSE_GT_{self.gti}")
            self._write_line("  D;JLE")
            self._write_line("  D=-1")
            self._push_d()
            self._write_line(f"  @{current_fun}$DONE_GT_{self.gti}")
            self._write_line("  0;JMP")
            self._write_line(f"({current_fun}$ELSE_GT_{self.gti})")
            self._write_line("  D=0")
            self._push_d()
            self._write_line(f"({current_fun}$DONE_GT_{self.gti})")
            self.gti += 1
        elif command == "lt":
            self._pop_d()
            self._write_line("  A=M-1")
            self._write_line("  D=M-D")
            self._decSP()
            self._write_line(f"  @{current_fun}$ELSE_LT_{self.lti}")
            self._write_line("  D;JGE")
            self._write_line("  D=-1")
            self._push_d()
            self._write_line(f"  @{current_fun}$DONE_LT_{self.lti}")
            self._write_line("  0;JMP")
            self._write_line(f"({current_fun}$ELSE_LT_{self.lti})")
            self._write_line("  D=0")
            self._push_d()
            self._write_line(f"({current_fun}$DONE_LT_{self.lti})")
            self.lti += 1
        elif command == "and":
            self._pop_d()
            self._write_line("  A=M-1")
            self._write_line("  M=D&M")
        elif command == "or":
            self._pop_d()
            self._write_line("  A=M-1")
            self._write_line("  M=D|M")
        elif command == "not":
            self._pop_d()
            self._write_line("  A=M")
            self._write_line("  M=!D")
            self._incSP()

    def write_push_pop(self, command: str, segment: str, index: int):
        """Writes assembly instructions for `push` and `pop` instructions"""
        if command == "push":
            self._push(segment, index)
        elif command == "pop":
            self._pop(segment, index)

    def write_label(self, label: str):
        """Writes assembly instructions for `label`.  Injects label `label`."""
        self._write_verbose(f"// Label {label}")
        self._write_line(f"({label})")

    def write_if(self, label: str):
        """
        Writes assembly instructions for `if-goto`.  Pops stack to D, jumps to
        `label` if `D` register is not equal to `0`
        """

        self._write_verbose(f"// If-goto {label}")
        self._pop_d()
        self._write_verbose(f"// Checking if-goto {label}")
        self._write_line(f"  @{label}")
        self._write_line("  D;JNE")

    def write_goto(self, label: str):
        """Writes assembly instructions for `goto`.  Jumps to `label`."""
        self._write_verbose(f"// Goto {label}")
        self._write_line(f"  @{label}")
        self._write_line("  0;JMP")

    def write_function(self, function_name: str, numVars: int):
        """
        Writes assembly instructions for `function`.  Injects function entry
        label, then pushes `0` to stack for `numVars` times
        """
        self._write_verbose(f"// Function {function_name} {numVars}")

        self._write_line(f"({function_name})")
        for i in range(numVars):
            self._write_verbose(f"// Allocating local {i} for {function_name}")
            self._write_line("  @0")
            self._write_line("  D=A")
            self._push_d()

    def write_call(self, function_name: str, numArgs: int):
        """
        Writes assembly instructions for `call` function.  Pushes return address,
        `LCL`, `ARG`, `THIS`, and `THAT` to the stack.  Repositions `ARG` to
        `SP` - `5` - `numArgs` Repositions LCL to SP.  Adds return address label
        at the end
        """
        global ret_i_dict
        if ret_i_dict.get(function_name, None) is None:
            ret_i_dict[function_name] = 0

        ret_i = ret_i_dict[function_name]
        fun_label = f"{function_name}"
        ret_label = f"{fun_label}$ret.{ret_i}"
        self._write_verbose(f"// Call {function_name} {numArgs}")
        self._write_verbose("// Pushing return address to stack")
        self._write_line(f"  @{ret_label}")
        self._write_line("  D=A")
        self._push_d()
        self._write_verbose("// Pushing LCL to stack")
        self._write_line("  @LCL")
        self._write_line("  D=M")
        self._push_d()
        self._write_verbose("// Pushing ARG to stack")
        self._write_line("  @ARG")
        self._write_line("  D=M")
        self._push_d()
        self._write_verbose("// Pushing THIS to stack")
        self._write_line("  @THIS")
        self._write_line("  D=M")
        self._push_d()
        self._write_verbose("// Pushing THAT to stack")
        self._write_line("  @THAT")
        self._write_line("  D=M")
        self._push_d()
        self._write_verbose("// Setting ARG to SP-5-numArgs")
        self._write_line("  @SP")
        self._write_line("  D=M")
        self._write_line("  @5")
        self._write_line("  D=D-A")
        if numArgs > 0:
            self._write_line(f"  @{numArgs}")
            self._write_line("  D=D-A")
        self._write_line("  @ARG")
        self._write_line("  M=D")
        self._write_line("  @SP")
        self._write_line("  D=M")
        self._write_line("  @LCL")
        self._write_line("  M=D")
        self._write_line(f"  @{fun_label}")
        self._write_line("  0;JMP")
        self._write_line(f"({ret_label})")
        ret_i_dict[function_name] = ret_i + 1

    def write_return(self):
        """
        Writes assembly instructions for `return`.  Stores LCL - 5 into RAM[14]
        as the return address.  Pops stack and stores it at current ARG.
        Repositions SP to ARG + 1. Restores THAT, THIS, ARG, and LCL.  Goes
        to return address
        """
        self._write_verbose("// Return")
        self._write_line("  @LCL")
        self._write_line("  D=M")
        self._write_line("  @R13")
        self._write_line("  M=D")  # Beginning of our frame(R13) = LCL
        self._write_line("  @5")
        self._write_line("  A=D-A")
        self._write_line("  D=M")  # D=*(frame - 5)
        self._write_line("  @R14")
        self._write_verbose("// Storing returnAddr as LCL-5 into R14")
        self._write_line("  M=D")  # retAddr(R14) = *(frame - 5)
        self._pop_d()
        self._write_line("  @ARG")
        self._write_line("  A=M")
        self._write_verbose("// Popping D into ARG dereferenced value")
        self._write_line("  M=D")  # *ARG = pop()
        self._write_line("  @ARG")
        self._write_line("  D=M")
        self._write_line("  @SP")
        self._write_verbose("// SP = Arg + 1")
        self._write_line("  M=D+1")  # SP = ARG + 1

        self._write_line("  @R13")
        self._write_line("  D=M")
        self._write_line("  @1")
        self._write_line("  A=D-A")
        self._write_line("  D=M")
        self._write_line("  @THAT")
        self._write_line("  M=D")  # THAT = *(frame - 1)

        self._write_line("  @R13")
        self._write_line("  D=M")
        self._write_line("  @2")
        self._write_line("  A=D-A")
        self._write_line("  D=M")
        self._write_line("  @THIS")
        self._write_line("  M=D")  # THIS = *(frame - 2)

        self._write_line("  @R13")
        self._write_line("  D=M")
        self._write_line("  @3")
        self._write_line("  A=D-A")
        self._write_line("  D=M")
        self._write_line("  @ARG")
        self._write_line("  M=D")  # ARG = *(frame - 3)

        self._write_line("  @R13")
        self._write_line("  D=M")
        self._write_line("  @4")
        self._write_line("  A=D-A")
        self._write_line("  D=M")
        self._write_line("  @LCL")
        self._write_line("  M=D")  # LCL = *(frame - 4)

        self._write_line("  @R14")
        self._write_line("  A=M")
        self._write_line("  0;JMP")  # goto retAddr

    def _push_d(self):
        """Pushes D register onto stack.  A will be at @SP"""
        self._write_verbose("// Push D")
        self._write_line("  @SP")
        self._write_line("  A=M")
        self._write_line("  M=D")
        self._incSP()

    def _pop_d(self):
        """Pops stack into D register.  A will be at @SP"""
        self._write_verbose("// Pop D")
        self._write_line("  @SP")
        self._write_line("  A=M-1")
        self._write_line("  D=M")
        self._decSP()

    def _incSP(self):
        """Incremenets stack pointer.  A will be at @SP"""
        self._write_verbose("// Incrementing SP")
        self._write_line("  @SP")
        self._write_line("  M=M+1")

    def _decSP(self):
        """Decrements stack pointer.  A will be at @SP"""
        self._write_verbose("// Decrementing SP")
        self._write_line("  @SP")
        self._write_line("  M=M-1")

    def _pop(self, segment: str, index: int):
        """Handles `pop` instructions"""
        self._write_verbose(f"// Pop {segment} {index}")

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
        elif segment == "this":
            if index == 0:
                self._store_d_segment("THIS")
            else:
                self._store_d_index("THIS", index)
        elif segment == "that":
            if index == 0:
                self._store_d_segment("THAT")
            else:
                self._store_d_index("THAT", index)
        elif segment == "pointer":
            self._store_d_segment("THIS" if index == 0 else "THAT")
        elif segment == "temp":
            assert index >= 0 and index <= 7, "Index must be between 0-7"
            self._store_d_ram(f"R{5 + index}")
        elif segment == "static":
            self._store_d_ram(f"{self.filename}.{index}")

    def _push(self, segment: str, index: int):
        """Handles `push` instructions"""
        self._write_verbose(f"// Push {segment} {index}")
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
        elif segment == "this":
            if index == 0:
                self._load_segment_d("THIS")
            else:
                self._load_index_d("THIS", index)
        elif segment == "that":
            if index == 0:
                self._load_segment_d("THAT")
            else:
                self._load_index_d("THAT", index)
        elif segment == "pointer":
            self._load_segment_d("THIS" if index == 0 else "THAT")
        elif segment == "constant":
            assert index >= 0 and index < 2**15, "Index must be between 0-32767"
            self._write_line(f"  @{index}")
            self._write_line("  D=A")
        elif segment == "temp":
            assert index >= 0 and index <= 7, "Index must be between 0-7"
            self._load_ram_d(f"R{5 + index}")
        elif segment == "static":
            self._load_ram_d(f"{self.filename}.{index}")

        self._push_d()

    def _store_d_index(self, segment: str, index: int):
        """Stores D register at base segment + index"""
        # TODO: Can I optimize this without using R13 for storing segment + index?
        self._write_verbose(f"// Storing D at segment '{segment}' index '{index}'")
        self._write_line(f"  @{index}")
        self._write_line("  D=A")
        self._write_line(f"  @{segment}")
        self._write_line("  D=D+M")
        self._write_line("  @R13")
        self._write_line("  M=D")

        self._pop_d()

        self._write_verbose(
            f"// Popping D into calculated segment '{segment}' index '{index}'"
        )
        self._write_line("  @R13")
        self._write_line("  A=M")
        self._write_line("  M=D")

    def _store_d_segment(self, segment: str):
        """Stores D register at base segment"""
        self._write_verbose(f"// Storing D at segment '{segment}'")
        self._pop_d()
        self._write_line(f"  @{segment}")
        self._write_line("  A=M")
        self._write_line("  M=D")

    def _store_d_ram(self, address: str):
        """Goes to RAM[address] and stores D Register there"""
        self._write_verbose(f"// Storing D at RAM['{address}']")
        self._pop_d()
        self._write_line(f"  @{address}")
        self._write_line("  M=D")

    def _load_index_d(self, segment: str, index: int):
        """Goes to base segment + index and stores value into D Register"""
        self._write_verbose(f"// Loading D from segment '{segment}' index '{index}'")
        self._write_line(f"  @{index}")
        self._write_line("  D=A")
        self._write_line(f"  @{segment}")
        self._write_line("  A=D+M")
        self._write_line("  D=M")

    def _load_segment_d(self, segment: str):
        """Goes to base segment and stores value into D Register"""
        self._write_verbose(f"// Loading D from segment '{segment}'")
        self._write_line(f"  @{segment}")
        self._write_line("  A=M")
        self._write_line("  D=M")

    def _load_ram_d(self, address: str):
        """Goes to RAM[address] and stores value into D Register"""
        self._write_verbose(f"// Loading D from RAM['{address}']")
        self._write_line(f"  @{address}")
        self._write_line("  D=M")

    def _write_verbose(self, line: str):
        append_verbose(self.buffer, line)

    def _write_line(self, line: str):
        self.buffer.append(f"{line}\n")
