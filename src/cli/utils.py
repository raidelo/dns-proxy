from ipaddress import IPv4Address
from typing import Mapping, Sequence

from dnslib import DNSLabel


def parse_map_arg(value: str) -> Mapping[DNSLabel, IPv4Address]:
    map: Mapping[DNSLabel, IPv4Address] = {}

    for pair in value.split(","):
        domain, ip = pair.split(":", 1)
        domain = DNSLabel(domain)
        ip = IPv4Address(ip)

        map[domain] = ip

    return map


def parse_exceptions_arg(value: str) -> Mapping[str, Sequence[IPv4Address]]:
    raise NotImplementedError()  # TODO: todo
