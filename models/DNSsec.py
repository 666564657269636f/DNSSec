from pathlib import Path
from subprocess import run, DEVNULL, PIPE


class DNSsec:

    def __init__(self, output: Path, zone_name: str, name: str):
        self.output: Path = output
        self.zone_name: str = zone_name
        self.name: str = name
        self.ksk: str | None = None
        self.zsk: str | None = None
        self.ds: str | None = None

    def generate(self) -> None:
        self.output.mkdir(parents = True, exist_ok = True)
        
        self._generate_ksk()
        self._generate_zsk()
        self._generate_ds()


    def sign(self):
        run(
            [
                'dnssec-signzone',
                '-S',
                '-o', self.zone_name,
                '-N', 'increment',
                f'db.{self.name}'
            ],
            check = True,
            cwd = self.output,
            stdout = DEVNULL,
            stderr = DEVNULL
        )


    def _generate_ksk(self) -> None:
        result = run(
            [
                'dnssec-keygen',
                '-K', str(self.output),
                '-a', 'ECDSAP256SHA256',
                '-n', 'ZONE',
                '-f', 'KSK',
                self.zone_name
            ],
            check = True,
            stdout = PIPE,
            stderr = DEVNULL,
            text = True
        )

        self.ksk = self.output / result.stdout.strip()


    def _generate_zsk(self) -> None:
        result = run(
            [
                'dnssec-keygen',
                '-K', str(self.output),
                '-a', 'ECDSAP256SHA256',
                '-n', 'ZONE',
                self.zone_name
            ],
            check = True,
            stdout = PIPE,
            stderr = DEVNULL,
            text = True
        )

        self.zsk = self.output / result.stdout.strip()


    def _generate_ds(self) -> None:
        result = run(
            [
                'dnssec-dsfromkey',
                str(self.ksk) + '.key'
            ],
            check = True,
            stdout = PIPE,
            stderr = DEVNULL,
            text = True
        )

        self.ds = result.stdout.strip()    

    def append_ds(self, ds: str) -> None:
        with open(
            file = self.output / f'db.{ self.name }', 
            mode = 'a',
            encoding = 'utf-8'
        ) as file:
            file.write(f'\n{ ds }\n')
