from importlib import resources
from pathlib import Path

import yaml

from jqb_devtools.app_utils.rsc_migrator import app_rsc_update_required, update_app_resources, \
    get_current_app_version_str
from jqb_devtools.app_utils.rsc_provider import get_app_config_path, get_app_dir, get_saved_project_configs_dir


def initialize_app_if_needed() -> bool:
    """
    Initializes the JQB DevTools program if that hasn't already been done.
    :return: True if initialization occurred, else False
    """
    config_path = get_app_config_path()
    if not config_path.exists():
        initialize_jqb_devtools()
        return True
    else:
        if app_rsc_update_required():
            print("Outdated JQB DevTools resources have been detected!")
            update_app_resources()
            return True

    return False


def initialize_jqb_devtools():
    """
    Initializes the JQB DevTools program directory.
    """
    initialize_config(get_app_config_path())
    initialize_cfg_templates_dir(get_app_dir())


def initialize_config(config_file: Path):
    """
    Initializes a JQB DevTools config file at the given path.
    :param config_file: The path to initialize the config file at
    """
    try:
        source_path = resources.files("jqb_devtools").joinpath("base-config.yaml")

        with source_path.open("r") as base_config:
            base_yaml = yaml.safe_load(base_config)
            base_yaml['app-config-version'] = get_current_app_version_str()
            config_file.write_text(base_config.read())
    except Exception as e:
        print(f"Failed to initialize config: {e}")


def initialize_cfg_templates_dir(app_path: Path):
    """
    Initializes the config templates directory
    :param app_path: The path to create the templates directory inside
    """
    templates_dir = app_path / "cfg-templates"
    templates_dir.mkdir(parents=True, exist_ok=True)


def save_project_config(name: str, src_path: Path) -> Path:
    """
    Saves the project config at the given path to the saved project configs
    directory with the given name
    :param name: The name to save the project's config under
    :param src_path: The location of the project's config to save
    :return: The path to the saved project config
    """
    dst_path = get_saved_project_configs_dir() / f"{name}.yaml"
    with open(src_path, 'r') as src:
        with open(dst_path, 'w') as dst:
            dst.write(src.read())

    return dst_path
