"""ninjadog v0.5.2

Render pug templates to html.

Usage:
    ninjadog string [options] <string>
    ninjadog file [options] <file>
    ninjadog dir [options] <source> [<destination>]
    ninjadog - [options]
    ninjadog -h | --help
    ninjadog -V | --version


Options:
    -h --help                 show help and exit
    -V --version              show version and exit
    -f --file <file>          the filepath to the template
    -p --pretty               pretty print output
    -c --context <context>    json string to be passed as context
    -j --with-jinja           render jinja2 syntax as well as pug
    -v --verbose              verbose output
    -n --dry-run              verbose output and exit without executing
    <destination>             destination directory to render pug files to


Strings may be passed via pipe using `-` argument.

i.e.

echo 'h1 hello {{ name }}' | ninjadog - -j -c '{"name": "Sam"}'

outputs

<h1>hello Sam</h1>

"""
import sys
import typing as T
from pathlib import Path

from docopt import docopt

from ninjadog import render


def render_directory(source: Path, destination: Path = None, **kwargs):
    """
    Render a directory of pug templates.

    Args:
        source: the source directory
        destination: the destination directory [default: source]
        kwargs: arguments that will be passed to the ninjadog renderer

    Returns: None
    """
    destination = destination or source
    destination.mkdir(exist_ok=True)

    pug_templates = filter(lambda p: p.suffix == '.pug', source.iterdir())

    for template in pug_templates:
        rendered_template = render(file=template, **kwargs)
        new_template = Path(destination, template.stem).with_suffix('.html')
        new_template.write_text(rendered_template)
        print('Rendered', new_template.absolute())


def main(argv: T.Optional[T.Iterable] = None):
    """Render pug template to stdout."""
    args = docopt(__doc__, argv=argv, version='0.5.2')

    if args['--file'] and args['<file>']:
        raise ValueError("Cannot combine --file and <file> arguments")

    string = sys.stdin.read() if args['-'] else args['<string>']
    file = args['--file'] or args['<file>']
    pretty = args['--pretty']
    context = args['--context']
    with_jinja = args['--with-jinja']
    verbose = args['--verbose']
    dry_run = args['--dry-run']
    source = args['<source>']
    destination = args['<destination>']

    if dry_run or verbose:
        print(args, file=sys.stderr, end='\n\n')
    if dry_run:
        print('dry run, no changes made', file=sys.stderr)
        return

    if source:
        render_directory(Path(source), Path(destination), pretty=pretty, context=context, with_jinja=with_jinja)
        return

    output = render(string=string, file=file, pretty=pretty, context=context, with_jinja=with_jinja)
    return output


if __name__ == "__main__":
    main()
