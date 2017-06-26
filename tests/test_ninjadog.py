#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ninjadog` package."""

# TODO: test raises ValueError when pug cli can't be found and not passed explicitly to renderer

import pytest


def test_npm_installed():
    from subprocess import run
    assert run(('which', 'npm')).returncode == 0, 'npm must be installed'


def test_pug_cli_exists():
    from ninjadog.constants import PUG_CLI_PATH
    assert PUG_CLI_PATH.exists()


def test_hello_world():
    import ninjadog
    assert ninjadog.render('h1 hello world') == '<h1>hello world</h1>'


def test_jinja2_template_syntax():
    import ninjadog
    assert ninjadog.render('h1 hello {{ name }}!') == '<h1>hello {{ name }}!</h1>'


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


def test_jinja2_renderer():
    from ninjadog import jinja2_renderer
    assert jinja2_renderer('h1 hello {{ name }}', context={'name': 'fred'}) == '<h1>hello fred</h1>'


def test_render_no_string_argument():
    from tempfile import NamedTemporaryFile
    import ninjadog
    string = 'h1 hello'
    with NamedTemporaryFile('w+') as tempfile:
        tempfile.write(string)
        tempfile.seek(0)
        assert ninjadog.render(filepath=tempfile.name) == ninjadog.render(string) == '<h1>hello</h1>'


def test_jinja2_render_no_string_argument():
    from tempfile import NamedTemporaryFile
    import ninjadog
    string = 'h1 hello {{ name }}'
    context = {'name': 'ash'}
    with NamedTemporaryFile('w+') as tempfile:
        tempfile.write(string)
        tempfile.seek(0)
        assert ninjadog.jinja2_renderer(filepath=tempfile.name, context=context) \
               == ninjadog.jinja2_renderer(string, context=context) \
               == '<h1>hello ash</h1>'


def test_jinja2_syntax_with_pug_syntax():
    # TODO: get rid of this test
    from textwrap import dedent
    from ninjadog import jinja2_renderer
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

    actual_output = jinja2_renderer(string, context=context, pretty=True).strip()

    assert expected_output == actual_output


def test_with_jinja2():
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


def test_jinja2_renderer_raises_pending_deprecation():
    import warnings
    from ninjadog import jinja2_renderer
    warnings.simplefilter('error')
    with pytest.raises(DeprecationWarning):
        jinja2_renderer('h1 foo')


def test_jinja2_renderer_not_yet_deprecated():
    from configparser import ConfigParser
    from pathlib import Path

    config = ConfigParser()
    with Path(__file__).parent.parent.joinpath('setup.cfg').open() as fp:
        config.read_string(fp.read())


    version = config.get('bumpversion', 'current_version')
    _, minor, _ = (int(e) for e in version.split('.'))

    jinja2_exists = False

    try:
        from ninjadog.ext.jinja2 import jinja2_renderer
        jinja2_exists = True
    except ImportError:
        pass

    assert jinja2_exists and minor < 3, 'Time to deprecate jinja2_renderer'
