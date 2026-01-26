from ipaddress import IPv4Address
from typing import Mapping, Sequence

from dnslib import DNSLabel
from dnslib.server import DNSHandler, DNSServer

from cli.types_ import Args
from config_repr import MainConfig, ServerSettings
from constants import (
    CONFIG_FILE,
    LADDRESS,
    LOG_FORMAT,
    LOG_PREFIX,
    LOGS_FILE,
    LPORT,
    TIMEOUT,
    UADDRESS,
    UPORT,
)
from dns import MainLogger, MainResolver
from utils import load_config_file, update, update_config_file

OVERWRITE_CONFIG_FILE = False  # TODO: add argument to handle this value


def main() -> None:
    args = Args.parse_args()

    mconfig = MainConfig(
        settings=ServerSettings(
            laddress=IPv4Address(LADDRESS),
            lport=LPORT,
            uaddress=IPv4Address(UADDRESS),
            uport=UPORT,
            timeout=TIMEOUT,
            log_format=LOG_FORMAT,
            log_prefix=LOG_PREFIX,
            logs_file=LOGS_FILE,
        ),
        map={},
        exceptions={},
        vars={},
    )

    if args.force_args:
        update(mconfig, args.config, True)
    else:
        try:
            update(mconfig, load_config_file(CONFIG_FILE), True)
        except FileNotFoundError:
            pass

    if args.save_config:
        update_config_file(
            config=args.config,
            config_file=CONFIG_FILE,
            overwrite=OVERWRITE_CONFIG_FILE,
        )

    settings = mconfig.settings

    lpart = f"Server started at {settings.laddress}:{settings.lport}"
    rpart = f"Upstream server at {settings.uaddress}:{settings.uport}"
    print(f"{lpart} || {rpart}")

    __import__("pprint").pprint(mconfig.__dict__)
    try:
        lconfig = load_config_file(CONFIG_FILE)
        __import__("pprint").pprint(lconfig.__dict__)
    except Exception:
        print("Inexistent config file")

    return

    start_server(
        settings=settings,
        map=mconfig.map,
        exceptions=mconfig.exceptions,
    )


def start_server(
    settings: ServerSettings,
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
