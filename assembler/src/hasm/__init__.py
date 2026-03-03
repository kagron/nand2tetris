import click
import io
import os
from .parser import Parser
from .util import set_verbose, print_verbose


def validate_ext(ctz, self, value: io.TextIOWrapper | None) -> io.TextIOWrapper | None:
    if value is None:
        return None
    if not value.name.endswith(".asm"):
        raise click.BadParameter("must be .asm file")
    return value


def init_symbol_table() -> dict[str, int]:
    symbol_table = dict()
    with open("symbol_table.cfg", "r") as file:
        for line in file.readlines():
            split = line.split("=")
            if len(split) != 2:
                raise ValueError(
                    "Symbol table entries must be in 'symbol=value' format"
                )
            symbol_table[split[0]] = int(split[1])

    return symbol_table


@click.command()
@click.argument(
    "filename", type=click.File(mode="r"), required=False, callback=validate_ext
)
@click.option("-v", "--verbose", is_flag=True)
def hack(filename: io.TextIOWrapper | None, verbose: bool) -> None:
    "Assembles Hack files"
    # TODO: Can optimize here by streaming in files by line instead of loading all
    # into memory
    files: dict[str, str] = dict()
    if filename is not None:
        files[filename.name] = filename.read()
        filename.close()
    else:
        for file in os.listdir("."):
            if file.endswith(".asm"):
                try:
                    with open(file, "r") as file:
                        files[file.name] = file.read()
                except FileNotFoundError:
                    print(f"The file {file} was not found.")

    if len(files) == 0:
        print("No Hack .asm files found in current directory")
        exit(1)
    set_verbose(verbose)
    print_verbose(f"Files: {files}")

    for name, content in files.items():
        parser = Parser(name, content, init_symbol_table())
        parser.parse()
        new_name = f"{name[:-4]}.hack"
        try:
            with open(new_name, "w") as new_file:
                for line in parser.parsed_contents:
                    new_file.write(f"{line}\n")
        except Exception:
            print("Error writing file")
