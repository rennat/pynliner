
pynliner
====================================

.. automodule :: pynliner

Project pages
-------------

- PyPI package page: http://pypi.python.org/pypi/pynliner
- github project page: http://github.com/rennat/pynliner
- this documentation: http://pythonhosted.org/pynliner

installation
------------

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


changelog
=========

0.7.1
-----

- attribute selector bug ( https://github.com/rennat/pynliner/issues/42 )

0.7.0
-----

- adopted better versioning practices (hence the 2 minor versions in one evening)
- fixed selector specificity sorting bug (via https://github.com/patricksurry/pynliner/commit/21cbadda157077f698a5f12891f6f021b584097f )
- fixed descendant operator logic (problem found by rogerhu https://github.com/rogerhu/pynliner/commit/07fb71ed3edffb9bdbc867577bc60f1ab1e2efd9 )

0.6.0
-----

- Python 3 support! (via agronholm https://github.com/rennat/pynliner/pull/41/commits/3ff3a7f3aae6e70d0a1e8919e27bf760f4ca79ae )
- Now uses Beautiful Soup 4 (thanks to agronholm)

0.5.0
-----

- started keeping track of changes here.
- improve CSS capabilities
- abandon old versions of BeautifulSoup (pre 3.2.1) in favor of full unicode support
