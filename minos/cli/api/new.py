from pathlib import (
    Path,
)

import typer

from ..consoles import (
    console,
)
from ..templating import (
    TemplateFetcher,
    TemplateProcessor,
)

app = typer.Typer(add_completion=False)


@app.command("project")
def new_project(path: Path) -> None:
    """Initialize a project on the given directory."""

    console.print(":wrench: Creating new Project...\n")

    fetcher = TemplateFetcher.from_name("project-init")
    processor = TemplateProcessor.from_fetcher(fetcher, path.absolute(), defaults={"project_name": path.name})
    processor.render()


@app.command("microservice")
def new_microservice(path: Path) -> None:
    """Initialize a microservice on the given directory."""

    console.print(":wrench: Creating new Microservice...\n")

    fetcher = TemplateFetcher.from_name("microservice-init")
    processor = TemplateProcessor.from_fetcher(fetcher, path.absolute(), defaults={"name": path.name})
    processor.render()


@app.callback()
def callback():
    """Creates a new project or microservice in a given path"""
