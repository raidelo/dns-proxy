from typing import Any, NotRequired, Optional, TypedDict


class SettingsDict(TypedDict):
    laddress: NotRequired[str]
    lport: NotRequired[int]
    uaddress: NotRequired[str]
    uport: NotRequired[int]
    timeout: NotRequired[int]
    log_format: NotRequired[str]
    log_prefix: NotRequired[bool]
    logs_file: NotRequired[Optional[str]]


type MapDict = dict[str, str]


type ExceptionsDict = dict[str, list[str]]


type VarsDict = dict[str, Any]


class ConfigDict(TypedDict):
    settings: NotRequired[SettingsDict]
    map: NotRequired[MapDict]
    exceptions: NotRequired[ExceptionsDict]
    vars: NotRequired[VarsDict]
