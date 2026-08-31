from pathlib import Path

from models.Server import Server
from models.JinjaRender import JinjaRender


class DockerComposeGenerator:

    def __init__(self, server: Server, input_dir: Path, output_dir: Path):
        self.server: Server = server
        self.input_dir: Path = input_dir
        self.output_dir: Path = output_dir


    def generate(self) -> None:
        template_path: Path = self.input_dir / 'docker-compose.yml.j2'
        output_path: Path = self.output_dir / 'docker-compose.yml'
        JinjaRender.render(
            template_path = template_path, 
            output_path = output_path, 
            servers=[self.server]
        )
