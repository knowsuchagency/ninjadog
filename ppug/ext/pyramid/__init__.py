from jinja2.ext import Extension
from ppug import render


class PugPreprocessor(Extension):
    """
    Renders pug template prior to jinja2 rendering
    """

    def preprocess(self, source, name, filename=None):
        "Renders pug template if filename has .pug extension"
        if filename and filename.endswith('.pug'):
            return render(source)
        return source


def includeme(config):
    config.add_jinja2_extension(PugPreprocessor)


if __name__ == '__main__':
    from jinja2 import Environment
    from jinja2 import FileSystemLoader
    from tempfile import TemporaryDirectory, NamedTemporaryFile
    with TemporaryDirectory() as tempdir:
        with NamedTemporaryFile(dir=tempdir, suffix='.pug') as fp:
            string = 'h1 hello {{ name }}'
            fp.write(string.encode('utf8'))
            fp.seek(0)

            loader = FileSystemLoader(tempdir)
            env = Environment(extensions=(PugPreprocessor,),
                              loader=loader)
            print(env.list_templates())
            template = env.get_or_select_template(env.list_templates())
            print(template.render(name='Stephan Fitzpatrick'))
