import click
import io
import os

from jv.codewriter import CodeWriter
from .util import print_verbose, set_verbose
from .parser import CommandType, Parser


def init_pointer(f: io.TextIOWrapper, pointer_name: str, base_address_loc: int):
    """Initializes pointer `pointer_name` to address location `base_address_loc`"""
    f.write(f"@{base_address_loc}\n")
    f.write("D=A\n")
    f.write(f"@{pointer_name}\n")
    f.write("M=D\n")


def init_program(f: io.TextIOWrapper):
    """Initializes program by calling Sys.init at beginning of program"""
    f.writelines(["@Sys.init\n", "0;JMP\n"])


def parse_file(parser: Parser, filename: str, f: io.TextIOWrapper):
    code_writer = CodeWriter(filename)
    current_fun = ""

    while parser.hasMoreLines():
        parser.advance()

        # If tokens = 0, in comment line
        if len(parser.tokens) == 0:
            continue

        command_type = parser.command_type()
        command = parser.tokens[0]

        print_verbose(f"command_type: {command_type}")
        print_verbose(f"command: {command}")
        print_verbose(f"current_fun: {current_fun}")

        if command_type == CommandType.C_ARITHMETIC:
            code_writer.write_arithmetic(parser.arg1(), current_fun)
        elif command_type == CommandType.C_PUSH:
            code_writer.write_push_pop(command, parser.arg1(), parser.arg2())
        elif command_type == CommandType.C_POP:
            code_writer.write_push_pop(command, parser.arg1(), parser.arg2())
        elif command_type == CommandType.C_LABEL:
            code_writer.write_label(f"{current_fun}${parser.arg1()}")
        elif command_type == CommandType.C_IF:
            code_writer.write_if(f"{current_fun}${parser.arg1()}")
        elif command_type == CommandType.C_GOTO:
            code_writer.write_goto(f"{current_fun}${parser.arg1()}")
        elif command_type == CommandType.C_FUNCTION:
            current_fun = parser.arg1()
            code_writer.write_function(current_fun, parser.arg2())
        elif command_type == CommandType.C_CALL:
            code_writer.write_call(parser.arg1(), parser.arg2())
        elif command_type == CommandType.C_RETURN:
            code_writer.write_return()
        f.writelines(code_writer.buffer)
        code_writer.buffer.clear()


def validate_ext(ctz, self, value: io.TextIOWrapper | None) -> io.TextIOWrapper | None:
    if value is None:
        return None
    if not value.name.endswith(".vm"):
        raise click.BadParameter("must be .vm file")
    return value


@click.command()
@click.argument(
    "filename", type=click.File(mode="r"), required=False, callback=validate_ext
)
@click.option("-v", "--verbose", is_flag=True)
def translate(filename: io.TextIOWrapper | None, verbose: bool) -> None:
    """Translates Jack VM code into Hack Assembly"""
    files: dict[str, str] = dict()
    if filename is not None:
        files[filename.name] = filename.read()
        filename.close()
    else:
        for file in os.listdir("."):
            if file.endswith(".vm"):
                try:
                    with open(file, "r") as file:
                        files[file.name] = file.read()
                except Exception:
                    print(f"The file {file} could not be opened.")

    if len(files) == 0:
        print("No Jack .vm files found in current directory")
        exit(1)

    set_verbose(verbose)
    print_verbose(f"Files: {files}")

    try:
        with open("Out.asm", "w") as f:
            init_pointer(f, "SP", 256)
            init_program(f)
            for name, content in files.items():
                parser = Parser(name, content)
                parse_file(parser, name, f)
    except Exception as e:
        print(f"Exception: {e}")
