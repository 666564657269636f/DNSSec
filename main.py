from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template
from yaml import safe_load


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


def generate_compose(config: dict[str, list[dict[str, str]]], template_path: Path, output_path: Path) -> None:
    parent: str = str(template_path.parent)
    template_file = str(template_path.name)

    env: Environment = Environment(loader=FileSystemLoader(searchpath=parent))
    template: Template = env.get_template(name=template_file)

    compose_content: str = template.render(servers=config['servers'])

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(data=compose_content, encoding="utf-8")


def main() -> None:
    config: dict[str, list[dict[str, str]]] = load_config(path=CONFIG_PATH / 'lab.yml')

    generate_compose(config=config, template_path=DOCKER_COMPOSE_TEMPLATE_PATH, output_path=DOCKER_COMPOSE_PATH)


if __name__ == "__main__":
    main()
