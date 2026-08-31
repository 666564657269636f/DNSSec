from dataclasses import dataclass

@dataclass
class Server:
    name: str
    zone_name: str
    container_name: str
    hostname: str
    ip: str 
    children: list["Server"]
