from pathlib import (
    Path,
)

import typer

from ..generators import (
    MicroserviceGenerator,
)

app = typer.Typer(add_completion=False)


@app.command("init")
def init() -> None:
    """Initialize a microservice on the current working directory."""

    typer.echo("Initializing...")
    MicroserviceGenerator(Path.cwd()).build()


@app.command("new")
def new(path: Path) -> None:
    """Initialize a microservice on the given directory."""

    typer.echo("Creating new...")
    MicroserviceGenerator(path).build()


@app.callback()
def callback():
    """Minos microservice CLI."""
