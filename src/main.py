from ipaddress import IPv4Address
from typing import Mapping, Optional, Sequence

from dnslib import DNSLabel
from dnslib.server import BaseResolver, DNSHandler, DNSLogger, DNSServer

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
from utils import load_config_file, save_to_config, update

OVERWRITE_CONFIG_FILE = True  # TODO: add argument to handle this value


def main() -> None:
    args = Args.parse_args()

    config = MainConfig(
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

    fconfig: Optional[MainConfig] = None
    try:
        fconfig = load_config_file(CONFIG_FILE)
        update(this=config, with_=fconfig, overwrite=True)
    except FileNotFoundError:
        pass

    if args.force_args:
        update(this=config, with_=args.config, overwrite=True)

    if args.save_config:
        save_to_config(config, CONFIG_FILE)

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
    settings: ServerSettings,
    map: Mapping[DNSLabel, IPv4Address],
    exceptions: Mapping[DNSLabel, Sequence[IPv4Address]],
) -> None:
    resolver = BaseResolver()

    logger: DNSLogger = DNSLogger(
        log=settings.log_format,
        prefix=settings.log_prefix,
        logf=settings.logs_file,
    )
    handler: type[DNSHandler] = DNSHandler

    server = DNSServer(
        resolver=resolver,
        address=str(settings.laddress),
        port=settings.lport,
        tcp=False,
        logger=logger,
        handler=handler,
        server=None,
    )

    # resolver = MainResolver(
    #     address=settings.uaddress,
    #     port=settings.uport,
    #     timeout=settings.timeout,
    #     map=map,
    #     exceptions=exceptions,
    # )
    #
    # logger = MainLogger(settings.log_format, settings.log_prefix)
    #
    # if settings.logs_file:
    #     logger.set_logs_file(settings.logs_file)
    #
    # server = DNSServer(
    #     resolver=resolver,
    #     address=str(settings.laddress),
    #     port=settings.lport,
    #     logger=logger,
    #     handler=DNSHandler,
    # )

    try:
        server.start()

    except KeyboardInterrupt:
        print("Keyboard Interrupt detected. Exitting ...")
    return


if __name__ == "__main__":
    main()
