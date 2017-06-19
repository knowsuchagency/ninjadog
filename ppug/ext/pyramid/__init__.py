from jinja2.ext import Extension
from pathlib import Path
from ppug import render


class PugPreprocessor(Extension):
    """
    Renders pug template prior to jinja2 rendering
    """

    def preprocess(self, source, name, filename=None):
        "Renders pug template if filename has .pug extension"
        return render(source, template_path=Path(filename))


def includeme(config):
    config.add_jinja2_renderer('.pug')
    config.add_jinja2_extension(PugPreprocessor)

