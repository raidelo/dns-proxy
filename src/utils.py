from pathlib import Path
from typing import Any, Mapping, TypeGuard

from toml import load
from cli.types_ import Args
from config_repr import MainConfig
from constants import DEFAULT_CONFIG_FILE
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


def get_config() -> MainConfig:
    raw_config: dict[str, Any] = load(DEFAULT_CONFIG_FILE)

    if not validate(raw_config):
        raise ValueError()

    data: ConfigDict = raw_config

    return MainConfig.from_dict(data)


def update(this: MainConfig, with_: MainConfig) -> None:
    for k, v in with_.settings.__dict__.items():
        this.settings.__dict__[k] = v

    for k, v in with_.map.__dict__.items():
        this.map.__dict__[k] = v

    for k, v in with_.exceptions.__dict__.items():
        this.exceptions.__dict__[k] = v

    for k, v in with_.vars.__dict__.items():
        this.vars.__dict__[k] = v


def save_to_config(config: MainConfig, path: Path) -> None:
    raise NotImplementedError()  # TODO: implement


def update_config_file(
    config: MainConfig,
    config_file: Path,
    overwrite: bool = False,  # TODO: implement
) -> None:
    fconfig = get_config()
    update(fconfig, config)
    save_to_config(fconfig, config_file)
