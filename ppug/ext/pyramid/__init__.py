from jinja2.ext import Extension
from pyramid_jinja2 import _caller_package

from pathlib import Path

from ppug import render
from ppug import render as preprocessor

from pyramid_mako import (
    MakoRendererFactory,
    parse_options_from_settings,
    PkgResourceTemplateLookup,
    )


class PugPreprocessor(Extension):
    """
    Renders pug template prior to jinja2 rendering
    """

    def preprocess(self, source, name, filename=None):
        "Renders pug template if filename has .pug extension"
        return render(source, template_path=Path(filename))


class PugRenderer:
    def __init__(self, info):
        info.settings['mako.preprocessor'] = preprocessor
        factory = MakoRendererFactory()
        self.makoRenderer = factory(info)

    def __call__(self, value, system):
        return self.makoRenderer(value, system)


def includeme(config):
    config.add_renderer('.pug', PugRenderer)
