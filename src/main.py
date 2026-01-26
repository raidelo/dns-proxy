from ipaddress import IPv4Address
from typing import Mapping, Sequence, cast

from dnslib import DNSLabel
from dnslib.server import DNSHandler, DNSServer
from toml import load

from cli.types_ import Args
from config_repr import ConfigData
from constants import (
    DEFAULT_SETTINGS_FILE,
    DEFAULT_TIMEOUT,
    LOCAL_ADDRESS,
    LOCAL_PORT,
    UPSTREAM_ADDRESS,
    UPSTREAM_PORT,
)
from dns import MainLogger, MainResolver
from models import ConfigDict

defaults = """
[defaults]
laddress = "0.0.0.0"
lport = 53
uaddress = "1.1.1.1"
uport = 53
timeout = 5
log_format = "request,reply,truncated,error"
log_prefix = "undefined"
logs_file = "dns_logs.log"
"""


def get_config() -> ConfigData:
    data: ConfigDict = cast(
        ConfigDict, load(DEFAULT_SETTINGS_FILE)
    )  # TODO: replace casting
    return ConfigData.from_dict(data)


def main() -> None:
    args = Args.parse_args()

    if args.force_args:
        config = args.configuration
    else:
        config = get_config()

    if args.save_config:
        args.configuration.save_to_file(DEFAULT_SETTINGS_FILE)

    print(
        f"Server started at {config.settings.laddress}:{config.settings.lport} || Upstream server at {config.settings.uaddress}:{config.settings.uport}"
    )

    setup_server(
        settings=config.settings,
        map=config.map,
        exceptions=exceptions,
    )


def setup_server(
    settings: Settings,
    map: Mapping[DNSLabel, IPv4Address],
    exceptions: Mapping[DNSLabel, Sequence[IPv4Address]],
):
    resolver = MainResolver(*uaddress, timeout=timeout, map=map, exceptions=exceptions)

    logger = MainLogger(log_format, log_prefix)

    if logs_file:
        logger.set_logs_file(logs_file)

    server_ = DNSServer(resolver, *laddress, logger=logger, handler=DNSHandler)

    try:
        server_.start()

    except KeyboardInterrupt:
        print("Keyboard Interrupt detected. Closing...")
        exit(0)


if __name__ == "__main__":
    main()
