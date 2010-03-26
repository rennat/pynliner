#!/usr/bin/env python

"""Pynliner : Convert CSS to inline styles

Python CSS-to-inline-styles conversion tool for HTML using BeautifulSoup and cssutils

"""

from BeautifulSoup import BeautifulSoup
from soupselect import select
import cssutils

class Pynliner(object):
    """Pynliner class"""

    soup = False
    style_string = False
    stylesheet = False
    output = False
    
    def from_url(self, url):
        """Gets remote HTML page for conversion
        
        Downloads HTML page from `url` as a string and passes it to the
        `from_string` method. Also sets `self.root_url` to be appended to all
        <link> tags urls when importing them.
        
        Returns self.
        
        >>> p = Pynliner()
        >>> p.from_url('http://somewebsite.com/file.html')
        <Pynliner object at 0x26ac70>
        """
        # TODO: implement url downloader
        pass
    
    def from_string(self, string):
        """Generates a Pynliner object from the given HTML string.
        
        Returns self.
        
        >>> p = Pynliner()
        >>> p.from_string('<style>h1 { color:#ffcc00; }</style><h1>Hello World!</h1>')
        <Pynliner object at 0x26ac70>
        """
        self.source_string = string
        return self
    
    def with_cssString(self, cssString):
        """Adds external CSS to the Pynliner object. Can be "chained".
        
        Returns self.
        
        >>> html = "<h1>Hello World!</h1>"
        >>> css = "h1 { color:#ffcc00; }"
        >>> p = Pynliner()
        >>> p.from_string(html).with_cssString(css)
        <pynliner.Pynliner object at 0x2ca810>
        """
        if not self.style_string:
            self.style_string = cssString + u'\n'
        else:
            self.style_string += cssString + u'\n'
        return self
    
    def run(self):
        """Applies each step of the process if they have not already been
        performed.
        
        Returns Unicode output with applied styles.
        
        >>> html = "<style>h1 { color:#ffcc00; }</style><h1>Hello World!</h1>"
        >>> Pynliner().from_string(html).run()
        u'<h1 style="color: #fc0">Hello World!</h1>'
        """
        if not self.soup:
            self._get_soup()
        if not self.stylesheet:
            self._get_styles()
        self._apply_styles()
        return self._get_output()
    
    def _get_soup(self):
        """Convert source string to BeautifulSoup object. Sets it to self.soup.
        """
        self.soup = BeautifulSoup(self.source_string)
    
    def _get_styles(self):
        """Gets all CSS content from and removes all <link rel="stylesheet"> and
        <style> tags concatenating into one CSS string which is then parsed with
        cssutils and the resulting CSSStyleSheet object set to
        `self.stylesheet`.
        """
        # TODO: get the link tags and import them
        
        style_tags = self.soup.findAll('style')
        
        if not self.style_string:
            self.style_string = u''
        
        for tag in style_tags:
            self.style_string += u'\n'.join(tag.contents) + u'\n'
            tag.extract()
        
        self.stylesheet = cssutils.parseString(self.style_string)
    
    def _apply_styles(self):
        """Steps through CSS rules and applies each to all the proper elements
        as @style attributes prepending any current @style attributes.
        """
        rules = self.stylesheet.cssRules.rulesOfType(1)
        ruleDict = {}
        for rule in rules:
            s = rule.selectorText
            if s in ruleDict:
                ruleDict[s] += '; ' + rule.style.cssText
            else:
                ruleDict[s] = rule.style.cssText
        
        for selector in ruleDict:
            elements = select(self.soup, selector)
            for el in elements:
                if el.has_key('style'):
                    el['style'] = u'%s; %s' % (ruleDict[selector], el['style'])
                else:
                    el['style'] = ruleDict[selector]
    
    def _get_output(self):
        """Generate Unicode string of `self.soup` and set it to `self.output`
        
        Returns self.output
        """
        self.output = unicode(self.soup)
        return self.output

def fromURL(url):
    """Shortcut Pynliner constructor. Equivelent to:
    
    >>> Pynliner().from_url(someURL).run()
    
    Returns processed HTML string.
    """
    return Pynliner().from_url(url).run()

def fromString(string):
    """Shortcut Pynliner constructor. Equivelent to:
    
    >>> Pynliner().from_string(someString).run()
    
    Returns processed HTML string.
    """
    return Pynliner().from_string(string).run()

