#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Pynliner : Convert CSS to inline styles

Python CSS-to-inline-styles conversion tool for HTML using BeautifulSoup and
cssutils

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

"""

import re

import cssutils
from bs4 import BeautifulSoup

from .soupselect import select

try:
    from urllib.parse import urljoin
    from urllib.request import urlopen
    unicode = str
except ImportError:
    from urlparse import urljoin
    from urllib2 import urlopen

__version__ = "0.8.0"


# this pattern may be too aggressive
HTML_ENTITY_PATTERN = re.compile(r'&(#([0-9]+|x[a-fA-F0-9]+)|[a-zA-Z][^\s;]+);')

SUBSTITUTION_FORMAT = '[pynlinerSubstitute:{0}]'
SUBSTITUTION_PATTERN = re.compile(r'\[pynlinerSubstitute:(\d+)\]')


class Pynliner(object):
    """Pynliner class"""

    soup = False
    style_string = False
    stylesheet = False
    output = False

    def __init__(self, log=None, allow_conditional_comments=False,
                 preserve_entities=True):
        self.log = log
        cssutils.log.enabled = False if log is None else True
        self.extra_style_strings = []
        self.allow_conditional_comments = allow_conditional_comments
        self.preserve_entities = preserve_entities
        self.root_url = None
        self.relative_url = None
        self._substitutions = None

    def from_url(self, url):
        """Gets remote HTML page for conversion

        Downloads HTML page from `url` as a string and passes it to the
        `from_string` method. Also sets `self.root_url` and `self.relative_url`
        for use in importing <link> elements.

        Returns self.

        >>> p = Pynliner()
        >>> p.from_url('http://somewebsite.com/file.html')
        <Pynliner object at 0x26ac70>
        """
        self.url = url
        self.relative_url = '/'.join(url.split('/')[:-1]) + '/'
        self.root_url = '/'.join(url.split('/')[:3])
        self.source_string = self._get_url(self.url)
        return self

    def from_string(self, string):
        """Generates a Pynliner object from the given HTML string.

        Returns self.

        >>> p = Pynliner()
        >>> p.from_string('<style>h1 {color:#ffcc00;}</style><h1>Hi</h1>')
        <Pynliner object at 0x26ac70>
        """
        self.source_string = string
        return self

    def with_cssString(self, css_string):
        """Adds external CSS to the Pynliner object. Can be "chained".

        Returns self.

        >>> html = "<h1>Hello World!</h1>"
        >>> css = "h1 { color:#ffcc00; }"
        >>> p = Pynliner()
        >>> p.from_string(html).with_cssString(css)
        <pynliner.Pynliner object at 0x2ca810>
        """
        self.extra_style_strings.append(css_string)
        return self

    def run(self):
        """Applies each step of the process if they have not already been
        performed.

        Returns Unicode output with applied styles.

        >>> html = "<style>h1 { color:#ffcc00; }</style><h1>Hello World!</h1>"
        >>> Pynliner().from_string(html).run()
        u'<h1 style="color: #fc0">Hello World!</h1>'
        """
        self._substitutions = []
        if self.preserve_entities:
            self._substitute_entities()
        if not self.soup:
            self._get_soup()
        if not self.stylesheet:
            self._get_styles()
        self._apply_styles()
        self._insert_media_rules()
        self._get_output()
        self._unsubstitute_output()
        return self.output

    def _store_substitute(self, value):
        """
        store a string and return it's substitute
        """
        index = len(self._substitutions)
        self._substitutions.append(value)
        return SUBSTITUTION_FORMAT.format(index)

    def _get_url(self, url):
        """Returns the response content from the given url
        """
        return urlopen(url).read().decode()

    def _substitute_entities(self):
        """
        Add HTML entities to the substitutions list and replace with
        placeholders in HTML source
        """
        self.source_string = re.sub(
            HTML_ENTITY_PATTERN,
            lambda m: self._store_substitute(m.group(0)),
            self.source_string
        )

    def _unsubstitute_output(self):
        """
        Put substitutions back into the output
        """
        self.output = re.sub(
            SUBSTITUTION_PATTERN,
            lambda m: self._substitutions[int(m.group(1))],
            self.output
        )

    def _get_soup(self):
        """Convert source string to BeautifulSoup object. Sets it to self.soup.

        If using mod_wgsi, use html5 parsing to prevent BeautifulSoup
        incompatibility.
        """
        # Check if mod_wsgi is running
        # - see http://code.google.com/p/modwsgi/wiki/TipsAndTricks
        try:
            from mod_wsgi import version
            self.soup = BeautifulSoup(self.source_string, "html5lib")
        except ImportError:
            self.soup = BeautifulSoup(self.source_string, "html.parser")

    def _get_styles(self):
        """Gets all CSS content from and removes all <link rel="stylesheet"> and
        <style> tags concatenating into one CSS string which is then parsed with
        cssutils and the resulting CSSStyleSheet object set to
        `self.stylesheet`.
        """
        self._get_external_styles()
        self._get_internal_styles()
        for style_string in self.extra_style_strings:
            self.style_string += style_string
        cssparser = cssutils.CSSParser(log=self.log)
        self.stylesheet = cssparser.parseString(self.style_string)

    def _get_external_styles(self):
        """Gets <link> element styles
        """
        if not self.style_string:
            self.style_string = u''
        else:
            self.style_string += u'\n'

        link_tags = self.soup.findAll('link', {'rel': 'stylesheet'})
        for tag in link_tags:
            url = tag['href']

            # Convert the relative URL to an absolute URL ready to pass to urllib
            base_url = self.relative_url or self.root_url
            url = urljoin(base_url, url)

            self.style_string += self._get_url(url)
            tag.extract()

    def _get_internal_styles(self):
        """Gets <style> element styles
        """
        if not self.style_string:
            self.style_string = u''
        else:
            self.style_string += u'\n'

        style_tags = self.soup.findAll('style')
        for tag in style_tags:
            self.style_string += u'\n'.join(tag.contents) + u'\n'
            tag.extract()

    def _insert_media_rules(self):
        """If there are any media rules, re-insert a style tag at the top and
        dump them all in.
        """
        rules = list(self.stylesheet.cssRules.rulesOfType(cssutils.css.CSSRule.MEDIA_RULE))
        if rules:
            style = BeautifulSoup(
                "<style>" + "\n".join(re.sub(r'\s+', ' ', x.cssText) for x in rules) +
                "</style>",
                "html.parser"
            )
            target = self.soup.body or self.soup
            target.insert(0, style)

    def _apply_styles(self):
        """Steps through CSS rules and applies each to all the proper elements
        as @style attributes prepending any current @style attributes.
        """
        rules = self.stylesheet.cssRules.rulesOfType(1)
        elem_prop_map = {}
        elem_style_map = {}
        # build up a property list for every styled element
        for rule in rules:
            for selector in rule.selectorList:
                for element in select(self.soup, selector.selectorText):
                    element_tuple = (element, id(element))
                    if element_tuple not in elem_prop_map:
                        elem_prop_map[element_tuple] = []
                    elem_prop_map[element_tuple].append({
                        'specificity': selector.specificity,
                        'props': rule.style.getProperties(),
                    })

        # build up another property list using selector specificity
        for elem_tuple, props in elem_prop_map.items():
            elem, elem_id = elem_tuple
            if elem_tuple not in elem_style_map:
                elem_style_map[elem_tuple] = cssutils.css.CSSStyleDeclaration()
            # ascending sort of prop_lists based on specificity
            props = sorted(props, key=lambda p: p['specificity'])
            # for each prop_list, apply to CSSStyleDeclaration
            for prop_list in map(lambda obj: obj['props'], props):
                for prop in prop_list:
                    elem_style_map[elem_tuple].removeProperty(prop.name)
                    elem_style_map[elem_tuple].setProperty(prop.name, prop.value)

        # apply rules to elements
        for elem_tuple, style_declaration in elem_style_map.items():
            elem, elem_id = elem_tuple
            if elem.has_attr('style'):
                elem['style'] = u'%s; %s' % (style_declaration.cssText.replace('\n', ' '), elem['style'])
            else:
                elem['style'] = style_declaration.cssText.replace('\n', ' ')

    def _get_output(self):
        """Generate Unicode string of `self.soup` and set it to `self.output`

        Returns self.output
        """
        self.output = unicode(self.soup)
        return self.output


def fromURL(url, **kwargs):
    """Shortcut Pynliner constructor. Equivalent to:

    >>> Pynliner().from_url(someURL).run()

    Returns processed HTML string.
    """
    return Pynliner(**kwargs).from_url(url).run()


def fromString(string, **kwargs):
    """Shortcut Pynliner constructor. Equivalent to:

    >>> Pynliner().from_string(someString).run()

    Returns processed HTML string.
    """
    return Pynliner(**kwargs).from_string(string).run()
