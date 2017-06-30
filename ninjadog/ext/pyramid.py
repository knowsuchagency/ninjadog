import typing as T
from pathlib import Path
from shutil import rmtree as rmdir

from pyramid.path import AssetResolver

from ninjadog.ninjadog import render
from ninjadog.constants import TEMPDIR


def get_and_update(dictionary: dict, key: T.Any, value: T.Any) -> T.Any:
    """
    Get the previous value for the key and update with the new value.
    
    Args:
        dictionary: dict
        key: any
        value: any

    Returns: the previous value for that key or the value if the key didn't exist

    """
    previous = dictionary.setdefault(key, value)
    dictionary.update({key: value})

    return previous


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


def run_once():
    """
    Creates the temporary directory at runtime idempotently.
    """
    has_run = False

    def logic():
        nonlocal has_run
        if not has_run:
            rmdir(TEMPDIR, ignore_errors=True)
            TEMPDIR.mkdir(exist_ok=True)
            has_run = True

    return logic


reset_tempdir = run_once()


class PugRendererFactory:
    def __init__(self, info):
        self.reload = info.settings['reload_all'] or info.settings['reload_templates']
        self.static_only = truth(info.settings.get('ninjadog.cache', False))

        self.template_path = resolve(info.name,
                                     info.package)
        self.template_name = self.template_path.name
        self.template_cache = {}

        if self.static_only:
            reset_tempdir()

    def __call__(self, value, system):
        if not isinstance(value, dict): raise ValueError('view must return dict')

        context = system
        context.update(value)

        if self.static_only:
            template_changed = False
            if self.reload:
                template_text = self.template_path.read_text()
                template_changed = get_and_update(self.template_cache, self.template_name,
                                                  template_text) != template_text

            template_file = Path(TEMPDIR, self.template_name)

            if (not template_file.exists()) or (self.reload and template_changed):
                html = render(file=self.template_path, context=context, with_jinja=True)
                template_file.write_text(html)

                return html

            return template_file.read_text()

        return render(file=self.template_path, context=context, with_jinja=True)


def includeme(config):
    config.add_renderer('.pug', PugRendererFactory)
