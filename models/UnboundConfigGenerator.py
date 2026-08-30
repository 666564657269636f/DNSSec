from pathlib import Path

from models.Server import Server
from models.JinjaRender import JinjaRender


class UnboundConfigGenerator:

    def __init__(self, server: Server, input_dir: Path, output_dir: Path):
        self.server: Server = server
        self.input_dir: Path = input_dir
        self.output_dir: Path = output_dir


    def generate(self) -> None:
        self._root_hints()
        self._root_key()
        self._unbound_conf()


    def _root_hints(self) -> None:
        template_path: Path = self.input_dir / 'root.hints.j2'
        output_path: Path = self.output_dir / 'root.hints'
        JinjaRender.render(
            template_path = template_path, 
            output_path = output_path, 
            name = self.server.name, 
            ip = self.server.ip
        )


    def _root_key(self) -> None:
        template_path: Path = self.input_dir / 'root.key.j2'
        output_path: Path = self.output_dir / 'root.key'
        JinjaRender.render(
            template_path = template_path, 
            output_path = output_path
        )


    def _unbound_conf(self): 
        template_path: Path = self.input_dir / 'unbound_conf.j2'
        output_path: Path = self.output_dir / 'unbound_conf'
        JinjaRender.render(
            template_path = template_path, 
            output_path = output_path, 
        )
