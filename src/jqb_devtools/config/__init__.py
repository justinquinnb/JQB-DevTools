import typer

from .locate import app as locate_app

app = typer.Typer()
app.add_typer(locate_app)
