from pathlib import (
    Path,
)

import typer

from ..consoles import (
    console,
)
from ..templating import (
    MICROSERVICE_INIT,
    PROJECT_INIT,
    TemplateProcessor,
)

app = typer.Typer(add_completion=False)


@app.command("project")
def new_project(path: Path) -> None:
    """Initialize a project on the given directory."""

    console.print(":wrench: Creating new Project...\n")
    processor = TemplateProcessor.from_fetcher(PROJECT_INIT, path.absolute(), defaults={"project_name": path.name})
    processor.render()


@app.command("microservice")
def new_microservice(path: Path) -> None:
    """Initialize a microservice on the given directory."""

    console.print(":wrench: Creating new Microservice...\n")
    processor = TemplateProcessor.from_fetcher(MICROSERVICE_INIT, path.absolute(), defaults={"name": path.name})
    processor.render()


@app.callback()
def callback():
    """Minos microservice CLI."""
    console.print(":gift: Microservice Utilities :gift:\n")
