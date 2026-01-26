from pathlib import Path
from time import strftime

from dnslib import QTYPE, RCODE, RR
from dnslib.proxy import ProxyResolver
from dnslib.server import DNSLogger


class MainResolver(ProxyResolver):
    def __init__(
        self,
        address,
        port,
        timeout=0,
        strip_aaaa=False,
        map={},
        exceptions={},
    ):
        self.map = map
        self.exceptions = exceptions
        super().__init__(address, port, timeout, strip_aaaa)

    def resolve(self, request, handler):
        domain = domain = self.get_domain(request.q.qname)

        if domain in self.map.keys() and not (
            domain in self.exceptions.keys()
            and self.exceptions[domain] == handler.client_address[0]
        ):
            reply = request.reply()

            ip = self.map[domain]

            reply.add_answer(
                *RR.fromZone("{domain} A {ip}".format(domain=domain, ip=ip))
            )

            return reply

        return super().resolve(request, handler)

    def get_domain(self, qname):
        return b".".join(qname.label).decode("utf-8")


class MainLogger(DNSLogger):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.logs_file = None

    def log_prefix(self, handler):
        if self.prefix:
            return "%s " % (strftime("%Y-%m-%d %X"))
        else:
            return ""

    def log_request(self, handler, request):
        self.logf(
            '%sRequest: [%s:%d] (%s) / "%s" (%s)'
            % (
                self.log_prefix(handler),
                handler.client_address[0],
                handler.client_address[1],
                handler.protocol,
                request.q.qname,
                QTYPE[request.q.qtype],
            )
        )

        self.log_data(request)

    def log_reply(self, handler, reply):
        if reply.header.rcode == RCODE.NOERROR:
            self.logf(
                '%sReply:   [%s:%d] (%s) / "%s" (%s) / RRs: %s'
                % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    handler.protocol,
                    reply.q.qname,
                    QTYPE[reply.q.qtype],
                    ",".join([QTYPE[a.rtype] for a in reply.rr]),
                )
            )

        else:
            self.logf(
                '%sReply:   [%s:%d] (%s) / "%s" (%s) / %s'
                % (
                    self.log_prefix(handler),
                    handler.client_address[0],
                    handler.client_address[1],
                    handler.protocol,
                    reply.q.qname,
                    QTYPE[reply.q.qtype],
                    RCODE[reply.header.rcode],
                )
            )

        self.log_data(reply)

    def log_dumper(self, data):
        print(data)

        if self.logs_file:
            self.logs_file.write(data.encode() + b"\n")
            self.logs_file.flush()

    def set_logs_file(self, logs_file: Path):
        try:
            self.logs_file = open(logs_file, "wb")
            self.logf = self.log_dumper

        except Exception:
            print("error: failed to open the log file")

    def __del__(self):
        if self.logs_file:
            self.logs_file.close()
