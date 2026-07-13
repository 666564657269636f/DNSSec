from pathlib import Path

from models.Server import Server
from models.JinjaRender import JinjaRender


class BindConfigGenerator:

    TEMPLATE_BIND_PATH: Path = Path('templates/bind')


    def __init__(self, server: Server):
        self.server: Server = server
        self.output_path: Path = Path(f'output/config/{ self.server.name }/')


    def generate_config(self) -> None:
        self._write_named_conf()
        self._write_named_conf_options()
        self._write_write_named_conf_local()
        self._write_db_zone()


    def _write_db_zone(self) -> None:
        pass


    def _write_named_conf(self) -> None:
        template_path: Path = self.TEMPLATE_BIND_PATH / 'named.conf.j2'
        output_path: Path = self.output_path / 'named.conf'
        JinjaRender.render(template_path=template_path, output_path=output_path, context=None)


    def _write_write_named_conf_local(self): 
        template_path: Path = self.TEMPLATE_BIND_PATH / 'named.conf.local.j2'
        output_path: Path = self.output_path / 'named.conf.local'
        JinjaRender.render(template_path=template_path, output_path=output_path, name=self.server.name)


    def _write_named_conf_options(self):
        template_path: Path = self.TEMPLATE_BIND_PATH / 'named.conf.options.j2'
        output_path: Path = self.output_path / 'named.conf.options'
        JinjaRender.render(template_path=template_path, output_path=output_path, context=None)
