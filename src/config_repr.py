from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import Any, Mapping, Optional, Sequence

from dnslib import DNSLabel


@dataclass
class Settings:
    laddress: Optional[IPv4Address]
    lport: Optional[int]
    uaddress: Optional[IPv4Address]
    uport: Optional[int]
    timeout: Optional[int]
    map: Mapping[DNSLabel, IPv4Address]
    exceptions: Mapping[DNSLabel, Sequence[IPv4Address]]
    vars: Mapping[str, Any]
    log_format: Optional[str]
    log_prefix: Optional[str]
    logs_file: Optional[str]
