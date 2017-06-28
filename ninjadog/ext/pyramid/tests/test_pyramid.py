from pyramid.config import Configurator
from pyramid.view import view_config
from webtest import TestApp as _TestApp


@view_config(route_name='home', renderer='./templates/child.pug')
def home(request):
    return {'title': 'title', 'subtitle': 'subtitle', 'content': 'This is a paragraph'}


def app_factory():
    config = Configurator()
    config.include('ninjadog')
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()


def test_rendering():
    testapp = _TestApp(app_factory())
    response = testapp.get('/', status=200)
    assert b'title' in response.body
    assert b'subtitle' in response.body
    assert b'This is a paragraph' in response.body
