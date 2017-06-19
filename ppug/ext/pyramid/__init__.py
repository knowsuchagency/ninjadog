from jinja2.ext import Extension
from pyramid_jinja2 import _caller_package
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
    package = _caller_package(('pyramid', 'pyramid.', 'pyramid_jinja2'))
    config.add_jinja2_renderer('.pug', package=package)
    config.add_jinja2_extension(PugPreprocessor, name='.pug')

    # always insert default search path relative to package
    default_search_path = '%s:' % (package.__name__,)
    config.add_jinja2_search_path(default_search_path, name='.pug')

