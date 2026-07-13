from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader
from yaml import safe_load


CONFIG_PATH: Path = Path("config/lab.yml")
DOCKER_COMPOSE_TEMPLATE_PATH: Path = Path("templates/docker-compose.yaml.j2")
OUTPUT_PATH: Path = Path("output/docker-compose.yml")


def load_config(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as file:
        data: dict[str, Any] = safe_load(file)

    return data


def generate_compose(
    config: dict[str, Any],
    template_path: Path,
    output_path: Path,
) -> None:

    template_directory: Path = template_path.parent
    template_name: str = template_path.name

    environment: Environment = Environment(
        loader=FileSystemLoader(str(template_directory))
    )

    template = environment.get_template(template_name)

    compose_content: str = template.render(
        servers=config["servers"]
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path.write_text(
        compose_content,
        encoding="utf-8"
    )


def main() -> None:
    config: dict[str, Any] = load_config(CONFIG_PATH)

    generate_compose(
        config,
        DOCKER_COMPOSE_TEMPLATE_PATH,
        OUTPUT_PATH,
    )


if __name__ == "__main__":
    main()
