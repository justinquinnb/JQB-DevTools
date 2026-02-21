import typer
from .project import app as project_app
from .config import app as config_app

app = typer.Typer()
app.add_typer(project_app, name="project")
app.add_typer(config_app, name="config")

if __name__ == "__main__":
    app()