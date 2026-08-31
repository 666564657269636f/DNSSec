from pathlib import Path

from models.Server import Server
from models.JinjaRender import JinjaRender


class BindConfigGenerator:

    def __init__(self, server: Server, input_dir: Path, output_dir: Path):
        self.server: Server = server
        self.input_dir: Path = input_dir
        self.output_dir: Path = output_dir


    def generate(self) -> None:
        self._db_zone()
        self._named_conf()
        self._named_conf_local()
        self._named_conf_options()


    def _db_zone(self) -> None:
        template_path: Path = self.input_dir / 'db.zone.j2'
        output_path: Path = self.output_dir / f'db.{ self.server.name }'
        JinjaRender.render(
            template_path = template_path, 
            output_path = output_path, 
            name = self.server.name, 
            ip = self.server.ip,
            children = self.server.children
        )


    def _named_conf(self) -> None:
        template_path: Path = self.input_dir / 'named.conf.j2'
        output_path: Path = self.output_dir / 'named.conf'
        JinjaRender.render(
            template_path = template_path, 
            output_path = output_path, 
        )


    def _named_conf_local(self): 
        template_path: Path = self.input_dir / 'named.conf.local.j2'
        output_path: Path = self.output_dir / 'named.conf.local'
        JinjaRender.render(
            template_path = template_path, 
            output_path = output_path, 
            name = self.server.name,
            zone_name = self.server.zone_name
        )


    def _named_conf_options(self):
        template_path: Path = self.input_dir / 'named.conf.options.j2'
        output_path: Path = self.output_dir / 'named.conf.options'
        JinjaRender.render(
            template_path = template_path, 
            output_path = output_path
        )
