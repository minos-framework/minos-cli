import typer

from ..consoles import (
    console,
)
from .microservice import app as microservices_app

app = typer.Typer(add_completion=False)
app.add_typer(microservices_app, name="microservice")


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
