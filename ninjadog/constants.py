import re
import subprocess as sp
from pathlib import Path

EXTENSION_PATT = re.compile('(?:extends|include)\s+(.+)')
PUG_CLI_PATH = Path(sp.run(('which', 'pug'), stdout=sp.PIPE).stdout.decode('utf8').strip())

