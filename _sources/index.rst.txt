ninjadog: pug + jinj2 == ❤️
===========================

.. image:: yodawg.jpg

.. include:: ../README.rst

Command Line Interface
----------------------

.. include:: ../ninjadog/cli.py
    :start-after: """
    :end-before: """
    :literal:

Pyramid
-------

You can avoid having to render each template anew with every HTTP request.
In your Pyramid configuration, you can have ninjadog cache templates by setting
the ``ninjadog.cache`` option to true like so

.. code-block:: ini

    [app:main]
    ninjadog.cache = true


.. code-block:: python

    Configurator(settings={'ninjadog.cache': True})
    # ...

... however you like to configure your app.


While this will make each page load much faster after the first visit,
**IT ALSO MEANS YOU CANNOT HAVE ANY MUTABLE STATE IN YOUR TEMPLATE**
as the template itself won't render any differently after the first time it's rendered.

It may be best to prototype by using ninjadog as normal - mutable state, conditionals, mixins... whatever -
but to set the aformentioned option to true and move any logic dealing with mutable state into
javascript for production. The choice yours.


API Documentation
-----------------

.. include:: modules.rst
    :start-line: 2

Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
