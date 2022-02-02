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
    ProjectDeployer,
)

app = typer.Typer(add_completion=False)


@app.command("microservice")
def deploy_microservice(name: Optional[str] = typer.Argument(None), path: Path = typer.Option(Path.cwd())) -> None:
    """Deploy a Microservice."""

    console.print(":wrench: Deploying the microservice...\n")
    deployer = MicroserviceDeployer(path, name)
    deployer.deploy()


@app.command("project")
def deploy_project(path: Path = typer.Option(Path.cwd())) -> None:
    """Deploy a Project."""

    console.print(":wrench: Deploying the Project...\n")

    deployer = ProjectDeployer(path)
    deployer.deploy()


@app.callback()
def callback():
    """Deploys the project"""
