import typer
from ..app_utils.rsc_provider import get_app_config_path
from ..app_utils.rsc_initializer import initialize_app_if_needed

app = typer.Typer()


@app.command()
def locate():
    """
    Locates the JQB DevTools config file
    """
    initialize_app_if_needed()
    print(get_app_config_path())
