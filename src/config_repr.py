from dataclasses import dataclass
from typing import Any, Mapping, Optional


@dataclass
class Settings:
    laddress: Optional[str]
    lport: Optional[int]
    uaddress: Optional[str]
    uport: Optional[int]
    timeout: Optional[int]
    map: Mapping[str, str]
    exceptions: Mapping[str, str]
    vars: Mapping[str, Any]
    log_format: Optional[str]
    log_prefix: Optional[str]
    logs_file: Optional[str]
