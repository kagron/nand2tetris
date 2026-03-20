import click
import io
import os

from jc.spec import KeywordType, TokenType
from jc.tokenizer import Tokenizer
from jc.abstract_engine import AbstractCompileEngine
from jc.xml_compile_engine import XmlCompileEngine

from .util import print_verbose, set_verbose


def analyze(tokenizer: Tokenizer, compiler: AbstractCompileEngine, tokens_only: bool):
    if tokens_only:
        compiler.buffer.append("<tokens>\n")

    token_generator = tokenizer.try_tokenize()
    first_token = next(token_generator)

    compiler.set_current_token(first_token)
    compiler.set_token_generator(token_generator)

    if tokens_only:
        compiler.compile_term()
    elif (
        first_token.token_type == TokenType.KEYWORD
        and tokenizer.key_word() == KeywordType.CLASS
    ):
        compiler.compile_class()

    if tokens_only:
        compiler.buffer.append("</tokens>\n")


def get_engine(output_xml: bool, buffer: list[str]) -> AbstractCompileEngine:
    return XmlCompileEngine(buffer)


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
@click.option("-x", "--output-xml", is_flag=True)
@click.option("-t", "--tokens-only", is_flag=True)
def compile(
    filename: io.TextIOWrapper | None,
    verbose: bool,
    output_xml: bool,
    tokens_only: bool,
) -> None:
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
    print_verbose(f"output_xml: {output_xml}")
    print_verbose(f"tokens_only: {tokens_only}")

    ext = ".vm"
    if tokens_only:
        ext = "T.xml"
    elif output_xml:
        ext = ".xml"
    try:
        for name, content in files.items():
            with open(f"{name[:-5]}{ext}", "w") as f:
                tokenizer = Tokenizer(f.name, content)
                buffer = list()
                analyze(tokenizer, get_engine(output_xml, buffer), tokens_only)
                f.writelines(buffer)
    except Exception as e:
        print(f"Exception: {e}")
    return
