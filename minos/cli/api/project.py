from pathlib import (
    Path,
)

import typer

from ..consoles import (
    console,
)
from ..templating import (
    PROJECT_INIT,
    TemplateProcessor,
)

app = typer.Typer(add_completion=False)


@app.command("init")
def init() -> None:
    """Initialize a project on the current working directory."""

    console.print(":wrench: Initializing new Project...\n")
    processor = TemplateProcessor.from_fetcher(PROJECT_INIT, Path.cwd(), defaults={"project_name": Path.cwd().name})
    processor.render()


@app.command("new")
def new(path: Path) -> None:
    """Initialize a project on the given directory."""

    console.print(":wrench: Creating new Project...\n")
    processor = TemplateProcessor.from_fetcher(PROJECT_INIT, path.absolute(), defaults={"project_name": path.name})
    processor.render()


@app.callback()
def callback():
    """Minos project CLI."""
    console.print(":gift: Project Utilities :gift:\n")
