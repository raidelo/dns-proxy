from argparse import ArgumentError, Namespace
from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import Optional

from dnslib import DNSLabel

from config_repr import MainConfig, ServerSettings


class UpstreamServer:
    def __init__(self, value: str) -> None:
        ip, port = value.split(":", 1)

        self.address = IPv4Address(ip)
        self.port = int(port)


@dataclass
class Args:
    config: MainConfig
    save_config: Optional[str]
    force_args: bool

    @classmethod
    def _map_to_dict(
        cls,
        list_: list[dict[DNSLabel, IPv4Address]],
    ) -> dict[DNSLabel, IPv4Address]:
        m: dict[DNSLabel, IPv4Address] = {}
        for dict_ in list_:
            for k, v in dict_.items():
                if k in m:
                    raise ArgumentError(
                        None,
                        f"Repeated values for argument -x, --exceptions: {k}:{m[k]} and {k}:{v}",
                    )
                m[k] = v
        return m

    @classmethod
    def _exceptions_to_dict(
        cls,
        list_: list[dict[DNSLabel, list[IPv4Address]]],
    ) -> dict[DNSLabel, list[IPv4Address]]:
        m: dict[DNSLabel, list[IPv4Address]] = {}
        for dict_ in list_:
            for k, v in dict_.items():
                if k in m:
                    m[k].extend(v)
                else:
                    m[k] = list(v)
        return m

    @classmethod
    def from_args(cls, args: Namespace) -> "Args":
        settings = ServerSettings(
            laddress=args.laddress,
            lport=args.lport,
            uaddress=args.upstream.address,
            uport=args.upstream.port,
            timeout=args.timeout,
            log_format=args.log_format,
            log_prefix=args.log_prefix,
            logs_file=args.logs_file,
        )
        config = MainConfig(
            settings=settings,
            map=cls._map_to_dict(args.map),
            exceptions=cls._exceptions_to_dict(args.exceptions),
            vars={},
        )
        return Args(
            config=config,
            save_config=args.save_config,
            force_args=args.force_args,
        )

    @classmethod
    def parse_args(cls) -> "Args":
        from cli import argument_parser

        args = argument_parser().parse_args()
        return cls.from_args(args)
