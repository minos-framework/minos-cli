from pathlib import (
    Path,
)
from typing import (
    Optional,
)

import typer

from ..consoles import (
    error_console,
)
from ..templating import (
    TemplateFetcher,
    TemplateProcessor,
)

app = typer.Typer(add_completion=False)


@app.command("render-template")
def render_template(
    destination: Path, path: Optional[Path] = typer.Option(None), url: Optional[str] = typer.Option(None)
) -> None:
    """Render a template on the given destination path.

    :param destination: The path in which the template will be rendered.
    :param path: The path to the template file.
    :param url: The url to the template file.
    :return: This method does not return anything.
    """
    if path is not None:
        fetcher = TemplateFetcher.from_path(path.absolute())
    elif url is not None:
        fetcher = TemplateFetcher.from_url(url)
    else:
        error_console.print(":x: One of '--path' or '--url' must be provided")
        raise typer.Exit(code=2)

    processor = TemplateProcessor.from_fetcher(fetcher, destination.absolute())
    processor.render()


@app.callback()
def callback():
    """Minos utils for devs"""
