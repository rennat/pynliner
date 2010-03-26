# pynliner

Python CSS-to-inline-styles conversion tool for HTML using BeautifulSoup and cssutils

- [PyPI](http://pypi.python.org/pypi/pynliner)
- [GitHub](http://github.com/rennat/pynliner)

## Installation

    $ pip install pynliner

## Examples

### Simplest usable example

    >>> import pynliner
    
    >>> html = "<style>h1 { color:#ffcc00; }</style><h1>Hello World!</h1>"
    
    >>> pynliner.fromString(html).run()
    u'<h1 style="color: #fc0">Hello World!</h1>'

### Separate HTML and CSS

    >>> import pynliner
    
    >>> html = "<h1>Hello World!</h1>"
    >>> css = "h1 { color:#ffcc00; }"
    
    >>> pynliner.fromString(html).with_cssString(css).run()
    u'<h1 style="color: #fc0">Hello World!</h1>'
