from typing import Any, Mapping, NotRequired, Optional, Sequence, TypedDict


class SettingsDict(TypedDict):
    laddress: NotRequired[str]
    lport: NotRequired[int]
    uaddress: NotRequired[str]
    uport: NotRequired[int]
    timeout: NotRequired[int]
    log_format: NotRequired[str]
    log_prefix: NotRequired[Optional[str]]
    logs_file: NotRequired[str]


type VarsDict = Mapping[str, Any]


type MapDict = Mapping[str, str]


type ExceptionsDict = Mapping[str, Sequence[str]]


class ConfigDict(TypedDict):
    settings: NotRequired[SettingsDict]
    vars: NotRequired[VarsDict]
    map: NotRequired[MapDict]
    exceptions: NotRequired[ExceptionsDict]
