FROM debian:trixie-slim

RUN apt update && apt install -y \
    unbound \
    dnsutils \
    tcpdump

EXPOSE 53/tcp
EXPOSE 53/udp 

CMD ["/usr/sbin/unbound", "-d", "-c", "/etc/unbound/unbound.conf"]
