from ppug.ext.jinja2 import jinja2_renderer
from pyramid_jinja2 import *
from pathlib import Path


class PugTemplateRenderer(Jinja2TemplateRenderer):
    def __call__(self, value, system):
        try:
            system.update(value)
        except (TypeError, ValueError) as ex:
            raise ValueError('renderer was passed non-dictionary '
                             'as value: %s' % str(ex))
        template = self.template_loader()
        jinja2_string = template.render(system)
        return jinja2_renderer(jinja2_string,
                               template_path=Path(template.filename),
                               context=system)


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


def includeme(config):
    config.add_directive('add_pug_renderer', add_pug_renderer)
    config.add_pug_renderer('.pug')
