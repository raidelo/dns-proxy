from pathlib import Path
from typing import Any, Mapping, TypeGuard

from toml import dump, load

from config_repr import MainConfig
from models import ConfigDict, SettingsDict


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
    settings = value.get("settings")
    vars = value.get("vars")
    map = value.get("map")
    exceptions = value.get("exceptions")

    assert isinstance(settings, dict)
    assert isinstance(vars, dict)
    assert isinstance(map, dict)
    assert isinstance(exceptions, dict)

    for k, v in map.items():
        assert isinstance(k, str), f"{k} must be of type {str}"
        assert isinstance(v, str), f"{v} must be of type {str}"
    for k, v in exceptions.items():
        assert isinstance(k, str), f"{k} must be of type {str}"
        assert isinstance(v, list), f"{v} must be of type {list}"
        for list_val in v:
            assert isinstance(list_val, str), f"{list_val} must be of type {str}"

    return True


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
    with path.open("w") as f:
        dump(parse_to_str(config), f)


def parse_to_str(config: MainConfig) -> ConfigDict:
    settings: SettingsDict = {
        "laddress": str(config.settings.laddress),
        "lport": config.settings.lport,
        "uaddress": str(config.settings.uaddress),
        "uport": config.settings.uport,
        "timeout": config.settings.timeout,
        "log_format": config.settings.log_format,
        "log_prefix": config.settings.log_prefix,
        # "logs_file": None,
    }
    map = {str(k): str(v) for k, v in config.map.items()}
    exceptions = {
        str(k): [str(list_val) for list_val in v] for k, v in config.exceptions.items()
    }
    vars = {str(k): str(v) for k, v in config.vars.items()}

    return {
        "settings": settings,
        "map": map,
        "exceptions": exceptions,
        "vars": vars,
    }
