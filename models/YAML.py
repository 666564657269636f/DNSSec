from pathlib import Path
from yaml import safe_load

from models.Server import Server


class YAML:

    def __init__(self, path: Path):
        self.path: Path = path
        self.servers: list[Server] = self._load_servers()

    def _load_servers(self) -> list[Server]:
        with self.path.open('r', encoding = 'utf-8') as file:
            data = safe_load(file)

        return [
            self._create_server(server)
            for server in data['servers']
        ]

    def _create_server(self, data: dict) -> Server:
        children = [
            self._create_server(child)
            for child in data.get('children', [])
        ]

        return Server(
            name = data['name'],
            container_name = data['container_name'],
            hostname = data['hostname'],
            ip = data['ip'],
            children = children
        )
