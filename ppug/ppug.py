# -*- coding: utf-8 -*-

"""Main module."""
import shlex
import subprocess as sp
import typing as T
from pathlib import Path
from tempfile import NamedTemporaryFile

from .constants import PUG_CLI_PATH
from .utils import jsonify


def render(string: str = '',
           filepath: T.Union[Path, str] = None,
           context: T.Any = None,
           pretty: bool = False) -> str:
    """
    Convert pug template to html.

    A Path variable may be passed for instances where
    the pug-cli needs to know the path to other templates
    
    i.e. where a .pug template begins with the `extends` keyword
    .
    
    The context can either be a json string or a json-serializable object
    """

    # create Path object if filepath argument is given
    # Path() is idempotent so this shouldn't make any difference
    # if the filepath argument is of type Path
    filepath = Path(filepath) if filepath else filepath

    # if filepath is given instead of a string argument,
    # return render of string
    if filepath and not string:
        with open(filepath) as fp:
            return render(fp.read(), filepath)

    with NamedTemporaryFile('w') as fp:
        fp.write(string)
        fp.seek(0)

        path = f'-p {shlex.quote(str(filepath))}' if filepath else ''
        context = f'-O {shlex.quote(jsonify(context))}' if context else ''
        pretty_print = '-P' if pretty else ''

        return sp.run(f'{str(PUG_CLI_PATH.absolute())} {pretty_print} {path} {context} < {shlex.quote(fp.name)}',
                      shell=True,
                      stdout=sp.PIPE,
                      cwd=filepath.parent if filepath else None,
                      ).stdout.decode('utf8')
