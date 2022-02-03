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
def init_project() -> None:
    """Initialize a project on the current working directory."""

    console.print(":wrench: Initializing new Project...\n")
    fetcher = TemplateFetcher.from_name("project-init")
    processor = TemplateProcessor.from_fetcher(fetcher, Path.cwd(), defaults={"project_name": Path.cwd().name})
    processor.render()


@app.command("microservice")
def init_microservice() -> None:
    """Initialize a microservice on the current working directory."""

    console.print(":wrench: Initializing new Microservice...\n")
    fetcher = TemplateFetcher.from_name("microservice-init")
    processor = TemplateProcessor.from_fetcher(fetcher, Path.cwd(), defaults={"name": Path.cwd().name})
    processor.render()


@app.callback()
def callback():
    """Initializes a new project or microservice in the current path"""
