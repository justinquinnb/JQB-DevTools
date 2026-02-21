from pathlib import Path
from platformdirs import PlatformDirs
from importlib import resources

def get_config_path() -> Path:
    dirs = PlatformDirs("JQB DevTools", ensure_exists=True)
    config_file = dirs.user_data_path / "config.yaml"
    if not config_file.exists():
        initialize_config(config_file)

    return config_file


def initialize_config(config_file: Path):
    try:
        source_path = resources.files("jqb_devtools").joinpath("base-config.yaml")

        with source_path.open("r") as base_config:
            config_file.write_text(base_config.read())
    except Exception as e:
        print(f"Failed to initialize config: {e}")