"""ninjadog v0.3.4

Render pug templates to html.

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


Strings may be passed via pipe using `-` argument.

i.e. 

echo 'h1 hello {{ name }}' | ninjadog - -j -c '{"name": "Sam"}'

outputs

<h1>hello Sam</h1>

"""
from docopt import docopt
import sys

from ninjadog import render


def main(argv=None):
    """Render pug template to stdout."""
    args = docopt(__doc__, argv=argv, version='0.3.4')

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
