from pathlib import (
    Path,
)

import typer

from .generator import (
    generate_microservice,
)

app = typer.Typer()


@app.command("init")
def init() -> None:
    """TODO"""
    typer.echo("Initializing...")
    generate_microservice(Path.cwd())


@app.command("new")
def new(path: Path) -> None:
    """TODO"""
    typer.echo("Creating new...")
    generate_microservice(path)


@app.callback()
def callback():
    """Minos microservice CLI."""


def main():  # pragma: no cover
    """CLI's main function."""
    app()
