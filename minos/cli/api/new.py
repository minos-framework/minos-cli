from pathlib import (
    Path,
)

import typer

from ..consoles import (
    console,
)
from ..pathlib import (
    get_microservices_directory,
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
def new_microservice(name: str) -> None:
    """Initialize a microservice on the given directory."""

    console.print(":wrench: Creating new Microservice...\n")

    try:
        microservice_path = get_microservices_directory(Path.cwd()) / name
    except ValueError:
        console.print("No Minos project found. Consider using 'minos new project'")
        raise typer.Exit(code=1)

    fetcher = TemplateFetcher.from_name("microservice-init")
    processor = TemplateProcessor.from_fetcher(fetcher, microservice_path, defaults={"name": name})
    processor.render()

    (microservice_path / ".build_docker_compose.txt").unlink()


@app.callback()
def callback():
    """Creates a new project or microservice in a given path"""
