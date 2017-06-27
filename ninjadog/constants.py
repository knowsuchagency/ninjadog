import re
import subprocess as sp
import typing as T
from pathlib import Path


EXTENSION_PATT = re.compile('(?:extends|include)\s+(.+)')
PUG_CLI_PATH = str(Path(sp.Popen(('which', 'pug'), stdout=sp.PIPE).communicate()[0].decode('utf8').strip()).absolute()) \
    if sp.Popen(('which', 'npm'), stdout=sp.DEVNULL).wait() == 0 else None

