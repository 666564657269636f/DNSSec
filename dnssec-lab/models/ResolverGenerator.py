from pathlib import Path
from subprocess import run, DEVNULL, PIPE


class ResolverGenerator:

    def __init__(self, output: Path):
        self.output: Path = output


    def append_ds(self, ds: str) -> None:
        with open(
            file = self.output / 'root.key', 
            mode = 'a',
            encoding = 'utf-8'
        ) as file:
            file.write(f'{ ds }\n')
