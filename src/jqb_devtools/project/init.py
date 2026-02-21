from pathlib import Path
from typing import Annotated
import inquirer
import typer
import subprocess
import os
import yaml
from ..utils.config import get_config_path

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
    cfg_path = get_config_path()
    with open(cfg_path, 'r') as config_file:
        cfg_data = yaml.safe_load(config_file)

    questions: list[inquirer.questions.Question] = []

    # Check whether git's been initialized already before letting the question be asked
    git_already_initialized = cwd.joinpath(".git").exists()

    if not git and not git_already_initialized:
        questions.append(
            inquirer.Confirm("git", message="Initialize as a Git repository?", default=True))

    # Build configuration file per DevTools configuration
    pending_cfg = {}
    if cfg_data['ides']:
        ides = {item['name']: item['executable'] for item in cfg_data['ides']}
        questions.append(inquirer.List(
            "default_ide",
            message="Select a default IDE for this project to open in",
            choices=ides
        ))

        pending_cfg["default_ide"] = lambda selected_cfg: ides[selected_cfg["default_ide"]]


    final_cfg = {}
    if questions:
        answers = inquirer.prompt(questions)

        # Initialize the project as a git repo
        if "git" in answers and answers["git"]:
            subprocess.run(["git", "init"])

        # Save the answers of all asked questions
        for pending_cfg_key, pending_cfg_value in pending_cfg.items():
            final_cfg[pending_cfg_key] = pending_cfg_value(answers)

    # Create the project's JQ DevTool files
    os.makedirs("./.jqb-devtools", exist_ok=True)
    with open("./.jqb-devtools/config.yaml", "w") as project_config_file:
        yaml.dump(final_cfg, project_config_file)

    print("Initialization complete!")

if __name__ == "__main__":
    app()