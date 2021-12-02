from pathlib import (
    Path,
)

import typer

from ..consoles import (
    console,
)
from ..templating import (
    MICROSERVICE_INIT,
    TemplateProcessor,
)

app = typer.Typer(add_completion=False)


@app.command("init")
def init() -> None:
    """Initialize a microservice on the current working directory."""

    console.print(":wrench: Initializing new Microservice...\n")
    processor = TemplateProcessor.from_fetcher(MICROSERVICE_INIT, Path.cwd())
    processor.render()


@app.command("new")
def new(path: Path) -> None:
    """Initialize a microservice on the given directory."""

    console.print(":wrench: Creating new Microservice...\n")
    processor = TemplateProcessor.from_fetcher(MICROSERVICE_INIT, path)
    processor.render()


@app.callback()
def callback():
    """Minos microservice CLI."""
    console.print(":gift: Microservice Utilities :gift:\n")