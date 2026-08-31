from pathlib import Path

from models.BindConfigGenerator import BindConfigGenerator
from models.UnboundConfigGenerator import UnboundConfigGenerator
from models.DockerComposeGenerator import DockerComposeGenerator
from models.Server import Server
from models.YAML import YAML
from models.DNSsec import DNSsec
from models.ResolverGenerator import ResolverGenerator


CONFIG_PATH: Path = Path('config')
MODELS_PATH: Path = Path('models')

OUTPUT_PATH: Path = Path('output')
OUTPUT_DNS_PATH: Path = Path('output/dns')
OUTPUT_RESOLVER_PATH: Path = Path('output/resolver')


TEMPLATES_PATH: Path = Path('templates')
TEMPLATES_BIND_PATH: Path = TEMPLATES_PATH / 'bind'
TEMPLATES_UNBOUND_PATH: Path = TEMPLATES_PATH / 'unbound'

LAB_PATH: Path = CONFIG_PATH / 'lab.yml'


def generate_dnssec(server: Server, input_dir: Path, output_dir: Path) -> str:
    bind: BindConfigGenerator = BindConfigGenerator(
        server = server,
        input_dir = input_dir,
        output_dir = output_dir / server.name
    )

    bind.generate()

    dnssec = DNSsec(
        output = output_dir / server.name,
        zone_name = server.name
    )

    dnssec.generate()

    for child in server.children:
        ds: str = generate_dnssec(
            server = child,
            input_dir = input_dir,
            output_dir = output_dir
        )

        dnssec.append_ds(ds = ds)

    dnssec.sign()

    return dnssec.ds


def main() -> None:
    servers: list[Server] = YAML(LAB_PATH).servers

    unbound: UnboundConfigGenerator = UnboundConfigGenerator(
        server = servers[0],
        input_dir = TEMPLATES_UNBOUND_PATH, 
        output_dir = OUTPUT_RESOLVER_PATH
    )

    unbound.generate()

    docker_compose: DockerComposeGenerator = DockerComposeGenerator(
        server = servers[0],
        input_dir = TEMPLATES_PATH,
        output_dir = OUTPUT_PATH
    )

    docker_compose.generate()

    for server in servers:
        ds: str = generate_dnssec(
            server = server,
            input_dir = TEMPLATES_BIND_PATH,
            output_dir = OUTPUT_DNS_PATH
        )

        resolver: ResolverGenerator = ResolverGenerator(
            output = OUTPUT_RESOLVER_PATH
        )

        resolver.append_ds(ds = ds)


if __name__ == "__main__":
    main()
