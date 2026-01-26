from dataclasses import dataclass
from ipaddress import AddressValueError, IPv4Address
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

from dnslib import DNSLabel

from constants import (
    DEFAULT_LOGGING_FMT,
    DEFAULT_LOGGING_PREFIX,
    DEFAULT_LOGS_FILE,
    DEFAULT_TIMEOUT,
    LOCAL_ADDRESS,
    LOCAL_PORT,
    UPSTREAM_ADDRESS,
    UPSTREAM_PORT,
)
from models import ConfigDict, ExceptionsDict, MapDict, SettingsDict, VarsDict

DEFAULT_SETTINGS: SettingsDict = {
    "laddress": LOCAL_ADDRESS,
    "lport": LOCAL_PORT,
    "uaddress": UPSTREAM_ADDRESS,
    "uport": UPSTREAM_PORT,
    "timeout": DEFAULT_TIMEOUT,
    "log_format": DEFAULT_LOGGING_FMT,
    "log_prefix": DEFAULT_LOGGING_PREFIX,
    "logs_file": DEFAULT_LOGS_FILE.as_posix(),
}


@dataclass
class Settings:
    laddress: IPv4Address
    lport: int
    uaddress: IPv4Address
    uport: int
    timeout: int
    log_format: str
    log_prefix: Optional[str]
    logs_file: Path

    @classmethod
    def from_dict(cls, val: SettingsDict) -> "Settings":
        logs_file = val.get("logs_file")
        return Settings(
            laddress=IPv4Address(val.get("laddress", default=LOCAL_ADDRESS)),
            lport=val.get("lport", default=LOCAL_PORT),
            uaddress=IPv4Address(val.get("uaddress", default=UPSTREAM_ADDRESS)),
            uport=val.get("uport", default=UPSTREAM_PORT),
            timeout=val.get("timeout", default=DEFAULT_TIMEOUT),
            log_format=val.get("log_format", default=DEFAULT_LOGGING_FMT),
            log_prefix=val.get("log_prefix", default=DEFAULT_LOGGING_PREFIX),
            logs_file=Path(logs_file) if logs_file else DEFAULT_LOGS_FILE,
        )


@dataclass
class ConfigData:
    settings: Settings
    map: Mapping[DNSLabel, IPv4Address]
    exceptions: Mapping[DNSLabel, Sequence[IPv4Address]]
    vars: Mapping[str, Any]

    @classmethod
    def from_dict(cls, val: ConfigDict) -> "ConfigData":
        settings = val.get("settings", default=DEFAULT_SETTINGS)
        map = val.get("map", default={})
        exceptions = val.get("exceptions", default={})
        vars = val.get("vars", default={})
        return ConfigData(
            settings=Settings.from_dict(settings),
            map=parse_map_sect(map, vars=vars),
            exceptions=parse_exceptions_sect(exceptions, vars=vars),
            vars=val.get("vars", default={}),
        )

    def save_to_file(self, path: Path) -> None:
        raise NotImplementedError()  # TODO: todo


def parse_map_sect(
    map: MapDict,
    vars: Optional[VarsDict],
) -> Mapping[DNSLabel, IPv4Address]:
    new_map: Mapping[DNSLabel, IPv4Address] = {}
    for domain, ip_str in map.items():
        new_key = DNSLabel(domain)
        try:
            new_ip = IPv4Address(ip_str)
        except AddressValueError:
            if vars is None:
                raise

            for key, value in vars.items():
                ip_str.replace(f"${{{key}}}", value)
            new_ip = IPv4Address(ip_str)
        new_map[new_key] = new_ip
    return new_map


def parse_exceptions_sect(
    exceptions: ExceptionsDict,
    vars: Optional[VarsDict],
) -> Mapping[DNSLabel, Sequence[IPv4Address]]:
    new_exc: Mapping[DNSLabel, Sequence[IPv4Address]] = {}
    for domain, ip_seq in exceptions.items():
        new_key = DNSLabel(domain)
        new_ip_seq: list[IPv4Address] = []
        for ip_str in ip_seq:
            try:
                new_ip = IPv4Address(ip_str)
            except AddressValueError:
                if vars is None:
                    raise

                for key, value in vars.items():
                    ip_str.replace(f"${{{key}}}", value)
                new_ip = IPv4Address(ip_str)
            new_ip_seq.append(new_ip)
        new_exc[new_key] = new_ip_seq
    return new_exc
