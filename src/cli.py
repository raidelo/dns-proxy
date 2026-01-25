from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Optional

from config_repr import Settings
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


class UpstreamServer:
    def __init__(self, value: str) -> None:
        raise NotImplementedError()  # TODO: todo


@dataclass
class Args(Settings):
    config_file: Optional[str]
    use_args: bool

    @classmethod
    def from_args(cls, args: Namespace) -> "Args":
        return Args(
            laddress=args.address,
            lport=args.port,
            uaddress=args.upstream.address,
            uport=args.upstream.port,
            timeout=args.timeout,
            map=args.exceptions,
            exceptions=args.exceptions,
            vars={},
            log_format=args.log_format,
            log_prefix=args.log_prefix,
            logs_file=args.logs_file,
            config_file=args.save_config,
            use_args=args.use_args,
        )


def argument_parser() -> ArgumentParser:
    parser = ArgumentParser()

    parser.add_argument(
        "-b",
        "-a",
        "--bind",
        "--address",
        default=LOCAL_ADDRESS,
        metavar="<laddress>",
        dest="address",
        help="bind to this address (default: all interfaces)",
    )
    parser.add_argument(
        "lport",
        default=LOCAL_PORT,
        type=int,
        nargs="?",
        help="bind to this port (default: %(default)s)",
    )
    parser.add_argument(
        "-u",
        "--upstream",
        default=f"{UPSTREAM_ADDRESS}:{UPSTREAM_PORT}",
        type=UpstreamServer,
        metavar="<upstream server:port>",
        dest="upstream",
        help="upstream DNS server:port (default: %(default)s)",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        default=DEFAULT_TIMEOUT,
        type=int,
        metavar="<timeout>",
        dest="timeout",
        help="timeout for the server to resolve queries (default: %(default)s)",
    )
    parser.add_argument(
        "--save-config",
        nargs="?",
        default=False,
        const=DEFAULT_SETTINGS_FILE,
        type=str,
        metavar="config_file",
        dest="save_config",
        help="whether to save specified arguments to a config file to load on next start (default: %(default)s)",
    )
    parser.add_argument(
        "--use-args",
        action="store_true",
        default=False,
        dest="use_args",
        help="to use the arguments instead of the config file (default: %(default)s)",
    )
    parser.add_argument(
        "-m",
        "--map",
        nargs="+",
        default={},
        metavar="<domain:ip domain:ip ...>",
        dest="map",
        help="a map like: domain:ip,domain:ip or separated by spaces like: domain:ip domain:ip. It will answer the query for the domain with the given IP address (default: %(default)s)",
    )
    parser.add_argument(
        "-x",
        "--exceptions",
        nargs="+",
        default={},
        metavar="<domain:ip domain:ip ...>",
        dest="exceptions",
        help="similar to parameter --map. If the client's IP address matches the given IP and the client is asking for the given domain, the local server will be forced to ask the upstream DNS server for that domain, even if that domain is manually mapped to the specified IP in the MAP section (default: %(default)s)",
    )
    parser.add_argument(
        "--logs-file",
        default=DEFAULT_LOGS_FILE,
        metavar="<logs_file>",
        dest="logs_file",
        help="file to dump the logs to (default: %(default)s)",
    )
    parser.add_argument(
        "--log-format",
        default=DEFAULT_LOGGING_FMT,
        metavar="<log_format>",
        dest="log_format",
        help="log hooks to enable (default: +request,+reply,+truncated,+error,-recv,-send,-data)",
    )
    parser.add_argument(
        "--log-prefix",
        action="store_true",
        default=DEFAULT_LOGGING_PREFIX,
        dest="log_prefix",
        help="log prefix (timestamp/handler/resolver) (default: %(default)s)",
    )

    return parser
