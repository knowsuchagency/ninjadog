def test_cli_string_argument():
    from ninjadog.cli import main
    assert main(('string', "h1 hello, world")) == '<h1>hello, world</h1>'


def test_cli_file_argument():
    from ninjadog.cli import main
    from ninjadog.utils import jsonify
    from tempfile import NamedTemporaryFile

    context = jsonify({'title': 'hello, world'})

    with NamedTemporaryFile('w+') as file:
        file.write('h1= title');
        file.seek(0)
        assert main(('file', file.name, '-c', context)) == '<h1>hello, world</h1>'


def test_cli_dir_argument(capsys):
    from ninjadog.cli import main
    from tempfile import TemporaryDirectory
    from pathlib import Path

    templates_dir = Path(Path(__file__).parent, 'pyramid/templates/')

    with TemporaryDirectory() as d:
        tempdir = Path(d)
        with capsys.disabled():
            print()
            main(('dir', str(templates_dir), str(tempdir)))

