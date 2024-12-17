import typer
from wiever import __version__

app = typer.Typer(help="Get the current version of the Viewer CLI.")


@app.command()
def version():
    typer.echo(__version__)