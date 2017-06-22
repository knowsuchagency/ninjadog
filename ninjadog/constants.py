import re
import subprocess as sp
import typing as T
from pathlib import Path

EXTENSION_PATT: re.sre_parse.Pattern
PUG_CLI_PATH: T.Optional[Path]

EXTENSION_PATT = re.compile('(?:extends|include)\s+(.+)')
PUG_CLI_PATH = Path(sp.run(('which', 'pug'), stdout=sp.PIPE).stdout.decode('utf8').strip()) \
    if sp.run(('which', 'npm'), stdout=sp.DEVNULL).returncode == 0 else None

