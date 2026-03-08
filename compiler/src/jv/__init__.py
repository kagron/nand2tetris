import click
import io
import os

from jv.codewriter import CodeWriter
from .util import print_verbose, set_verbose
from .parser import CommandType, Parser


def parse_file(parser: Parser):
    try:
        filename = parser.filename.replace(".vm", ".asm")
        with open(filename, "w") as f:
            code_writer = CodeWriter(f)
            # Initialize SP to 256.  Likely only needed in CPU emulator
            f.write("  @256\n")
            f.write("  D=A\n")
            f.write("  @SP\n")
            f.write("  M=D\n")
            while parser.hasMoreLines():
                parser.advance()
                # If tokens = 0, in comment line
                if len(parser.tokens) == 0:
                    continue
                command_type = parser.command_type()
                command = parser.tokens[0]

                if command_type == CommandType.C_ARITHMETIC:
                    code_writer.write_arithmetic(parser.arg1())
                elif command_type == CommandType.C_PUSH:
                    code_writer.write_push_pop(command, parser.arg1(), parser.arg2())
                elif command_type == CommandType.C_POP:
                    code_writer.write_push_pop(command, parser.arg1(), parser.arg2())

    except Exception as e:
        print(f"Exception: {e}")


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

    for name, content in files.items():
        print_verbose(f"{name} found.")
        parser = Parser(name, content)
        parse_file(parser)
    return
