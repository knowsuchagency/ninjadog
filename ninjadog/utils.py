import typing as T
from functools import partial
from json import dumps
from pathlib import Path

from .constants import EXTENSION_PATT

jsonify = partial(dumps, skipkeys=True, default=lambda _: '', ensure_ascii=False)
