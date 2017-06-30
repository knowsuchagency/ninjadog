from webtest import TestApp as _TestApp

import pytest


@pytest.fixture
def settings():
    from textwrap import dedent
    from configparser import ConfigParser

    config_ini = dedent("""
    [app:main]
    pyramid.reload_templates = true
    pug.static_only = false
    """)
    config = ConfigParser()
    config.read_string(config_ini)
    return dict(config.items('app:main'))


@pytest.fixture
def testapp(settings):
    from pyramid.config import Configurator
    with Configurator(settings=settings) as config:
        config.include('ninjadog')
        config.add_route('home', '/')
        config.add_view(
            lambda request: {'title': 'title', 'subtitle': 'subtitle', 'content': 'This is a paragraph'},
            route_name='home',
            renderer='./templates/child.pug',
        )
        app = config.make_wsgi_app()

        yield _TestApp(app)


def test_rendering(testapp):
    response = testapp.get('/', status=200)
    assert b'title' in response.body
    assert b'subtitle' in response.body
    assert b'This is a paragraph' in response.body
