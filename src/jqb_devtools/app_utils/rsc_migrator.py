from typing import Callable

import yaml

from jqb_devtools.app_utils.rsc_provider import get_app_config_data, get_base_app_config_data, get_app_config_path
from importlib import metadata

def app_rsc_update_required() -> bool:
    """
    Determines whether an update to the app's resources is required based on
    the currently executing JQB DevTools version compared to the config's version
    :return: True if an update is required, else False
    """
    saved_app_config_version = get_app_config_data()['config-version']
    current_app_config_version = get_current_app_version_str()

    return compare_versions(saved_app_config_version, current_app_config_version) < 0


def compare_versions(version1: str, version2: str) -> int:
    """
    Compares version1 to version2, returning an integer representing the comparison's outcome.

    :param version1: the first version to compare
    :param version2: the second version to compare

    :return: -1 if version1 < version2, 0 if version1 == version2, and 1 if version1 > version2
    """
    # Make the versions comparable
    version1 = convert_version_str_to_comparable(version1)
    version2 = convert_version_str_to_comparable(version2)

    # Normalize the versions
    if len(version1) < len(version2):
        for i in range(len(version2) - len(version1)):
            version1.append(0)
    elif len(version2) < len(version1):
        for i in range(len(version1) - len(version2)):
            version2.append(0)

    # Skip the number-by-number conversion if the version strings are identical
    if version1 != version2:
        # Stop as soon as a difference is detected
        for i in range(len(version1)):
            if version1[i] < version2[i]:
                return -1
            elif version1[i] > version2[i]:
                return 1
    else:
        return 0


def convert_version_str_to_comparable(version_str: str) -> list[int]:
    """
    Converts the provided, period-delimited version string into an array, which can be compared
    :param version_str: The period-delimited version string to convert
    :return: An array of length delimiter + 1 containing each number of the version as an int, in the same
    order as the version number string
    """
    comparable_version_arr = []
    for digit in version_str.split('.'):
        comparable_version_arr.append(int(digit))

    return comparable_version_arr


def get_current_app_version_str() -> str:
    """
    Gets the current version string of JQB DevTools
    :return: The current version string of JQB DevTools
    """
    return metadata.version("jqb_devtools")


def update_app_resources():
    """
    Updates the app's resources to the latest version
    """
    print(f"Migrating JQB DevTools app resources from version "
          f"{get_app_config_data()['app-config-version']} to the latest version {get_current_app_version_str()}...")
    migrate_app_config()
    print("JQB DevTools app resources update complete.")


def migrate_app_config():
    """
    Migrates the app's config to the latest config format
    """
    transient_config = get_app_config_data()
    transient_version = transient_config['app-config-version']

    # While there are still migration steps left to perform
    while transient_version in app_cfg_migrators.keys():
        transient_config = app_cfg_migrators[transient_version](transient_config)
        transient_version = transient_config['app-config-version']

    # Fill in any new config properties that didn't exist before
    base_config = get_base_app_config_data()
    migrated_config = add_missing_cfg_properties(transient_config, base_config)

    # Save the new config
    with get_app_config_path().open("w") as config_file:
        config_file.write(yaml.dump(migrated_config))

def add_missing_cfg_properties(incomplete_config: dict, reference_config: dict) -> dict:
    """
    Adds any missing properties of the reference_config to the incomplete_config

    :param incomplete_config: the config dict to add any missing properties from the reference_config to
    :param reference_config: the config to reference as the "complete" version

    :return: the original incomplete_config but with all properties of the reference version guaranteed
    """
    complete_config = incomplete_config.copy()
    for key in reference_config.keys():
        if key not in complete_config.keys():
            complete_config[key] = reference_config[key]

    return complete_config

def migrate0_0_4(old_config: dict) -> dict:
    new_config = old_config.copy()
    new_config['app-config-version'] = "0.0.5"
    return new_config


# Migrates from version <key> to the next version using the <value> migrator function
app_cfg_migrators: dict[str, Callable[[dict], dict]] = {
    "0.0.4": migrate0_0_4
}
