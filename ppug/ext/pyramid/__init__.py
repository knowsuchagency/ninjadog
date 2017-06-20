from ppug.ext.jinja2 import PugPreprocessor, jinja2_renderer
from jinja2.ext import Extension
from pyramid_jinja2 import *
from ppug import render
from pathlib import Path
from pprint import pprint
import logging


class PugTemplateRenderer(Jinja2TemplateRenderer):
    def __call__(self, value, system):
        try:
            system.update(value)
        except (TypeError, ValueError) as ex:
            raise ValueError('renderer was passed non-dictionary '
                             'as value: %s' % str(ex))
        template = self.template_loader()
        jinja2_string = template.render(system)
        print('this is the template to be rendered by pug:')
        print(jinja2_string)

        # filter out only dictionary values for pug rendering
        context = {k: v for k, v in system.items() if isinstance(v, dict)}
        print('this is the context to be rendered by pug template')
        pprint(context)
        print('this was the original system')
        pprint(system)
        return jinja2_renderer(jinja2_string,
                               system,
                               template_path=Path(template.filename),
                               context=context)


class PugRendererFactory(object):
    environment = None

    def __call__(self, info):
        name, package = info.name, info.package

        def template_loader():
            # attempt to turn the name into a caller-relative asset spec
            if ':' not in name and package is not None:
                try:
                    name_with_package = '%s:%s' % (package.__name__, name)
                    return self.environment.get_template(name_with_package)
                except TemplateNotFound:
                    pass

            return self.environment.get_template(name)

        return PugTemplateRenderer(template_loader)


def add_pug_renderer(config, name, settings_prefix='jinja2.', package=None):
    """
    This function is added as a method of a :term:`Configurator`, and
    should not be called directly.  Instead it should be called like so after
    ``pyramid_jinja2`` has been passed to ``config.include``:
    .. code-block:: python
       config.add_jinja2_renderer('.html', settings_prefix='jinja2.')
    It will register a new renderer, loaded from settings at the specified
    ``settings_prefix`` prefix. This renderer will be active for files using
    the specified extension ``name``.
    """
    renderer_factory = PugRendererFactory()
    config.add_renderer(name, renderer_factory)

    package = package or config.package
    resolver = DottedNameResolver(package=package)

    def register():
        registry = config.registry
        settings = config.get_settings()

        loader_opts = parse_loader_options_from_settings(
            settings,
            settings_prefix,
            resolver.maybe_resolve,
            package,
        )
        env_opts = parse_env_options_from_settings(
            settings,
            settings_prefix,
            resolver.maybe_resolve,
            package,
        )
        env = create_environment_from_options(env_opts, loader_opts)
        renderer_factory.environment = env

        registry.registerUtility(env, IJinja2Environment, name=name)

    config.action(
        ('pug-renderer', name), register, order=ENV_CONFIG_PHASE)


class PugPreprocessor2(Extension):
    """
    Renders pug template prior to jinja2 rendering
    """

    def preprocess(self, source, name, filename=None):
        """Render pug template."""
        if source.strip().startswith('extends'):
            return render(source, template_path=Path(filename) if filename else None)
        return source


def includeme(config):
    # config.add_jinja2_renderer('.pug')
    # config.add_jinja2_extension(PugPreprocessor, name='.pug')
    config.add_directive('add_pug_renderer', add_pug_renderer)
    config.add_pug_renderer('.pug')
