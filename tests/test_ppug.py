#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ppug` package."""

import pytest

import ppug


def test_npm_installed():
    from subprocess import run
    assert run(('which', 'npm')).returncode == 0, 'npm must be installed'


def test_pug_cli_exists():
    from ppug.constants import PUG_CLI_PATH
    assert PUG_CLI_PATH.exists()


def test_hello_world():
    import ppug
    assert ppug.render('h1 hello world') == '<h1>hello world</h1>'


def test_jinja2_template_syntax():
    assert ppug.render('h1 hello {{ name }}!') == '<h1>hello {{ name }}!</h1>'


def test_context():
    context = {'name': 'Derp'}
    assert ppug.render('h1 hello #{ name }', context=context) == '<h1>hello Derp</h1>'
    assert ppug.render("h1= name", context=context) == '<h1>Derp</h1>'


def test_conditional():
    from textwrap import dedent
    string = dedent("""
    if name == 'sam'
        h1 hello #{ name }
    """)
    assert ppug.render(string, context={'name': 'sam'}) == '<h1>hello sam</h1>'

    string = dedent("""
    if person.name == 'sam'
        h1 hello #{ person.name }
    """)
    assert ppug.render(string, context={'person': {'name': 'sam'}}) == '<h1>hello sam</h1>'


def test_jinja2_renderer():
    from ppug import jinja2_renderer
    assert jinja2_renderer('h1 hello {{ name }}', context={'name': 'fred'}) == '<h1>hello fred</h1>'


def test_render_no_string_argument():
    from tempfile import NamedTemporaryFile
    string = 'h1 hello'
    with NamedTemporaryFile('w+') as tempfile:
        tempfile.write(string)
        tempfile.seek(0)
        assert ppug.render(filepath=tempfile.name) == ppug.render(string) == '<h1>hello</h1>'


def test_jinja2_render_no_string_argument():
    from tempfile import NamedTemporaryFile
    string = 'h1 hello {{ name }}'
    context = {'name': 'ash'}
    with NamedTemporaryFile('w+') as tempfile:
        tempfile.write(string)
        tempfile.seek(0)
        assert ppug.jinja2_renderer(filepath=tempfile.name, context=context) \
               == ppug.jinja2_renderer(string, context=context) \
               == '<h1>hello ash</h1>'


def test_jinja2_syntax_with_pug_syntax():
    from textwrap import dedent
    from ppug import jinja2_renderer
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
