import os
from pathlib import (
    Path,
)

import typer
import yaml

from ..consoles import (
    console,
)
from ..templating import TemplateFetcher
from ..templating import (
    TemplateProcessor,
)

app = typer.Typer(add_completion=False)


@app.command("database")
def database(
    backend: str = typer.Argument(...),
) -> None:
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
        version = "v0.1.0.dev3"
        fetcher = TemplateFetcher.from_name(f"project-database-{backend}-init", version)
        processor = TemplateProcessor.from_fetcher(
            fetcher,
            Path.cwd(),
            defaults={"project_name": Path.cwd().name}
        )
        processor.render()

        data["database"] = backend
        yaml.dump(data, sort_keys=False)


@app.callback()
def callback():
    """Minos project CLI."""
    console.print(":gift: Set configuration variables :gift:\n")
