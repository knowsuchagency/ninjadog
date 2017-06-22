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


Pug template support in Python


* Free software: MIT license
* Documentation: https://ppug.readthedocs.io.


Features
--------

* Render `.pug templates <https://pugjs.org/api/getting-started.html>`_ (formerly `jade <https://naltatis.github.io/jade-syntax-docs/>`_)

Usage
-----

You can use the render function to simply render a block of pug-formatted text to html

.. code-block:: python

    from ppug import render

    string = 'h1 hello, world'

    print(render(string)) # -> <h1>hello, world</h1>

    # or if you have a template on the filesystem

    render(filename='mytemplate.pug') # -> whatever is in your template

    # if you have data that you want rendered within the template, pass it
    # as the context

    render('h1= title', context={'title': 'hello, pug'}) # -> <h1>hello, pug</h1>


You can also have jinja2 and pug template syntax in the same template.

They say a picture is worth a thousand words, so while the following isn't a picture
it's a hopefully illuminating example taken straight from the test suite.

Essentially, jinja2 will behave as a pre-processor the the pug template engine.
Only those parts of the context that are json-serializable will be passed to it.

Thus, in the following example, ``person.name`` works in the pug template because Python was able to serialize it into
json and pass it to the pug template engine as a json object.

Similarly, you could also have ``#{ person.name }``
in the template, but not ``#{ Bob.age }``
because it is not able to be serialized automatially into json
and will never be passed to the pug template engine.

.. code-block:: python

    def test_jinja2_syntax_and_jade_syntax():
        from textwrap import dedent

        from ppug import jinja2_renderer

        string = dedent("""
        if person.name == "Bob"
            h1 Hello Bob
            h1 Bob's age is {{ Bob.age }}
        else
            h1 My name is #{ person.name }

        p The persons's uppercase name is {{ person.get('name').upper() }}
        p The person's name is #{ person.name }

        if animal
            h1 This should not output
        else
            p animal value is false
        """).strip()

        class Bob:
            """This class is not itself json-serializable"""
            age = 23

        context = {'person': {'name': 'Bob'}, 'animal': None, 'Bob': Bob}

        expected_output = dedent("""
        <h1>Hello Bob</h1>
        <h1>Bob's age is 23</h1>
        <p>The persons's uppercase name is BOB</p>
        <p>The person's name is Bob</p>
        <p>animal value is false</p>
        """).strip()

        actual_output = jinja2_renderer(string, context=context, pretty=True).strip()

        assert expected_output == actual_output

To use pug templates with Pyramid, simply include them with your configuration
after ``pyramid-jinja2``.

This will allow you to use jinja2 template syntax within pug templates.

.. code-block:: python

    config = Configurator()
    config.include('pyramid_jinja2')
    config.include('ppug.ext.pyramid')


Installation
------------

Please note that npm must be installed for this package to work.

    brew install npm

    npm install -g pug-cli

    pip install ppug


Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

