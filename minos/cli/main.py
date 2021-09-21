import typer

app = typer.Typer()


@app.command("init")
def init():
    """TODO"""
    typer.echo("Initializing...")


@app.command("new")
def new():
    """TODO"""
    typer.echo("Creating new...")


@app.callback()
def callback():
    """Minos microservice CLI."""


def main():  # pragma: no cover
    """CLI's main function."""
    app()
