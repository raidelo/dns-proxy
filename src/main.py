from configparser import ConfigParser

from dnslib.server import DNSHandler, DNSServer
from cli import argument_parser
from constants import (
    DEFAULT_LOGGING_FMT,
    DEFAULT_SETTINGS_FILE,
    DEFAULT_TIMEOUT,
    LOCAL_ADDRESS,
    LOCAL_PORT,
    UPSTREAM_ADDRESS,
    UPSTREAM_PORT,
)
from dns import MainLogger, MainResolver
from utils import get_mapping, get_section_without_defaults, parse_logs_file


def main(
    local_server_address=(LOCAL_ADDRESS, LOCAL_PORT),
    dns_server_address=(UPSTREAM_ADDRESS, UPSTREAM_PORT),
    timeout=DEFAULT_TIMEOUT,
    log_format="",
    log_prefix=False,
    logs_file: str | bool = False,
    map={},
    exceptions={},
):
    resolver = MainResolver(
        *dns_server_address, timeout=timeout, map=map, exceptions=exceptions
    )

    logger = MainLogger(log_format, log_prefix)

    if logs_file:
        logger.set_logs_file(logs_file)

    server_ = DNSServer(
        resolver, *local_server_address, logger=logger, handler=DNSHandler
    )

    try:
        server_.start()

    except KeyboardInterrupt:
        print("Keyboard Interrupt detected. Closing...")
        exit(0)


if __name__ == "__main__":
    args = argument_parser().parse_args()

    defaults = {
        "address": LOCAL_ADDRESS,
        "port": LOCAL_PORT,
        "upstream": f"{UPSTREAM_ADDRESS}:{UPSTREAM_PORT}",
        "timeout": DEFAULT_TIMEOUT,
        "log_format": DEFAULT_LOGGING_FMT,
        "log_prefix": False,
        "logs_file": False,
    }

    map_ = get_mapping(args.map)
    exceptions_ = get_mapping(args.exceptions)

    if args.save_config or not args.use_args:
        c_parser = ConfigParser(defaults=defaults)

        for section in ("SAVED", "MAP", "EXCEPTIONS"):
            c_parser.add_section(section)

        config_file_route = (
            args.save_config if args.save_config else DEFAULT_SETTINGS_FILE
        )

        if args.save_config:
            for arg, xdefect_value in defaults.items():
                dict_args = dict(args._get_kwargs())

                if dict_args[arg] != xdefect_value:
                    c_parser.set("SAVED", arg, str(dict_args[arg]))

            if map_:
                c_parser["MAP"] = map_

            if exceptions_:
                c_parser["EXCEPTIONS"] = exceptions_

            with open(config_file_route, "w") as file:
                c_parser.write(file)

        if not args.use_args:
            found_ = c_parser.read(config_file_route)

            if found_:
                address = c_parser.get("SAVED", "address")
                port = c_parser.getint("SAVED", "port")
                upstream = c_parser.get("SAVED", "upstream")
                timeout = c_parser.getint("SAVED", "timeout")
                log_format = c_parser.get("SAVED", "log_format")
                log_prefix = c_parser.getboolean("SAVED", "log_prefix")
                logs_file = c_parser.get("SAVED", "logs_file")
                map_ = get_section_without_defaults(c_parser, "MAP")
                exceptions_ = get_section_without_defaults(c_parser, "EXCEPTIONS")

            else:
                args.use_args = True

    if args.use_args:
        address = args.address
        port = args.port
        upstream = args.upstream
        timeout = args.timeout
        log_format = args.log_format
        log_prefix = args.log_prefix
        logs_file = args.logs_file

    upstream_address, _, upstream_port = upstream.partition(":")

    upstream_port = int(upstream_port or 53)

    print(
        "Server started at %s:%d || Remote server at %s:%d"
        % (address, port, upstream_address, upstream_port)
    )

    main(
        (address, port),
        (upstream_address, upstream_port),
        timeout,
        log_format,
        log_prefix,
        parse_logs_file(logs_file, default_value=default_logs_file),
        map_,
        exceptions_,
    )
