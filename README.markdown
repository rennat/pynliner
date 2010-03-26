# pynliner

Python CSS-to-inline-styles conversion tool for HTML using BeautifulSoup and cssutils

-PyPI: http://pypi.python.org/pypi/pynliner/0.1.0a
-GitHub: http://github.com/rennat/pynliner

## Simple Example

Install with `pip install pynliner`

    >>> import pynliner
    
    >>> html = "<style>h1 { color:#ffcc00; }</style><h1>Hello World!</h1>"
    >>> output = pynliner.fromString(html).run()
    
    >>> output
    u'<h1 style="color: #fc0">Hello World!</h1>'
