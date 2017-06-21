#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ppug` package."""

import pytest

import ppug


def test_node_installed():
    from subprocess import run
    assert run(('which', 'node')).returncode == 0, 'Node must be installed'


def test_hello_world():
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
