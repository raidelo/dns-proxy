from pathlib import Path
from typing import Any, Mapping, Optional, TypeGuard

from toml import TomlEncoder, dump, load

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


def _expect_dict(value: Any, *, name: str) -> dict[Any, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be of type dict")
    return value


def _validate(value: Mapping[str, Any]) -> TypeGuard[ConfigDict]:
    try:
        settings = value["settings"]
        vars_ = value["vars"]
        map_ = value["map"]
        exceptions = value["exceptions"]
    except KeyError as e:
        raise TypeError(f"Missing key in settings file: {e.args[0]}") from None

    settings = _expect_dict(settings, name="settings")
    vars_ = _expect_dict(vars_, name="vars")
    map_ = _expect_dict(map_, name="map")
    exceptions = _expect_dict(exceptions, name="exceptions")

    for k, v in map_.items():
        if not isinstance(k, str):
            raise TypeError("map keys must be str")
        if not isinstance(v, str):
            raise TypeError("map values must be str")

    for k, v in exceptions.items():
        if not isinstance(k, str):
            raise TypeError("exceptions keys must be str")
        if not isinstance(v, list):
            raise TypeError("exceptions values must be list[str]")
        if not all(isinstance(item, str) for item in v):
            raise TypeError("exceptions values must be list[str]")

    return True


def load_config_file(config_file: Path) -> MainConfig:
    raw_config: dict[str, Any] = load(config_file)

    try:
        if _validate(raw_config):
            return MainConfig.from_dict(raw_config)
        else:
            raise ValueError(
                "unreachable"
            )  # _validate raises TypeError if the provided value doesn't match the ConfigDict definition
    except TypeError as e:
        raise TypeError(f"Invalid format in the config file: {e}") from None


class CustomTomlEncoder(TomlEncoder):
    def dump_list(self, v):
        retval = "["
        for u in v:
            retval += str(self.dump_value(u)) + ", "

        retval = retval.strip(", ") + "]"

        return retval


def save_to_config(config: MainConfig, path: Path) -> None:
    with path.open("w") as f:
        nconfig = parse_to_str(config)
        dump(nconfig, f, encoder=CustomTomlEncoder())


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
    exceptions = {str(k): [str(lv) for lv in v] for k, v in config.exceptions.items()}
    vars = {str(k): str(v) for k, v in config.vars.items()}

    return {
        "settings": settings,
        "map": map,
        "exceptions": exceptions,
        "vars": vars,
    }


def _update(this: dict[Any, Any], with_: dict[Any, Any], overwrite: bool) -> None:
    if overwrite:
        this.update(with_)
    else:
        for k, v in with_.items():
            if k not in this:
                this[k] = v


def update(this: MainConfig, with_: MainConfig, overwrite: bool) -> None:
    _update(this.settings.__dict__, with_.settings.__dict__, overwrite)
    _update(this.map, with_.map, overwrite)
    _update(this.exceptions, with_.exceptions, overwrite)
    _update(this.vars, with_.vars, overwrite)


def print_error(msg: str) -> None:
    RED = "\x1b[31m"
    BOLD = "\x1b[1m"
    RESET = "\x1b[0m"
    print(f"{RED + BOLD}error:{RESET} {msg}{RESET}")


def logf(msg: str, logs_file: Optional[Path]) -> None:
    print(msg)

    if logs_file is not None:
        with logs_file.open("r") as f:
            f.write(f"{msg}\n")
            f.flush()
