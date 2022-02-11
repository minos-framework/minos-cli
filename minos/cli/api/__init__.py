import typer

from ..consoles import (
    console,
)
from .init import app as init_app
from .new import app as new_app
from .set import app as set_app
from .utils import app as utils_app

app = typer.Typer(add_completion=False)
app.add_typer(init_app, name="init")
app.add_typer(new_app, name="new")
app.add_typer(utils_app, name="utils")
app.add_typer(set_app, name="set")


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
