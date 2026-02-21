from pathlib import Path
from typing import Annotated
import typer
import subprocess

app = typer.Typer()


@app.command()
def init(
        git: Annotated[bool, typer.Option(help="Initialize as a Git project too")] = False
):
    """
    Initializes the current directory as a JQ DevTools-compatible project.
    """
    print(f"Initializing project {Path.cwd().name}...")
    if git:
        print("Initializing Git repository...")
        subprocess.run(["git", "init"])
        print("Git repository initialized.")



if __name__ == "__main__":
    app()