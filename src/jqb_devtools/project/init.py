from pathlib import Path
from typing import Annotated
import inquirer
import typer
import subprocess
import os
import yaml
from ..utils.global_resources import get_config_path, initialize_if_needed

app = typer.Typer()


@app.command()
def init(
        git: Annotated[bool, typer.Option(help="Initialize as a Git project too")] = False
):
    """
    Initializes the current directory as a JQ DevTools-compatible project.
    """
    initialize_if_needed()

    cwd = Path.cwd()
    print(f"Initializing project {cwd.name}...")

    # Retrieve the pre-configured IDEs
    cfg_path = get_config_path()
    with open(cfg_path, 'r') as config_file:
        cfg_data = yaml.safe_load(config_file)

    questions: list[inquirer.questions.Question] = []

    # Check whether git's been initialized already before letting the question be asked
    git_initialized = cwd.joinpath(".git").exists()

    if not git and not git_initialized:
        questions.append(
            inquirer.Confirm("git", message="Initialize as a Git repository?", default=True))

    # Build configuration file per DevTools configuration
    pending_cfg = {}
    if cfg_data['ides']:
        ides = {item['name']: item['executable'] for item in cfg_data['ides']}
        questions.append(inquirer.List(
            "preferred_ide",
            message="Select a preferred IDE for this project to open in",
            choices=ides
        ))

        pending_cfg["preferred_ide"] = lambda selected_cfg: ides[selected_cfg["preferred_ide"]]


    final_cfg = {}
    if questions:
        answers = inquirer.prompt(questions)

        # Initialize the project as a git repo
        if "git" in answers and answers["git"]:
            subprocess.run(["git", "init"])
            git_initialized = True


        # Save the answers of all asked questions
        for pending_cfg_key, pending_cfg_value in pending_cfg.items():
            final_cfg[pending_cfg_key] = pending_cfg_value(answers)

    # Create the project's JQ DevTool files
    os.makedirs("./.jqb-devtools", exist_ok=True)
    with open("./.jqb-devtools/config.yaml", "w") as project_config_file:
        yaml.dump(final_cfg, project_config_file)

    # Git-ignore the project's JQB DevTools files if desired
    if git_initialized:
        answers = inquirer.prompt(
            [inquirer.Confirm("git_ignore_devtools_config", message="Add .jqb-devtools to .gitignore", default=True)])

        if answers["git_ignore_devtools_config"]:
            with open("./.gitignore", "a") as gitignore_file:
                gitignore_file.write(".jqb-devtools")

    print("Initialization complete!")

if __name__ == "__main__":
    app()