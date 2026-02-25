import click
import io


def validate_ext(value: io.TextIOWrapper) -> io.TextIOWrapper:
    if not value.name.endswith(".asm"):
        raise click.BadParameter("must be .asm file")
    return value


@click.command()
@click.argument(
    "filename", type=click.File(mode="r"), required=True, callback=validate_ext
)
@click.option("-v", "--verbose", is_flag=True)
def cli(filename: io.TextIOWrapper, verbose: bool) -> None:
    "Assembles Hack files"
    if verbose:
        print(f"filename: {filename}")

    content = filename.read()
    print(content)
