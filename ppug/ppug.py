# -*- coding: utf-8 -*-

"""Main module."""
from tempfile import NamedTemporaryFile
from pathlib import Path
import typing as T
import subprocess as sp
import logging
import shlex
import json

def jsonify(obj: T.Any) -> T.Optional[str]:
    if isinstance(obj, str):
        try:
            json.loads(obj)
            # valid string, return the object
            return obj
        except json.decoder.JSONDecodeError:
            logging.error(f'{obj} is not a valid json string')
            raise
    else:
        try:
            result = json.dumps(obj)
            # serializable
            return result
        except TypeError:
            logging.error(f'{obj} is not json serializable')
            raise


def render(text: str, template_path: Path = None, context: T.Any=None) -> str:
    """
    Convert pug template to html.

    A Path variable may be passed for instances where
    the pug-cli needs to know the path to other templates
    
    i.e. where a .pug template begins with the `extends` keyword
    .
    
    The context can either be a json string or a json-serializable object
    """
    PUG_CLI_PATH = Path(__file__).parent.joinpath('node_modules/.bin/pug')

    with NamedTemporaryFile('w') as fp:
        fp.write(text)
        fp.seek(0)

        path_argument = f'-p {shlex.quote(str(template_path))}' if template_path else ''
        context_argument = f'-O {shlex.quote(jsonify(context))}' if context else ''

        return sp.run(f'{str(PUG_CLI_PATH)} {path_argument} {context_argument} < {shlex.quote(fp.name)}',
                      shell=True,
                      stdout=sp.PIPE,
                      cwd=template_path.parent if template_path else None,
                      ).stdout.decode('utf8')
