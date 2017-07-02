import typing as T
from pathlib import Path

from pyramid.path import AssetResolver

from ninjadog.ninjadog import render
from ninjadog.decorators import idempotent


def changed(dictionary: dict, key: T.Any, value: T.Any) -> bool:
    """
    Return true if the value for the given key in the dictionary has changed.

    Args:
        dictionary: dict
        key: any
        value: any

    Returns:

    """
    previous = dictionary.get(key)
    dictionary[key] = value
    return previous != value


def truth(value: T.Union[bool, str]) -> bool:
    """
    Return whether the value is True or not.

    Args:
        value: an element parsed from a settings dictionary

    Returns: bool

    """
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        return value.lower().startswith('t')


def resolve(path: str, caller=None) -> Path:
    """
    Return the path of the given string, given a path or asset spec.

    Args:
        path: absolute or relative path or asset spec
        caller: the python module or package that called the function

    Returns: Path to file

    """
    if ':' in path:
        return Path(AssetResolver().resolve(path).abspath())
    elif Path(path).is_absolute():
        return Path(path)

    return Path(Path(caller.__file__).parent, path).absolute()


@idempotent
def remove_file_if_exists(file: Path) -> True:
    """
    Removes the file from the file system if it exists.

    Args:
        file: filepath

    Returns: True

    """
    if file.exists():
        file.unlink()

    return True


class PugRendererFactory:
    template_cache = {}

    def __init__(self, info):
        self.reload = info.settings['reload_all'] or info.settings['reload_templates']
        self.cached = truth(info.settings.get('ninjadog.cache', False))

        self.template_path = resolve(info.name, info.package)

    def __call__(self, value, system):
        if not isinstance(value, dict): raise ValueError('view must return dict')

        context = system
        context.update(value)

        if self.cached:
            html_file = self.template_path.with_suffix('.html')
            remove_file_if_exists(html_file)
            template_changed = False

            if self.reload:
                template_text = self.template_path.read_text()
                template_changed = changed(PugRendererFactory.template_cache,
                                           self.template_path, template_text)

            if (not html_file.exists()) or (self.reload and template_changed):
                html = render(file=self.template_path, context=context, with_jinja=True)
                html_file.write_text(html)

                return html

            return html_file.read_text()

        return render(file=self.template_path, context=context, with_jinja=True)


def includeme(config):
    config.add_renderer('.pug', PugRendererFactory)
