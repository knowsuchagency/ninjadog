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


def add_pug_renderer(config, extension, mako_settings_prefix='mako.'):

    renderer_factory = MakoRendererFactory()
    config.add_renderer(extension, renderer_factory)

    def register():
        settings = config.registry.settings
        settings['{0}preprocessor'.format(mako_settings_prefix)] = preprocessor

        opts = parse_options_from_settings(settings, mako_settings_prefix, config.maybe_dotted)
        lookup = PkgResourceTemplateLookup(**opts)

        renderer_factory.lookup = lookup

    config.action(('pug-renderer', extension), register)


def includeme(config):
    config.add_directive('add_pug_renderer', add_pug_renderer)
    config.add_pug_renderer('.pug')
