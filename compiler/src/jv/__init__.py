import click
import io
import os
from .util import print_verbose, set_verbose


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
                except FileNotFoundError:
                    print(f"The file {file} was not found.")

    if len(files) == 0:
        print("No Jack .vm files found in current directory")
        exit(1)
    set_verbose(verbose)
    print_verbose(f"Files: {files}")

    for name, content in files.items():
        print(f"{name} found.")
    return
