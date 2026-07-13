from pathlib import Path

from yaml import safe_load

from models.JinjaRender import JinjaRender
from models.BindConfigGenerator import BindConfigGenerator
from models.Server import Server


CONFIG_PATH: Path = Path('config')
MODELS_PATH: Path = Path('models')
OUTPUT_PATH: Path = Path('output')
TEMPLATES_PATH: Path = Path('templates')

DOCKER_COMPOSE_PATH: Path = OUTPUT_PATH / 'docker-compose.yml'
DOCKER_COMPOSE_TEMPLATE_PATH: Path = TEMPLATES_PATH / 'docker-compose.yml.j2'


def load_config(path: Path) -> dict[str, list[dict[str, str]]]:
    with path.open("r", encoding="utf-8") as file:
        data: dict[str, list[dict[str, str]]] = safe_load(file)

    return data


def main() -> None:
    config: dict[str, list[dict[str, str]]] = load_config(path=CONFIG_PATH / 'lab.yml')

    JinjaRender.render(template_path=DOCKER_COMPOSE_TEMPLATE_PATH, output_path=DOCKER_COMPOSE_PATH, **config)
    
    for server in config['servers']:
        bind: BindConfigGenerator = BindConfigGenerator(server=Server(
            server['name'],
            server['container_name'],
            server['hostname'],
            server['ip']
        ))
        bind.generate_config()


if __name__ == "__main__":
    main()
