import re
from pathlib import Path

EXTENSION_PATT = re.compile('extends\s+(\w+)')
PUG_CLI_PATH = Path(__file__).parent.joinpath('node_modules/.bin/pug')
