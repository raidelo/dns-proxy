from argparse import Namespace
from dataclasses import dataclass
from ipaddress import IPv4Address
from typing import Optional

from cli import argument_parser
from config_repr import ConfigData, Settings


class UpstreamServer:
    def __init__(self, value: str) -> None:
        ip, port = value.split(":", 1)

        self.address = IPv4Address(ip)
        self.port = int(port)


@dataclass()
class Args:
    configuration: ConfigData
    save_config: Optional[str]
    force_args: bool

    @classmethod
    def from_args(cls, args: Namespace) -> "Args":
        settings = Settings(
            laddress=args.laddress,
            lport=args.lport,
            uaddress=args.upstream.address,
            uport=args.upstream.port,
            timeout=args.timeout,
            log_format=args.log_format,
            log_prefix=args.log_prefix,
            logs_file=args.logs_file,
        )
        configuration = ConfigData(
            settings=settings,
            map=args.map,
            exceptions=args.exceptions,
            vars={},
        )
        return Args(
            configuration=configuration,
            save_config=args.save_config,
            force_args=args.force_args,
        )

    @classmethod
    def parse_args(cls) -> "Args":
        args = argument_parser().parse_args()
        return cls.from_args(args)
