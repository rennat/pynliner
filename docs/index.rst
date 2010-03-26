
pynliner
====================================

.. automodule :: pynliner

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