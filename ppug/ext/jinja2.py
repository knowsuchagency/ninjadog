from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory

from jinja2 import Environment
from jinja2.ext import Extension

from ppug import render as _render
from ppug.constants import EXTENSION_PATT
from ppug.utils import get_extensions


class PugPreprocessor(Extension):
    """
    Renders pug template prior to jinja2 rendering
    """

    def preprocess(self, source, name, filename=None):
        """Render pug template."""
        render = _render
        return render(source, filepath=Path(filename) if filename else None)


def jinja2_renderer(string: str = '',
                    filepath: Path = None,
                    context: dict = None,
                    pretty: bool = False,
                    ):
    """
    Render pug templates that extend from other pug templates
    that have jinja2 syntax
    
    :param string: text of the original template
    :param filepath: the path of the original template
    :param context: elements of the global context that are json-serializable
    :return: 
    """
    # lock pretty-print argument
    render = partial(_render, pretty=pretty)

    # initialize jinja2 environment
    env = Environment()
    env.globals = context if context else {}

    # early return - template does not extend
    extends = EXTENSION_PATT.search(string)
    if not extends:
        return env.from_string(render(string, filepath, context)).render()
    elif not filepath:
        msg = 'You must pass the path to the template being rendered since it extends from other templates'
        raise ValueError(msg)

    with TemporaryDirectory() as tempdir:

        # first, render all the extensions in jinja2
        # and write them to the temporary directory
        extensions = get_extensions(filepath)
        for extension in extensions:
            with open(extension) as jinja2_template:
                rendered_jinja = env.from_string(jinja2_template.read()).render()
                new_template_file = Path(tempdir, extension.name)
                with open(new_template_file, 'w') as newfile:
                    newfile.write(rendered_jinja)

        # create a copy of the original template in the temporary
        # directory relative to the now-rendered pug templates
        extended_path = Path(tempdir, filepath.name)
        return render(string, extended_path, context)
