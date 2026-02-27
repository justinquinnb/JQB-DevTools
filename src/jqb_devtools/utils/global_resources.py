from pathlib import Path
from platformdirs import PlatformDirs
from importlib import resources


def get_app_path() -> Path:
    """
    Gets the Path to the JQB DevTools program (app) directory.
    :return: The Path to the JQB DevTools program directory on the current OS
    """
    return PlatformDirs("DevTools", "JQB", ensure_exists=True).user_data_path


def get_config_path() -> Path:
    """
    Gets the Path to the JQB DevTools config file.
    :return: The Path to the JQB DevTools config file on the current OS
    """
    return get_app_path() / "config.yaml"


def initialize_if_needed() -> bool:
    """
    Initializes the JQB DevTools program if that hasn't already been done.
    :return: True if initialization occurred, else False
    """
    config_path = get_config_path()
    if not config_path.exists():
        initialize_jqb_devtools()
        return True

    return False


def initialize_jqb_devtools():
    """
    Initializes the JQB DevTools program directory.
    """
    initialize_config(get_config_path())
    initialize_cfg_templates_dir(get_app_path())

def initialize_config(config_file: Path):
    """
    Initializes a JQB DevTools config file at the given path.
    :param config_file: The path to initialize the config file at
    :return:
    """
    try:
        source_path = resources.files("jqb_devtools").joinpath("base-config.yaml")

        with source_path.open("r") as base_config:
            config_file.write_text(base_config.read())
    except Exception as e:
        print(f"Failed to initialize config: {e}")
