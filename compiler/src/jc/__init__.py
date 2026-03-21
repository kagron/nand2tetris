import click
import io
import os

from jc.spec import KeywordType, TokenType
from jc.tokenizer import Tokenizer
from jc.abstract_compile_engine import AbstractCompileEngine
from jc.xml_compile_engine import XmlCompileEngine

from .util import print_verbose, set_verbose


def analyze(
    tokenizer: Tokenizer, compiler: AbstractCompileEngine, tokens_only: bool
) -> None:
    if tokens_only:
        compiler.buffer.append("<tokens>\n")

    tokenizer.tokenize_line()
    tokenizer.advance()

    if tokens_only:
        compiler.compile_term()
    elif (
        tokenizer.token_type() == TokenType.KEYWORD
        and tokenizer.key_word() == KeywordType.CLASS
    ):
        compiler.compile_class()

    if tokens_only:
        compiler.buffer.append("</tokens>\n")


def get_engine(
    output_xml: bool, tokenizer: Tokenizer, buffer: list[str]
) -> AbstractCompileEngine:
    return XmlCompileEngine(buffer, tokenizer)


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
    files: list[io.TextIOWrapper] = []
    try:
        if filename is not None:
            files.append(filename)
        else:
            files = [open(file) for file in os.listdir(".") if file.endswith(".jack")]
    except Exception as e:
        print("Could not open .jack files")
        print(f"{e}")

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
    for file in files:
        with open(f"{file.name[:-5]}{ext}", "w") as f:
            tokenizer = Tokenizer(file)
            buffer = list()
            analyze(tokenizer, get_engine(output_xml, tokenizer, buffer), tokens_only)
            f.writelines(buffer)
            f.close()
