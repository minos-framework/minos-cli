import os
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

VERSION = "v0.1.0.dev6"

app = typer.Typer(add_completion=False)


@app.command("database")
def database(backend: str = typer.Argument(...),) -> None:
    """Set database configuration"""
    path = Path(os.getcwd()) / ".minos-project.yaml"

    if not path.exists():
        console.print(Path.cwd().name)
        console.print("No Minos project found. Consider 'minos project init'")
        raise typer.Exit()

    with path.open() as project_file:
        data = yaml.load(project_file, Loader=yaml.FullLoader)
        if "services" in data and not data["services"]:
            data["services"] = dict()

    if "services" in data and "database" in data["services"]:
        console.print("Database already set")
        raise typer.Exit()
    else:
        console.print(":wrench: Setting database config\n")
        fetcher = TemplateFetcher.from_name(f"project-database-{backend}-init", VERSION)
        processor = TemplateProcessor.from_fetcher(fetcher, Path.cwd(), defaults={"project_name": Path.cwd().name})
        processor.render()

        data["database"] = backend
        yaml.dump(data, sort_keys=False)


@app.command("discovery")
def discovery(backend: str = typer.Argument(...),) -> None:
    """Set discovery configuration"""
    path = Path(os.getcwd()) / ".minos-project.yaml"

    if not path.exists():
        console.print(Path.cwd().name)
        console.print("No Minos project found. Consider 'minos project init'")
        raise typer.Exit()

    with path.open() as project_file:
        data = yaml.load(project_file, Loader=yaml.FullLoader)
        if "services" in data and not data["services"]:
            data["services"] = dict()

    if "services" in data and "discovery" in data["services"]:
        console.print("Database already set")
        raise typer.Exit()
    else:
        console.print(":wrench: Setting discovery config\n")
        fetcher = TemplateFetcher.from_name(f"project-discovery-{backend}-init", VERSION)
        processor = TemplateProcessor.from_fetcher(fetcher, Path.cwd(), defaults={"project_name": Path.cwd().name})
        processor.render()

        data["discovery"] = backend
        yaml.dump(data, sort_keys=False)


@app.command("broker")
def broker(backend: str = typer.Argument(...),) -> None:
    """Set broker configuration"""
    path = Path(os.getcwd()) / ".minos-project.yaml"

    if not path.exists():
        console.print(Path.cwd().name)
        console.print("No Minos project found. Consider 'minos project init'")
        raise typer.Exit()

    with path.open() as project_file:
        data = yaml.load(project_file, Loader=yaml.FullLoader)
        if "services" in data and not data["services"]:
            data["services"] = dict()

    if "services" in data and "broker" in data["services"]:
        console.print("Database already set")
        raise typer.Exit()
    else:
        console.print(":wrench: Setting broker config\n")
        fetcher = TemplateFetcher.from_name(f"project-broker-{backend}-init", VERSION)
        processor = TemplateProcessor.from_fetcher(fetcher, Path.cwd(), defaults={"project_name": Path.cwd().name})
        processor.render()

        data["broker"] = backend
        yaml.dump(data, sort_keys=False)


@app.command("api-gateway")
def apigateway(backend: str = typer.Argument(...),) -> None:
    """Set api-gateway configuration"""
    path = Path(os.getcwd()) / ".minos-project.yaml"

    if not path.exists():
        console.print(Path.cwd().name)
        console.print("No Minos project found. Consider 'minos project init'")
        raise typer.Exit()

    with path.open() as project_file:
        data = yaml.load(project_file, Loader=yaml.FullLoader)
        if "services" in data and not data["services"]:
            data["services"] = dict()

    if "services" in data and "api-gateway" in data["services"]:
        console.print("Database already set")
        raise typer.Exit()
    else:
        console.print(":wrench: Setting api-gateway config\n")
        fetcher = TemplateFetcher.from_name(f"project-apigateway-{backend}-init", VERSION)
        processor = TemplateProcessor.from_fetcher(fetcher, Path.cwd(), defaults={"project_name": Path.cwd().name})
        processor.render()

        data["broker"] = backend
        yaml.dump(data, sort_keys=False)


@app.callback()
def callback():
    """Minos project CLI."""
    console.print(":gift: Set configuration variables :gift:\n")
