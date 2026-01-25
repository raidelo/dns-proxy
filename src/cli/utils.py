from ipaddress import IPv4Address
from typing import Sequence


def parse_map(value: str) -> Mapping[str, IPv4Address]:
    raise NotImplementedError()  # TODO: todo


def parse_exceptions(value: str) -> Mapping[str, Sequence[IPv4Address]]:
    raise NotImplementedError()  # TODO: todo
