from jinja2.ext import Extension
from jinja2 import Environment
from ppug.constants import EXTENSION_PATT
from ppug.utils import get_extensions
from ppug import render

from tempfile import TemporaryDirectory
from pathlib import Path


class PugPreprocessor(Extension):
    """
    Renders pug template prior to jinja2 rendering
    """

    def preprocess(self, source, name, filename=None):
        """Render pug template."""
        return render(source, template_path=Path(filename) if filename else None)


def jinja2_renderer(text: str,
                    template_path: Path = None,
                    context: dict = None,
                    ):
    """
    Render pug templates that extend from other pug templates
    that have jinja2 syntax
    
    :param text: text of the original template
    :param template_path: the path of the original template
    :param context: elements of the global context that are json-serializable
    :return: 
    """
    # initialize jinja2 environment
    env = Environment()
    env.globals = context if context else {}

    # early return - template does not extend
    extends = EXTENSION_PATT.search(text)
    if not extends:
        return env.from_string(render(text, template_path, context)).render()
    elif not template_path:
        msg = 'You must pass the path to the template being rendered since it extends from other templates'
        raise ValueError(msg)

    with TemporaryDirectory() as tempdir:

        # first, render all the extensions in jinja2
        # and write them to the temporary directory
        extensions = get_extensions(template_path)
        for extension in extensions:
            with open(extension) as jinja2_template:
                rendered_jinja = env.from_string(jinja2_template.read()).render()
                new_template_file = Path(tempdir, extension.name)
                with open(new_template_file, 'w') as newfile:
                    newfile.write(rendered_jinja)

        # create a copy of the original template in the temporary
        # directory relative to the now-rendered pug templates
        extended_path = Path(tempdir, template_path.name)
        return render(text, extended_path, context)
