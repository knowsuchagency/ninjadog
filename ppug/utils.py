import typing as T
from functools import partial
from json import dumps
from pathlib import Path

from .constants import EXTENSION_PATT

jsonify = partial(dumps, skipkeys=True, default=lambda _: '', ensure_ascii=False)


def get_extensions(file: T.Union[str, Path]) -> T.Sequence[Path]:
    """
    Yield Path objects for pug templates that the pug
    template extends from.
    """
    file = Path(file)
    parent_path = file.parent
    with open(file) as fp:
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
