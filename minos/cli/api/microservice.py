from pathlib import (
    Path,
)
from typing import (
    Optional,
)

import typer

from ..consoles import (
    console,
)
from ..deploying import (
    MicroserviceDeployer,
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
    processor = TemplateProcessor.from_fetcher(MICROSERVICE_INIT, Path.cwd(), defaults={"name": Path.cwd().name})
    processor.render()


@app.command("new")
def new(path: Path) -> None:
    """Initialize a microservice on the given directory."""

    console.print(":wrench: Creating new Microservice...\n")
    processor = TemplateProcessor.from_fetcher(MICROSERVICE_INIT, path.absolute(), defaults={"name": path.name})
    processor.render()


@app.command("deploy")
def deploy(
    name: Optional[str] = typer.Argument(None, help="TODO"), path: Path = typer.Option(Path.cwd(), help="TODO")
) -> None:
    """TODO"""
    console.print(":wrench: Deploying the microservice...\n")
    deployer = MicroserviceDeployer(name, path)
    deployer.deploy()


@app.callback()
def callback():
    """Minos microservice CLI."""
    console.print(":gift: Microservice Utilities :gift:\n")
