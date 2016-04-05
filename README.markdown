# pynliner

Python CSS-to-inline-styles conversion tool for HTML using BeautifulSoup and
cssutils

[![Build Status](https://travis-ci.org/rennat/pynliner.png?branch=master)](https://travis-ci.org/rennat/pynliner)

- [PyPI page](http://pypi.python.org/pypi/pynliner)
- [PyPI documentation](http://pythonhosted.org/pynliner)
- [GitHub project page](http://github.com/rennat/pynliner)

## License

Copyright (c) 2011-2016 Tanner Netterville

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

The generated output of this software shall not be used in a mass marketing
service.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO
EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
THE USE OR OTHER DEALINGS IN THE SOFTWARE.

## Notes

### Templating Languages

Because Pynliner uses BeautifulSoup to find the tags specified in the CSS it aggressively
converts to HTML. This means that **templating languages like Mako, Genshi, and Jinja**
will be pounded into valid HTML in the process of applying styles.
