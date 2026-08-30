from dataclasses import dataclass

@dataclass
class Server:
    name: str
    container_name: str
    hostname: str
    ip: str 
    children: list["Server"]
