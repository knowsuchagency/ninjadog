from functools import wraps
from time import time


def idempotent(func):
    """Ensure the function runs only once."""
    cache = {}
    now = hash(time())

    @wraps(func)
    def wrapped(*args):
        if cache.get(args, now) == now:
            cache[args] = func(*args)
        return cache[args]
    return wrapped
