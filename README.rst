====
ppug
====


.. image:: https://img.shields.io/pypi/v/ppug.svg
        :target: https://pypi.python.org/pypi/ppug

.. image:: https://img.shields.io/travis/knowsuchagency/ppug.svg
        :target: https://travis-ci.org/knowsuchagency/ppug

.. image:: https://readthedocs.org/projects/ppug/badge/?version=latest
        :target: https://ppug.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/knowsuchagency/ppug/shield.svg
     :target: https://pyup.io/repos/github/knowsuchagency/ppug/
     :alt: Updates


`Pug`_ template (formerly `jade`_) support in Python


* Free software: MIT license
* Documentation: https://ppug.readthedocs.io.



Installation
------------

::

    brew install npm
    npm install -g pug-cli
    pip install ppug


For use with Pyramid, just add it to the configuration

.. code-block:: python

    config.include('pyramid_jinja2')
    config.include('ppug.ext.pyramid')


What?
-----

ppug lets you render pug templates and combine them with jinja2
syntax.

.. code-block:: python

    from ppug import jinja2_renderer

    def stop_believing():
        return False

    context = {
        'stop_believing': stop_believing,
        'happy': {
            'birthday': 'today',
        }
    }

    template_string = """
    h1 hello, world
    if happy.birthday == today
        p it's time to celebrate!
        p {{ 'never' if not stop_believing() }} stop believing
    """

    print(jinja2_renderer(template_string,
                          context=context,
                          pretty=True))

This will render

.. code-block:: html

    <h1>hello, world</h1>
    <p>it's time to celebrate!</p>
    <p>never stop believing</p>

How?
----

Jinja2 basically behaves as a preprocessor to the pug template
engine and any data passed via the context argument that are able to be serialized
into json will then be passed to the pug template engine for rendering as well.


Why?
----

I think pug templates are a very elegant and expressive way to write
html. It makes something akin to an exercise in corporal mortification
almost pleasant.

There exists a project, `pyjade`_ and a less-popular fork, `pypugjs`_,
that are pure-python implementations of the pug template engine,
but they haven't been very well-maintained and and the bugs don't
lend themselves to fixes by mere-mortals like myself.

It made more sense to me to use the existing nodejs implementation,
and find a way to have it play nicely with Python.

ppug does this by spawning the pug cli as a subprocess and communicating
with it that way. Furthermore, if you want to use jinja2 template
syntax with your pug templates, any pug template that extends from another
will need to have that template rendered through jinja2 first, and since we
can't overwrite the original template, that means creating a temporary directory
and copies of all the relevant templates in that directory to be rendered prior
to passing it to the pug cli process.

All of that is to say that ppug is rather slow, but I'm willing
to accept pull-requests to make it faster or convenient caching
mechanisms.


.. _pug: https://pugjs.org/api/getting-started.html
.. _jade: https://naltatis.github.io/jade-syntax-docs/
.. _pyjade: https://github.com/syrusakbary/pyjade
.. _pypugjs: https://github.com/matannoam/pypugjs
