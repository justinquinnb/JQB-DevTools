import typer
from ..utils.global_resources import get_config_path, initialize_if_needed

app = typer.Typer()


@app.command()
def locate():
    """
    Locates the JQB DevTools config file
    """
    initialize_if_needed()
    print(get_config_path())
