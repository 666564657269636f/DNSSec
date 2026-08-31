from jinja2 import Template, FileSystemLoader, Environment
from pathlib import Path
from typing import Any

class JinjaRender:
    
    @staticmethod
    def render(template_path: Path, output_path: Path, **context: dict[str, Any]) -> None:
        env: Environment = Environment(loader=FileSystemLoader(searchpath=str(template_path.parent)))
        template: Template = env.get_template(template_path.name)
        content: str = template.render(**context)
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(data=content, encoding='utf-8')
