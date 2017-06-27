#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ninjadog` package."""

# TODO: test raises ValueError when pug cli can't be found and not passed explicitly to renderer
# TODO: add mypy testing
# TODO: test pyramid extension

import pytest


def test_npm_installed():
    from subprocess import Popen
    assert Popen(('which', 'npm')).wait() == 0, 'npm must be installed'


def test_pug_cli_exists():
    from pathlib import Path
    from ninjadog.constants import PUG_CLI_PATH
    assert Path(PUG_CLI_PATH).exists()


def test_hello_world():
    from ninjadog import render
    assert render('h1 hello world') == '<h1>hello world</h1>'


def test_pug_variable():
    from ninjadog import render
    assert render('h1= title', context={'title': 'hello world'}) == '<h1>hello world</h1>'


def test_jinja2_variable():
    from ninjadog import render
    assert render('h1 {{ title }}', context={'title': 'hello world'}, with_jinja=True) == '<h1>hello world</h1>'


def test_context():
    import ninjadog
    context = {'name': 'Derp'}
    assert ninjadog.render('h1 hello #{ name }', context=context) == '<h1>hello Derp</h1>'
    assert ninjadog.render("h1= name", context=context) == '<h1>Derp</h1>'


def test_conditional():
    from textwrap import dedent
    import ninjadog
    string = dedent("""
    if name == 'sam'
        h1 hello #{ name }
    """)
    assert ninjadog.render(string, context={'name': 'sam'}) == '<h1>hello sam</h1>'

    string = dedent("""
    if person.name == 'sam'
        h1 hello #{ person.name }
    """)
    assert ninjadog.render(string, context={'person': {'name': 'sam'}}) == '<h1>hello sam</h1>'


def test_render_no_string_argument():
    from tempfile import NamedTemporaryFile
    import ninjadog
    string = 'h1 hello'
    with NamedTemporaryFile('w+') as tempfile:
        tempfile.write(string)
        tempfile.seek(0)
        assert ninjadog.render(file=tempfile.name) == ninjadog.render(string) == '<h1>hello</h1>'


def test_with_pug_with_jinja2():
    from textwrap import dedent
    from ninjadog import render
    string = dedent("""
    if person.name == "Bob"
        h1 Hello Bob
    else
        h1 My name is #{ person.name }

    p The persons's uppercase name is {{ person.get('name').upper() }}
    p The person's name is #{ person.name }

    if animal
        h1 This should not output
    else
        p animal value is false
    """).strip()

    context = {'person': {'name': 'Bob'}, 'animal': None}

    expected_output = dedent("""
    <h1>Hello Bob</h1>
    <p>The persons's uppercase name is BOB</p>
    <p>The person's name is Bob</p>
    <p>animal value is false</p>
    """).strip()

    actual_output = render(string, context=context, pretty=True, with_jinja=True).strip()

    assert expected_output == actual_output


def test_cli_string():
    from ninjadog.cli import main
    from ninjadog.utils import jsonify
    context = jsonify({'title': 'hello, world'})
    assert main(('string', 'h1= title', '-c', context)) == '<h1>hello, world</h1>'


def test_cli_file():
    from ninjadog.cli import main
    from ninjadog.utils import jsonify
    from tempfile import NamedTemporaryFile

    context = jsonify({'title': 'hello, world'})

    with NamedTemporaryFile('w+') as file:
        file.write('h1= title'); file.seek(0)
        assert main(('file', file.name, '-c', context)) == '<h1>hello, world</h1>'

