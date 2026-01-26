from argparse import ArgumentParser
from ipaddress import IPv4Address

from cli.types_ import UpstreamServer
from cli.utils import parse_exceptions_arg, parse_map_arg
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


def argument_parser() -> ArgumentParser:
    parser = ArgumentParser()

    parser.add_argument(
        "-b",
        "--bind",
        default=LOCAL_ADDRESS,
        type=IPv4Address,
        metavar="<laddress>",
        dest="laddress",
        help="bind to this address (default: all interfaces)",
    )

    parser.add_argument(
        "lport",
        default=LOCAL_PORT,
        type=int,
        nargs="?",
        metavar="<lport>",
        dest="port",
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
        default=None,
        const=DEFAULT_SETTINGS_FILE,
        type=str,
        nargs="?",
        metavar="<config_file>",
        dest="save_config",
        help="whether to save specified arguments to a config file to load on next start (default: %(default)s)",
    )

    parser.add_argument(
        "-A",
        "--force-args",
        action="store_true",
        default=False,
        dest="force_args",
        help="to use the arguments instead of the config file (default: %(default)s)",
    )

    parser.add_argument(
        "-m",
        "--map",
        default={},
        type=parse_map_arg,
        metavar="<domain:ip,domain:ip,...>",
        dest="map",
        help="a map like: domain:ip,domain:ip. It will answer the query for the domain with the given IP address (default: %(default)s)",
    )

    parser.add_argument(
        "-x",
        "--exceptions",
        default={},
        type=parse_exceptions_arg,
        metavar="<domain:ip,domain:ip,...>",
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
        help="enable log prefix (timestamp/handler/resolver) (default: %(default)s)",
    )

    return parser
