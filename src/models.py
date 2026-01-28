from typing import Any, Mapping, NotRequired, Optional, Sequence, TypedDict


class SettingsDict(TypedDict):
    laddress: NotRequired[str]
    lport: NotRequired[int]
    uaddress: NotRequired[str]
    uport: NotRequired[int]
    timeout: NotRequired[int]
    log_format: NotRequired[str]
    log_prefix: NotRequired[bool]
    logs_file: NotRequired[Optional[str]]


type MapDict = Mapping[str, str]


type ExceptionsDict = Mapping[str, Sequence[str]]


type VarsDict = Mapping[str, Any]


class ConfigDict(TypedDict):
    settings: NotRequired[SettingsDict]
    map: NotRequired[MapDict]
    exceptions: NotRequired[ExceptionsDict]
    vars: NotRequired[VarsDict]
