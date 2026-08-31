FROM debian:trixie-slim

RUN apt update && apt install -y \
    bind9 \
    bind9utils \
    dnsutils \
    tcpdump 

EXPOSE 53/tcp
EXPOSE 53/udp

CMD ["/usr/sbin/named", "-f", "-g", "-c", "/etc/bind/named.conf"]
