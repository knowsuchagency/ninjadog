from functools import partial
from json import dumps


jsonify = partial(dumps, skipkeys=True, default=lambda _: '', ensure_ascii=False)
