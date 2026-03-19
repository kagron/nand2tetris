import click
import io
import os

from jc.tokenizer import TokenType, Tokenizer

from .util import print_verbose, set_verbose


def analyze(tokenizer: Tokenizer):
    while tokenizer.has_more_tokens():
        tokenizer.advance()
        token = tokenizer.current_token
        print(token)


def validate_ext(ctz, self, value: io.TextIOWrapper | None) -> io.TextIOWrapper | None:
    if value is None:
        return None
    if not value.name.endswith(".jack"):
        raise click.BadParameter("must be .jack file")
    return value


@click.command()
@click.argument(
    "filename", type=click.File(mode="r"), required=False, callback=validate_ext
)
@click.option("-v", "--verbose", is_flag=True)
def compile(filename: io.TextIOWrapper | None, verbose: bool) -> None:
    """Compilse Jack code into Jack VM code"""
    files: dict[str, str] = dict()
    if filename is not None:
        files[filename.name] = filename.read()
        filename.close()
    else:
        for file in os.listdir("."):
            if file.endswith(".jack"):
                try:
                    with open(file, "r") as file:
                        files[file.name] = file.read()
                except Exception:
                    print(f"The file {file} could not be opened.")

    if len(files) == 0:
        print("No Jack .jack files found in current directory")
        exit(1)

    set_verbose(verbose)
    print_verbose(f"Files: {files}")

    try:
        for name, content in files.items():
            with open(f"{name[:-5]}.vm", "w") as f:
                tokenizer = Tokenizer(f.name, content)
                analyze(tokenizer)
    except Exception as e:
        print(f"Exception: {e}")
    return
