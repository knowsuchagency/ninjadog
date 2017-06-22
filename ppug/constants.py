import re
from pathlib import Path

import pkg_resources

EXTENSION_PATT = re.compile('extends\s+(\w+)')
PUG_CLI_PATH = Path(pkg_resources.resource_filename('ppug', 'node_modules/.bin/pug'))

