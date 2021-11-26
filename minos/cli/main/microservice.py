from pathlib import (
    Path,
)

import typer

from ..consoles import (
    console,
)
from ..constants import (
    TemplateCategory,
)
from ..templating import (
    TemplateGenerator,
)

app = typer.Typer(add_completion=False)


@app.command("init")
def init() -> None:
    """Initialize a microservice on the current working directory."""

    console.print(":wrench: Initializing new Microservice...\n")
    TemplateGenerator(Path.cwd(), TemplateCategory.MICROSERVICE).build()


@app.command("new")
def new(path: Path) -> None:
    """Initialize a microservice on the given directory."""

    console.print(":wrench: Creating new Microservice...\n")
    TemplateGenerator(path, TemplateCategory.MICROSERVICE).build()


@app.callback()
def callback():
    """Minos microservice CLI."""
    console.print(":gift: Microservice Utilities :gift:\n")
