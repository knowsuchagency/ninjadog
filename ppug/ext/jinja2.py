from jinja2.ext import Extension
from jinja2 import Environment
from ppug import render

from tempfile import TemporaryDirectory, NamedTemporaryFile
from pathlib import Path
import typing as T
import re


EXTENSION_PATT = re.compile('extends\s+(\w+)')


class PugPreprocessor(Extension):
    """
    Renders pug template prior to jinja2 rendering
    """

    def preprocess(self, source, name, filename=None):
        """Render pug template."""
        return render(source, template_path=Path(filename) if filename else None)


def get_extensions(filepath) -> Path:
    """
    Yield Path objects for pug templates that the pug
    template extends from.
    """
    filepath = Path(filepath)
    parent_path = filepath.parent
    with open(filepath) as fp:
        match = EXTENSION_PATT.search(fp.read())
        if match:
            found = match.group(1)
            if not found.endswith('.pug'):
                found += '.pug'
            path = Path(parent_path, found)
            yield path
            yield from get_extensions(path)
        else:
            return


def jinja2_renderer(text: str,
                    system: dict,
                    template_path: Path,
                    context: dict=None,
                    ):
    """
    Render pug templates that extend from other pug templates
    that have jinja2 syntax
    
    :param text: text of the original template
    :param system: the global context to be passed to jinja templates
    :param template_path: the path of the original template
    :param context: elements of the global context that are json-serializable
    :return: 
    """
    # early return - template does not extend
    extends = EXTENSION_PATT.search(text)
    if not extends:
        return render(text, template_path, context)

    with TemporaryDirectory() as tempdir:

        # first, render all the extensions in jinja2
        # and write them to the temporary directory
        extensions = get_extensions(template_path)
        env = Environment()
        env.globals = system
        for template in extensions:
            with open(template) as old_template:
                old_template_render = env.from_string(old_template.read()).render()
                new_template_file = Path(tempdir, template.name)
                with open(new_template_file, 'w') as newfile:
                    newfile.write(old_template_render)

        # create a copy of the original template in the temporary
        # directory relative to the now-rendered pug templates
        extended_path = Path(tempdir, template_path.name)
        return render(text, extended_path, context)





