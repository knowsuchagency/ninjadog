========
ninjadog
========


.. image:: https://img.shields.io/pypi/v/ninjadog.svg
        :target: https://pypi.python.org/pypi/ninjadog

.. image:: https://img.shields.io/travis/knowsuchagency/ninjadog.svg
        :target: https://travis-ci.org/knowsuchagency/ninjadog

.. image:: https://readthedocs.org/projects/ninjadog/badge/?version=latest
        :target: https://ninjadog.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/knowsuchagency/ninjadog/shield.svg
     :target: https://pyup.io/repos/github/knowsuchagency/ninjadog/
     :alt: Updates


`Pug`_ template (formerly `jade`_) support in Python


* Free software: MIT license
* Documentation: https://ninjadog.readthedocs.io.



Installation
------------

ninjadog requires Python 3.6, node-js, npm, and the pug-cli library

::

    brew install npm
    npm install -g pug-cli
    pip install ninjadog


For use with Pyramid, just add it to the configuration

.. code-block:: python

    config.include('pyramid_jinja2')
    config.include('ninjadog.ext.pyramid')


What?
-----

ninjadog leverages the `pug-cli`_ library, written in nodejs, to render
`pug`_ templates in Python. In addition, you can utilize `jinja2`_ syntax
within pug templates for even greater power!

.. code-block:: python

    from ninjadog import jinja2_renderer


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
    if happy.birthday == 'today'
        p it's time to celebrate!
        p {{ "Don't" if not stop_believing() }} stop believing
    """

    print(jinja2_renderer(template_string,
                          context=context,
                          pretty=True))

This will render

.. code-block:: html

    <h1>hello, world</h1>
    <p>it's time to celebrate!</p>
    <p>Don't stop believing</p>

How?
----

`Jinja2`_ basically behaves as a preprocessor to the pug template
engine. All data passed as the context will be processed by `jinja2`_.
Only that which can be serialized to json will be passed to the
pug template engine.


Why?
----

`Pug`_ templates are a very elegant and expressive way to write
html. It makes something akin to an exercise in corporal mortification
almost pleasant.

There exists a project, `pyjade`_ and a less-popular fork, `pypugjs`_,
that are pure-python implementations of the pug template engine,
but they haven't been maintained as well as one might like and and the bugs don't
lend themselves to fixes by mere-mortals like myself.

It made more sense to me to use the existing nodejs implementation,
and find a way to have it play nicely with Python.

ninjadog does this by spawning the `pug cli`_ as a subprocess.
This means that it can't be as fast as a native template engine
like `pyjade`_, but it will be more reliable as it's leveraging
the popular and well-maintained nodejs implementation.


.. _pug: https://pugjs.org/api/getting-started.html
.. _jade: https://naltatis.github.io/jade-syntax-docs/
.. _pyjade: https://github.com/syrusakbary/pyjade
.. _pypugjs: https://github.com/matannoam/pypugjs
.. _pug-cli: https://www.npmjs.com/package/pug-cli
.. _pug cli: https://www.npmjs.com/package/pug-cli
.. _jinja2: http://jinja.pocoo.org/
