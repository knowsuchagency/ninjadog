# -*- coding: utf-8 -*-

"""Main module."""
import shlex
import json
import subprocess as sp
import typing as T
from pathlib import Path

from ninjadog.constants import PUG_CLI_PATH
from ninjadog.utils import jsonify

from jinja2 import Template


def render(string: str = '',
           file: T.Union[Path, str] = None,
           context: T.Any = None,
           pretty: bool = False,
           pug_cli_path: str = None,
           with_jinja: bool = False) -> str:
    """
    Render a pug template through the pug cli.
    
    Args:
        string: a string in pug syntax to be rendered
        file: the path to a pug template
        context: the data to be passed to the template
        pretty: pretty html output
        pug_cli_path: path to the pug cli
        with_jinja: render jinja2 template syntax as well

    Returns: rendered html

    """

    if pug_cli_path is None and PUG_CLI_PATH is None:
        msg = "the pug command was not found. Did you install it?\n" \
              "brew install npm\n" \
              "npm install -g pug-cli"
        raise ValueError(msg)
    elif pug_cli_path is None:
        pug_cli_path = PUG_CLI_PATH

    # create Path object if file argument is given
    # Path() is idempotent so this shouldn't make any difference
    # if the file argument is of type Path
    filepath = Path(str(file)) if file else file

    # if filepath is given instead of a string argument,
    # return render of string
    if filepath and not string:
        with filepath.open() as fp:
            return render(fp.read(),
                          filepath,
                          context=context,
                          pretty=pretty,
                          pug_cli_path=pug_cli_path)

    cmd = shlex.quote(pug_cli_path)
    path = '-p {}'.format(shlex.quote(str(filepath))) if filepath else ''
    pretty_print = '-P' if pretty else ''

    if context is None:
        context_arg = ''
    elif isinstance(context, str):
        context_arg = '-O {}'.format(shlex.quote(context))
    else:
        context_arg = '-O {}'.format(shlex.quote(jsonify(context)))

    pug_cli = sp.Popen(shlex.split('{} {} {} {}'.format(cmd, context_arg, path, pretty_print)),
                       stdin=sp.PIPE,
                       stdout=sp.PIPE,
                       cwd=str(filepath.parent) if filepath else None,
                       universal_newlines=True,
                       )
    html, _ = pug_cli.communicate(string)

    if with_jinja:
        if isinstance(context, str):
            context = json.loads(context)
        return Template(html).render(context)

    return html

