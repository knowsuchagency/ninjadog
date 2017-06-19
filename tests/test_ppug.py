#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ppug` package."""

import pytest


import ppug


def test_hello_world():
    assert ppug.render('h1 hello world') == '<h1>hello world</h1>'


def test_jinja2_template_syntax():
    assert ppug.render('h1 hello {{ name }}!') == '<h1>hello {{ name }}!</h1>'


def test_whitespace():
    from textwrap import dedent
    string = dedent("""
    p
        a(href='google.com') google
        |
        | to
        |
        a(href='github.com') github
    """)

    assert ppug.render(string) == '<p><a href="google.com">google</a> to <a href="github.com">github</a></p>'
