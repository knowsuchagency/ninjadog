from ppug.ext.jinja2 import PugPreprocessor


def includeme(config):
    config.add_jinja2_renderer('.pug')
    config.add_jinja2_extension(PugPreprocessor, name='.pug')

