import re
import subprocess as sp
from pathlib import Path
from tempfile import gettempdir


EXTENSION_PATT = re.compile('(?:extends|include)\s+(.+)')
PUG_CLI_PATH = str(Path(sp.Popen(('which', 'pug'), stdout=sp.PIPE).communicate()[0].decode('utf8').strip()).absolute()) \
    if sp.Popen(('which', 'npm'), stdout=sp.DEVNULL).wait() == 0 else None

# will likely be deprecated in the future as it's no longer being used
TEMPDIR = Path(gettempdir(), '.ninjadog/')

