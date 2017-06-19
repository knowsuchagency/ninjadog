from jinja2.ext import Extension
from ppug import render


class PugPreprocessor(Extension):
    """
    Renders pug template prior to jinja2 rendering
    """

    def preprocess(self, source, name, filename=None):
        return render(source)


def includeme(config):
    config.add_jinja2_extension(PugPreprocessor, name='.pug')
