from ipaddress import IPv4Address
from typing import Mapping, Optional, Sequence

from dnslib import DNSLabel
from dnslib.server import DNSHandler, DNSLogger, DNSServer

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
from dns import CustomDNSLogger, CustomProxyResolver
from utils import (
    load_config_file,
    logf,
    print_error,
    save_to_config,
    update,
)


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
    resolver = CustomProxyResolver(
        address=str(settings.uaddress),
        port=settings.uport,
        timeout=settings.timeout,
        strip_aaaa=False,
        map=map,
        exceptions=exceptions,
    )

    def _logf(msg: str) -> None:
        return logf(msg, LOGS_FILE)

    logger: DNSLogger = CustomDNSLogger(
        log=settings.log_format,
        prefix=settings.log_prefix,
        logf=_logf,
    )

    handler: type[DNSHandler] = DNSHandler

    try:
        server = DNSServer(
            resolver=resolver,
            address=str(settings.laddress),
            port=settings.lport,
            tcp=False,
            logger=logger,
            handler=handler,
            server=None,
        )
    except PermissionError:
        print_error(f"cannot bind to port {settings.lport}")
        return

    server.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupt detected ...")
