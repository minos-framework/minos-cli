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
    console.rule(":robot: Minos CLI :robot:")


def main():  # pragma: no cover
    """CLI's main function."""
    app()
