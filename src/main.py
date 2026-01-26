from ipaddress import IPv4Address
from typing import Mapping, Sequence

from dnslib import DNSLabel
from dnslib.server import DNSHandler, DNSServer

from cli.types_ import Args
from config_repr import ConfigData, Settings
from constants import (
    DEFAULT_LOGGING_FMT,
    DEFAULT_LOGGING_PREFIX,
    DEFAULT_LOGS_FILE,
    DEFAULT_SETTINGS_FILE,
    DEFAULT_TIMEOUT,
    LOCAL_ADDRESS,
    LOCAL_PORT,
    UPSTREAM_ADDRESS,
    UPSTREAM_PORT,
)
from dns import MainLogger, MainResolver
from utils import get_config, update


def main() -> None:
    args = Args.parse_args()

    config = ConfigData(
        settings=Settings(
            laddress=IPv4Address(LOCAL_ADDRESS),
            lport=LOCAL_PORT,
            uaddress=IPv4Address(UPSTREAM_ADDRESS),
            uport=UPSTREAM_PORT,
            timeout=DEFAULT_TIMEOUT,
            log_format=DEFAULT_LOGGING_FMT,
            log_prefix=DEFAULT_LOGGING_PREFIX,
            logs_file=DEFAULT_LOGS_FILE,
        ),
        map={},
        exceptions={},
        vars={},
    )

    if args.force_args:
        update(config, args.config)
    else:
        try:
            update(config, get_config())
        except FileNotFoundError:
            pass

    if args.save_config:
        args.config.save_to_file(DEFAULT_SETTINGS_FILE)

    settings = config.settings

    lpart = f"Server started at {settings.laddress}:{settings.lport}"
    rpart = f"Upstream server at {settings.uaddress}:{settings.uport}"
    print(f"{lpart} || {rpart}")

    start_server(
        settings=settings,
        map=config.map,
        exceptions=config.exceptions,
    )


def start_server(
    settings: Settings,
    map: Mapping[DNSLabel, IPv4Address],
    exceptions: Mapping[DNSLabel, Sequence[IPv4Address]],
) -> None:
    resolver = MainResolver(
        address=settings.uaddress,
        port=settings.uport,
        timeout=settings.timeout,
        map=map,
        exceptions=exceptions,
    )

    logger = MainLogger(settings.log_format, settings.log_prefix)

    if settings.logs_file:
        logger.set_logs_file(settings.logs_file)

    server = DNSServer(
        resolver=resolver,
        address=str(settings.laddress),
        port=settings.lport,
        logger=logger,
        handler=DNSHandler,
    )

    try:
        server.start()

    except KeyboardInterrupt:
        print("Keyboard Interrupt detected. Exitting ...")
        return


if __name__ == "__main__":
    main()
