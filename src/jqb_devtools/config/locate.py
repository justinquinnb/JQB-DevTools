import typer
from ..utils.config import get_config_path

app = typer.Typer()


@app.command()
def locate():
    """
    Locates the JQB DevTools config file
    """
    print(get_config_path())
