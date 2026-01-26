from pathlib import Path
from typing import Any, Mapping, TypeGuard

from toml import load

from config_repr import MainConfig
from models import ConfigDict


def parse_logs_file(logs_file: str, default_value: str):
    if isinstance(logs_file, str):
        if logs_file.strip().lower() in ["true", "1", "activate", "enable", "on"]:
            return default_value

        elif logs_file.strip().lower() in [
            "false",
            "0",
            "deactivate",
            "disable",
            "off",
        ]:
            return False

        else:
            return logs_file

    else:
        return default_value if logs_file else logs_file


def validate(value: Mapping[str, Any]) -> TypeGuard[ConfigDict]:
    v1 = isinstance(value.get("settings"), dict)
    v2 = isinstance(value.get("vars"), dict)
    v3 = isinstance(value.get("map"), dict)
    v4 = isinstance(value.get("exceptions"), dict)

    return v1 and v2 and v3 and v4


def load_config_file(config_file: Path) -> MainConfig:
    raw_config: dict[str, Any] = load(config_file)

    if not validate(raw_config):
        raise ValueError("Invalid format in the config file")

    return MainConfig.from_dict(raw_config)


def _update(this: Mapping[Any, Any], with_: Mapping[Any, Any], overwrite: bool) -> None:
    for k, v in with_.items():
        res = this.get(k)
        if not res or res and overwrite:
            this[k] = v


def update(this: MainConfig, with_: MainConfig, overwrite: bool) -> None:
    _update(this.settings.__dict__, with_.settings.__dict__, overwrite)
    _update(this.map, with_.map, overwrite)
    _update(this.exceptions, with_.exceptions, overwrite)
    _update(this.vars, with_.vars, overwrite)


def save_to_config(config: MainConfig, path: Path) -> None:
    with path.open("r") as f:
        toml.dump(config.__dict__, f)


def update_config_file(config: MainConfig, config_file: Path, overwrite: bool) -> None:
    fconfig = load_config_file(config_file)
    update(fconfig, config, overwrite)
    save_to_config(fconfig, config_file)
