from ipaddress import IPv4Address
from time import strftime
from typing import Callable, Mapping, Optional, Sequence

from dnslib import RR, DNSLabel, DNSRecord
from dnslib.proxy import ProxyResolver
from dnslib.server import DNSHandler, DNSLogger


class CustomProxyResolver(ProxyResolver):
    def __init__(
        self,
        address: str,
        port: int,
        timeout: int = 0,
        strip_aaaa: bool = False,
        map: Mapping[DNSLabel, IPv4Address] = {},
        exceptions: Mapping[DNSLabel, Sequence[IPv4Address]] = {},
    ):
        self.map = map
        self.exceptions = exceptions
        super().__init__(address, port, timeout, strip_aaaa)

    def resolve(self, request: DNSRecord, handler: DNSHandler):
        qname: DNSLabel = request.q.qname
        client_address: str = handler.client_address[0]

        if (
            qname in self.exceptions
            and client_address in self.exceptions[qname]
            or qname not in self.map
        ):
            return super().resolve(request, handler)

        else:
            reply = request.reply()

            ip = self.map[qname]

            reply.add_answer(*RR.fromZone(f"{qname} A {ip}"))

            return reply


class CustomDNSLogger(DNSLogger):
    def __init__(
        self,
        log: str = "",
        prefix: bool = True,
        logf: Optional[Callable[[str], None]] = None,
    ):
        super().__init__(log, prefix, logf)

    def log_prefix(self, handler):
        _ = handler
        if self.prefix:
            return f"{strftime('%F %T')} "
        else:
            return ""
