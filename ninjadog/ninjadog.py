# -*- coding: utf-8 -*-

"""Main module."""
import shlex
import subprocess as sp
import typing as T
from pathlib import Path
from tempfile import NamedTemporaryFile

from ninjadog.constants import PUG_CLI_PATH
from ninjadog.utils import jsonify


def render(string: str = '',
           filepath: T.Union[Path, str] = None,
           context: T.Any = None,
           pretty: bool = False,
           pug_cli_path: T.Union[Path, str] = None) -> str:
    """
    Render a pug template through the pug cli.
    
    Args:
        string: a string in pug syntax to be rendered
        filepath: the path to a pug template
        context: the data to be passed to the template
        pretty: pretty html output
        pug_cli_path: path to the pug cli

    Returns: rendered html

    """

    if pug_cli_path is None and PUG_CLI_PATH is None:
        msg = "the pug command was not found. Did you install it?\n" \
              "brew install npm\n" \
              "npm install -g pug-cli"
        raise ValueError(msg)
    elif pug_cli_path is None:
        pug_cli_path = PUG_CLI_PATH

    # create Path object if filepath argument is given
    # Path() is idempotent so this shouldn't make any difference
    # if the filepath argument is of type Path
    filepath = Path(filepath) if filepath else filepath

    # if filepath is given instead of a string argument,
    # return render of string
    if filepath and not string:
        with open(filepath) as fp:
            return render(fp.read(),
                          filepath,
                          context=context,
                          pretty=pretty,
                          pug_cli_path=pug_cli_path)

    with NamedTemporaryFile('w') as fp:
        fp.write(string)
        fp.seek(0)

        cmd = shlex.quote(str((Path(pug_cli_path).absolute())))
        path = f'-p {shlex.quote(str(filepath))}' if filepath else ''
        pretty_print = '-P' if pretty else ''

        if context is None:
            context_arg = ''
        elif isinstance(context, str):
            context_arg = f'-O {shlex.quote(context)}'
        else:
            context_arg = f'-O {shlex.quote(jsonify(context))}'

        input_file = shlex.quote(fp.name)

        return sp.run(f'{cmd} {context_arg} {path} {pretty_print} < {input_file}',
                      shell=True,
                      stdout=sp.PIPE,
                      cwd=filepath.parent if filepath else None,
                      ).stdout.decode('utf8')
