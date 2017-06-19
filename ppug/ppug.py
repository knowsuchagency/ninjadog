# -*- coding: utf-8 -*-

"""Main module."""
from tempfile import NamedTemporaryFile
from pathlib import Path
import subprocess as sp
import shlex


def render(text: str, template_path: Path = None) -> str:
    """
    Convert pug template to html.

    A Path variable may be passed for instances where
    the pug-cli needs to know the path to other templates
    
    i.e. where a .pug template begins with the `extends` keyword
    .
    """
    PUG_CLI_PATH = Path(__file__).parent.joinpath('node_modules/.bin/pug')

    with NamedTemporaryFile('w') as fp:
        fp.write(text)
        fp.seek(0)

        path_argument = f'-p {shlex.quote(str(template_path))}' if template_path else ''

        return sp.run(f'{str(PUG_CLI_PATH)} {path_argument} < {shlex.quote(fp.name)}',
                      shell=True,
                      stdout=sp.PIPE,
                      cwd=template_path.parent if template_path else None,
                      ).stdout.decode('utf8')
