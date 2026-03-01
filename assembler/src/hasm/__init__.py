import click
import io
import os
from .parser import Parser


def validate_ext(ctz, self, value: io.TextIOWrapper | None) -> io.TextIOWrapper | None:
    if value is None:
        return None
    if not value.name.endswith(".asm"):
        raise click.BadParameter("must be .asm file")
    return value


@click.command()
@click.argument(
    "filename", type=click.File(mode="r"), required=False, callback=validate_ext
)
@click.option("-v", "--verbose", is_flag=True)
def hack(filename: io.TextIOWrapper | None, verbose: bool) -> None:
    "Assembles Hack files"
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
    if verbose:
        print(f"Files: {files}")

    for name, content in files.items():
        parser = Parser(name, content)
        parser.parse()
    # for name, content in assembled_files.items():
    #     try:
    #         with open(name, "w") as file:
    #             file.write(content)
    #     except Exception:
    #         print(f"Unable to write file {name}")
