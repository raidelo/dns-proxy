from dataclasses import dataclass
from ipaddress import AddressValueError, IPv4Address
from pathlib import Path
from typing import Any, Mapping, Optional, Sequence

from dnslib import DNSLabel

from constants import (
    LOG_FORMAT,
    LOG_PREFIX,
    LOGS_FILE,
    TIMEOUT,
    LADDRESS,
    LPORT,
    UADDRESS,
    UPORT,
)
from models import ConfigDict, ExceptionsDict, MapDict, SettingsDict, VarsDict


@dataclass
class ServerSettings:
    laddress: IPv4Address
    lport: int
    uaddress: IPv4Address
    uport: int
    timeout: int
    log_format: str
    log_prefix: Optional[str]
    logs_file: Path

    @classmethod
    def from_dict(cls, val: SettingsDict) -> "ServerSettings":
        logs_file = val.get("logs_file")
        return ServerSettings(
            laddress=IPv4Address(val.get("laddress", LADDRESS)),
            lport=val.get("lport", LPORT),
            uaddress=IPv4Address(val.get("uaddress", UADDRESS)),
            uport=val.get("uport", UPORT),
            timeout=val.get("timeout", TIMEOUT),
            log_format=val.get("log_format", LOG_FORMAT),
            log_prefix=val.get("log_prefix", LOG_PREFIX),
            logs_file=Path(logs_file) if logs_file else LOGS_FILE,
        )


@dataclass
class MainConfig:
    settings: ServerSettings
    map: Mapping[DNSLabel, IPv4Address]
    exceptions: Mapping[DNSLabel, Sequence[IPv4Address]]
    vars: Mapping[str, Any]

    @classmethod
    def from_dict(cls, val: ConfigDict) -> "MainConfig":
        settings = val.get("settings", {})
        map = val.get("map", {})
        exceptions = val.get("exceptions", {})
        vars = val.get("vars", {})
        return MainConfig(
            settings=ServerSettings.from_dict(settings),
            map=parse_map_sect(map, vars=vars),
            exceptions=parse_exceptions_sect(exceptions, vars=vars),
            vars=val.get("vars", {}),
        )


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
                ip_str = ip_str.replace(f"${{{key}}}", value)
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
                    ip_str = ip_str.replace(f"${{{key}}}", value)
                new_ip = IPv4Address(ip_str)
            new_ip_seq.append(new_ip)
        new_exc[new_key] = new_ip_seq
    return new_exc
