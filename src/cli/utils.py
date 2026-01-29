from ipaddress import IPv4Address

from dnslib import DNSLabel


def parse_map_arg(value: str) -> dict[DNSLabel, IPv4Address]:
    map: dict[DNSLabel, IPv4Address] = {}

    for pair in value.split(","):
        domain, ip = pair.split(":", 1)
        domain = DNSLabel(domain)
        ip = IPv4Address(ip)

        map[domain] = ip

    return map


def parse_exceptions_arg(value: str) -> dict[DNSLabel, list[IPv4Address]]:
    mapping: dict[DNSLabel, list[IPv4Address]] = {}

    domain, ip = value.split(":", 1)
    ips = ip.split(",")
    domain = DNSLabel(domain)
    ips = [IPv4Address(ip) for ip in ips]

    mapping[domain] = ips

    return mapping
