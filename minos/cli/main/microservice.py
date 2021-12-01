from pathlib import (
    Path,
)

import typer

from ..consoles import (
    console,
)
from ..templating import (
    MICROSERVICE_INIT_TEMPLATE,
    TemplateGenerator,
)

app = typer.Typer(add_completion=False)


@app.command("init")
def init() -> None:
    """Initialize a microservice on the current working directory."""

    console.print(":wrench: Initializing new Microservice...\n")
    TemplateGenerator(Path.cwd(), MICROSERVICE_INIT_TEMPLATE).build()


@app.command("new")
def new(path: Path) -> None:
    """Initialize a microservice on the given directory."""

    console.print(":wrench: Creating new Microservice...\n")
    TemplateGenerator(path, MICROSERVICE_INIT_TEMPLATE).build()


@app.callback()
def callback():
    """Minos microservice CLI."""
    console.print(":gift: Microservice Utilities :gift:\n")
