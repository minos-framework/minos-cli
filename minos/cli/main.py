from pathlib import Path
from typing import Optional

import typer

from .generator import (
    generate_microservice,
)

app = typer.Typer()


@app.command("new")
def new() -> None:
    """TODO"""
    typer.echo("Creating new...")
    generate_microservice(Path.cwd())


@app.callback()
def callback():
    """Minos microservice CLI."""


def main():  # pragma: no cover
    """CLI's main function."""
    app()
