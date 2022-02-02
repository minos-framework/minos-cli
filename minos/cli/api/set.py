from pathlib import (
    Path,
)

import typer
import yaml

from ..consoles import (
    console,
)
from ..templating import (
    TemplateFetcher,
    TemplateProcessor,
)

VERSION = "v0.1.0.dev7"

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
    path = Path.cwd() / ".minos-project.yaml"

    if not path.exists():
        console.print("No Minos project found. Consider 'minos project init'")
        raise typer.Exit(code=1)

    with path.open() as project_file:
        data = yaml.safe_load(project_file)
        if "services" in data and not data["services"]:
            data["services"] = dict()

        if "services" in data and service in data["services"]:
            console.print(f"{service} already set")
            raise typer.Exit(code=1)
        else:
            console.print(f":wrench: Setting {service} config\n")
            fetcher = TemplateFetcher.from_name(f"project-{service}-{backend}-init", VERSION)
            processor = TemplateProcessor.from_fetcher(fetcher, Path.cwd(), defaults={"project_name": Path.cwd().name})
            processor.render()

            with path.open("w") as project_file_write:
                data["services"][service] = backend
                yaml.dump(data, project_file_write, sort_keys=False)


@app.callback()
def callback():
    """Sets project services such as database or broker"""
