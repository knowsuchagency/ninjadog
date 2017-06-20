from pathlib import Path
from .constants import EXTENSION_PATT



def get_extensions(filepath) -> Path:
    """
    Yield Path objects for pug templates that the pug
    template extends from.
    """
    filepath = Path(filepath)
    parent_path = filepath.parent
    with open(filepath) as fp:
        match = EXTENSION_PATT.search(fp.read())
        if match:
            found = match.group(1)
            if not found.endswith('.pug'):
                found += '.pug'
            path = Path(parent_path, found)
            yield path
            yield from get_extensions(path)
        else:
            return
