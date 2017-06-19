from jinja2.ext import Extension
from pathlib import Path
from ppug import render


class PugPreprocessor(Extension):
    """
    Renders pug template prior to jinja2 rendering
    """

    def preprocess(self, source, name, filename=None):
        """Render pug template."""
        return render(source, template_path=Path(filename) if filename else None)
