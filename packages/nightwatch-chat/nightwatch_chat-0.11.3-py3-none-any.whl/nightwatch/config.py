# Copyright (c) 2024 iiPython

# Modules
import os
import json
import typing
from pathlib import Path

# Initialization
data_override = os.getenv("DATA_OVERRIDE")
if data_override is None:
    config_path = Path.home() / ".local/share/nightwatch"
    if os.name == "nt":
        appdata = os.getenv("APPDATA")
        if appdata is None:
            exit(r"Nightwatch: %APPDATA% is None, no place available to store data at.")

        config_path = Path(appdata) / "Nightwatch"

else:
    config_path = Path(data_override)

config_path.mkdir(exist_ok = True, parents = True)

# Configuration class
class Configuration():
    def __init__(self, config_path: Path) -> None:
        self.config, self.config_path = {}, config_path
        if config_path.is_file():
            self.config = json.loads(self.config_path.read_text())

    def __getitem__(self, item: str) -> typing.Any:
        v = self.config
        for k in item.split("."):
            if k not in v:
                return None

            v = v[k]

        return v

    def set(self, key: str, value: typing.Any) -> None:
        v = self.config
        for k in key.split(".")[:-1]:
            if k not in v:
                v[k] = {}

            v = v[k]

        v[key.split(".")[-1]] = value
        self.config_path.write_text(json.dumps(self.config, indent = 4))

    def reset(self) -> None:
        self.config = {}
        self.config_path.write_text(json.dumps({}))

# Modern configuration system
def fetch_config(config_module: str) -> Configuration:
    return Configuration(config_path / f"{config_module}.json")
