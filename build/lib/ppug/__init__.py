# -*- coding: utf-8 -*-

"""Top-level package for ppug."""

__author__ = """Stephan Fitzpatrick"""
__email__ = 'knowsuchagency@gmail.com'
__version__ = '0.1.0'

from tempfile import NamedTemporaryFile
from pathlib import Path
import subprocess as sp
import shlex


def render(text: str, template_path: Path=None) -> str:
    """
    Convert pug template to html.
    
    A Path variable may be passed for instances such as
    in the template where the extends keyword needs it.
    """
    PUG_CLI_PATH = Path(__file__).parent.joinpath('node_modules/.bin/pug')

    with NamedTemporaryFile('w') as fp:
        fp.write(text)
        fp.seek(0)

        path_argument = f'-p {str(template_path)}' if template_path else ''
        return sp.run(f'{str(PUG_CLI_PATH)} {path_argument} < {shlex.quote(fp.name)}',
                      shell=True,
                      stdout=sp.PIPE,
                      cwd=template_path.parent if template_path else None,
                      ).stdout.decode('utf8')


if __name__ == '__main__':
    from textwrap import dedent
    string = dedent("""
    p
      a(href='google.com') google
      |
      | to
      |
      a(href='github.com') github
    """)
    print(render(string))
