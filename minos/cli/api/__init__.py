import typer

from .. import (
    __version__,
)
from ..consoles import (
    console,
)
from .new import app as new_app
from .set import app as set_app
from .utils import app as utils_app

app = typer.Typer(add_completion=False)
app.add_typer(new_app, name="new")
app.add_typer(utils_app, name="utils")
app.add_typer(set_app, name="set")


@app.command()
def version():
    """CLI's version"""
    console.print(f"Minos CLI {__version__}")


@app.callback()
def callback():
    """Minos CLI."""


def main():  # pragma: no cover
    """CLI's main function."""
    console.rule("Welcome to the Minos CLI :robot:")
    console.print()

    try:
        app()
    finally:
        console.rule("See you later! :call_me_hand:")
        console.print()
