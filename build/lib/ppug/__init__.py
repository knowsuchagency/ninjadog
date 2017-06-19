# -*- coding: utf-8 -*-

"""Top-level package for ppug."""

__author__ = """Stephan Fitzpatrick"""
__email__ = 'knowsuchagency@gmail.com'
__version__ = '0.1.0'

from tempfile import NamedTemporaryFile
from pathlib import Path
import subprocess as sp
import shlex


def render(text: str) -> str:
    """
    Convert pug template to html.
    """
    PUG_CLI_PATH = Path(__file__).parent.joinpath('node_modules/.bin/pug')

    with NamedTemporaryFile('w') as fp:
        fp.write(text)
        fp.seek(0)
        return sp.run(f'{str(PUG_CLI_PATH)} < {shlex.quote(fp.name)}',
                      shell=True,
                      stdout=sp.PIPE,
                      ).stdout.decode('utf8')


if __name__ == '__main__':
    string = """
    p
      a(href='google.com') google
      |
      | to
      |
      a(href='github.com') github
    """
    print(render(string))
