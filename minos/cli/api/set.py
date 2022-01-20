from pathlib import (
    Path,
)

import typer

from ..consoles import (
    console,
)
from ..templating import (
    PROJECT_INIT,
    TemplateProcessor,
)

app = typer.Typer(add_completion=False)


@app.command("database")
def database() -> None:
    """Set database configuration"""

    console.print(":wrench: Setting database config\n")
    processor = TemplateProcessor.from_fetcher(PROJECT_INIT, Path.cwd(), defaults={"project_name": Path.cwd().name})
    processor.render()

@app.callback()
def callback():
    """Minos project CLI."""
    console.print(":gift: Set configuration variables :gift:\n")
