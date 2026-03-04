import click
import io


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
def compile(filename: io.TextIOWrapper | None, verbose: bool) -> None:
    """Compilse Jack code into Jack VM code"""
    print("Compile")
    return
