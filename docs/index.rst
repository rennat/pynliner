
pynliner
====================================

.. automodule :: pynliner

Project pages
-------------

- PyPI package page: http://pypi.python.org/pypi/pynliner
- github project page: http://github.com/rennat/pynliner
- this documentation: http://packages.python.org/pynliner

installation
------------

::

    $ easy_install pynliner

or

::

    $ pip install pynliner

example 
-------

>>> html = u'<style>h1 { color:#ffcc00; }</style><h1>Hello World!</h1>'
>>> output = pynliner.fromString(html)
u'<h1 style="color: #fc0">Hello World!</h1>'

functions
---------

.. autofunction :: pynliner.fromURL
.. autofunction :: pynliner.fromString

pynliner.Pynliner
-----------------

.. autoclass :: pynliner.Pynliner

methods
~~~~~~~

.. automethod :: pynliner.Pynliner.from_url
.. automethod :: pynliner.Pynliner.from_string
.. automethod :: pynliner.Pynliner.with_cssString
.. automethod :: pynliner.Pynliner.run