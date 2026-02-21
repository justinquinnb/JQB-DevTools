from pathlib import Path
from typing import Annotated
import inquirer
import typer
import subprocess
import os
import yaml

app = typer.Typer()


@app.command()
def init(
        git: Annotated[bool, typer.Option(help="Initialize as a Git project too")] = False
):
    """
    Initializes the current directory as a JQ DevTools-compatible project.
    """
    cwd = Path.cwd()
    print(f"Initializing project {cwd.name}...")

    # Retrieve the pre-configured IDEs
    config_path = Path(__file__).resolve().parent.parent.parent.parent / 'config.yaml'
    with open(config_path, 'r') as config_file:
        config_data = yaml.safe_load(config_file)

    ides = {item['name']: item['executable'] for item in config_data['ides']}

    # Define the configuration questions
    questions: list[inquirer.questions.Question]  = [
        inquirer.List(
            "default_ide",
            message="Select a default IDE for this project to open in",
            choices= ides
        )
    ]

    # Check whether git's been initialized already before letting the question be asked
    git_already_initialized = cwd.joinpath(".git").exists()

    if not git and not git_already_initialized:
        questions.insert(0,
                         inquirer.Confirm("git", message="Initialize as a Git repository?", default=True))

    init_cfg = inquirer.prompt(questions)

    # Act according to the configuration questions' answers
    # Initialize the project as a git repo
    if git or (not git_already_initialized and init_cfg["git"]):
        subprocess.run(["git", "init"])

    # Build the configuration from the question's responses
    configurations = {
        "default_ide_executable": ides[init_cfg["default_ide"]]
    }

    # Create the project's JQ DevTool files
    os.makedirs("./.jqb-devtools", exist_ok=True)
    with open("./.jq-devtools/config.yaml", "w") as project_config_file:
        yaml.dump(configurations, project_config_file)

if __name__ == "__main__":
    app()