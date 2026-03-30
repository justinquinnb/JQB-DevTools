from pathlib import Path
from importlib import resources
import yaml
from platformdirs import PlatformDirs


def get_app_dir() -> Path:
    """
    Gets the Path to the JQB DevTools program (app) directory.
    :return: The Path to the JQB DevTools program directory on the current OS
    """
    return PlatformDirs("DevTools", "JQB", ensure_exists=True).user_data_path


def get_base_app_config_path() -> Path:
    """
    Gets the Path to the base JQB DevTools app config file.
    :return: The Path to the base JQB DevTools app config file
    """
    base_app_cfg_rsc = resources.files("jqb_devtools").joinpath("base-config.yaml")
    with resources.as_file(base_app_cfg_rsc) as base_app_cfg_path:
        return base_app_cfg_path


def get_base_app_config_data() -> dict:
    """
    Gets the base app config's YAML object
    :return: A safe load of the base app config's YAML object
    """
    with open(get_base_app_config_path(), 'r') as base_app_cfg_file:
        return yaml.safe_load(base_app_cfg_file)

def get_app_config_path() -> Path:
    """
    Gets the Path to the JQB DevTools app config file.
    :return: The Path to the JQB DevTools config file on the current OS
    """
    return get_app_dir() / "config.yaml"


def get_existing_app_config_version() -> str:
    return get_app_config_data()['app-config-version']

def get_current_app_config_version() -> str:
    return get_base_app_config_data()['app-config-version']

def get_app_config_data() -> dict:
    """
    Gets the app config's YAML object
    :return: A safe load of the app config's YAML object
    """
    cfg_path = get_app_config_path()
    with open(cfg_path, 'r') as config_file:
        return yaml.safe_load(config_file)


def get_saved_project_configs_dir() -> Path:
    """
    Gets the saved configs directory
    :return: The Path to the saved configs directory
    """
    return get_app_dir() / "saved-project-configs"

