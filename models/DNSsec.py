from pathlib import Path
from subprocess import run 

class DNSsec:

    def __init__(self, output: Path, zone_name: str):
        self.output: Path = output
        self.zone_name = zone_name
        self.ksk: Path | None = None
        self.zsk: Path | None = None
        self.ds: str | None = None

    def generate(self):
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
                f'db.{ self.zone_name }'
            ],
            check = True,
            cwd = self.output
        )

    def _generate_ksk(self):
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
            capture_output = True,
            text = True
        )

        self.ksk = self.output / result.stdout.strip()

    def _generate_zsk(self):
        result = run(
            [
                'dnssec-keygen',
                '-K', str(self.output),
                '-a', 'ECDSAP256SHA256',
                '-n', 'ZONE',
                self.zone_name
            ],
            check = True,
            capture_output = True,
            text = True
        )

        self.zsk = self.output / result.stdout.strip()

    def _generate_ds(self) -> str:
        result = run(
            [
                'dnssec-dsfromkey',
                str(self.ksk) + '.key'
            ],
            check = True,
            capture_output = True,
            text = True
        )

        return result.stdout.strip()
