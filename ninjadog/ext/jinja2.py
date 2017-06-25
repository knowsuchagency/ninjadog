import typing as T
from functools import partial
from pathlib import Path

from jinja2 import Environment
from jinja2.ext import Extension

from ninjadog import render as _render


class PugPreprocessor(Extension):
    """
    Jinja2 preprocessor that renders pug to html.
    """

    def preprocess(self, source, name, filename=None):
        """
        Render pug string to html.
        
        Args:
            source: string to be rendered
            name: the name of the template
            filename: the filepath of the template

        Returns: rendered html

        """
        return _render(source, filepath=Path(filename) if filename else None)


def jinja2_renderer(string: str = '',
                    filepath: Path = None,
                    context: dict = None,
                    pretty: bool = False,
                    pug_cli_path: T.Union[Path, str] = None,
                    ) -> str:
    """
    Renders pug and jinja2 syntax formatted string to html.
    
    Jinja2 will be rendered first and can accept any Python
    object as its context. 
    
    The pug-template engine will only receive json-serializable
    data, however.
    
    Args:
        string: the string to be rendered
        filepath: the path to the template to be rendered
        context: the data to be passed to the template engines
        pretty: pretty html output
        pug_cli_path: Path to the pug cli

    Returns: html string

    """
    # lock arguments
    pug_renderer = partial(_render,
                           context=context,
                           filepath=filepath,
                           pretty=pretty,
                           pug_cli_path=pug_cli_path)

    # initialize jinja2 environment
    env = Environment()
    env.globals = context if context else {}

    return env.from_string(pug_renderer(string)).render()
