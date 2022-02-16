from pathlib import (
    Path,
)

import typer
import yaml

from ..consoles import (
    console,
)
from ..pathlib import (
    get_project_target_directory,
)
from ..templating import (
    TemplateFetcher,
    TemplateProcessor,
)

app = typer.Typer(add_completion=False)


@app.command("database")
def database(backend: str = typer.Argument(...)) -> None:
    """Set database configuration"""
    set_service("database", backend)


@app.command("discovery")
def discovery(backend: str = typer.Argument(...)) -> None:
    """Set discovery configuration"""
    set_service("discovery", backend)


@app.command("broker")
def broker(backend: str = typer.Argument(...)) -> None:
    """Set broker configuration"""
    set_service("broker", backend)


@app.command("api-gateway")
def api_gateway(backend: str = typer.Argument(...)) -> None:
    """Set api-gateway configuration"""
    set_service("apigateway", backend)


def set_service(service: str, backend: str) -> None:
    """Set configuration"""

    try:
        project_path = get_project_target_directory(Path.cwd())
    except ValueError:
        console.print("No Minos project found. Consider 'minos new project'")
        raise typer.Exit(code=1)

    config_path = project_path / ".minos-project.yaml"

    with config_path.open() as file:
        data = yaml.safe_load(file)
        if "services" in data and not data["services"]:
            data["services"] = dict()

        if "services" in data and service in data["services"]:
            console.print(f"{service} already set")
            raise typer.Exit(code=1)

    console.print(f":wrench: Setting {service} config\n")
    fetcher = TemplateFetcher.from_name(f"project-{service}-{backend}-init")
    processor = TemplateProcessor.from_fetcher(
        fetcher, project_path, defaults={"project_name": project_path.name}, context={service: backend}
    )
    processor.render()

    with config_path.open("w") as file:
        data["services"][service] = backend
        yaml.dump(data, file, sort_keys=False)


@app.callback()
def callback():
    """Sets project services such as database or broker"""
