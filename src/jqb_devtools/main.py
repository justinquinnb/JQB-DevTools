import typer

from .project import app as project_app

app = typer.Typer()
app.add_typer(project_app, name="project")

if __name__ == "__main__":
    app()