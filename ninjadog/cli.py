"""ninjadog v0.3.3

Usage:
    ninjadog string [options] <string>
    ninjadog file [options] <file>
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


Render pug templates to html. 

Use "-" to read from stdin i.e. echo "h1 hello" | ninjadog -
"""
from docopt import docopt
import sys

from ninjadog import render


def main(argv=None):
    """Render pug template to stdout."""
    args = docopt(__doc__, argv=argv, version='0.3.3')

    if args['--file'] and args['<file>']:
        raise ValueError("Cannot combine --file and <file> arguments")

    string = sys.stdin.read() if args['-'] else args['<string>']
    file = args['--file'] or args['<file>']
    pretty = args['--pretty']
    context = args['--context']
    with_jinja = args['--with-jinja']
    verbose = args['--verbose']

    output = render(string=string, file=file, pretty=pretty, context=context, with_jinja=with_jinja)

    if verbose:
        print(args, file=sys.stderr, end='\n\n')

    return output


if __name__ == "__main__":
    main()
