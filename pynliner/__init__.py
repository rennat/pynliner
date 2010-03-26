#!/usr/bin/env python

"""Pynliner : Convert CSS to inline styles

Python CSS-to-inline-styles conversion tool for HTML using BeautifulSoup and cssutils

"""

import urllib2
import cssutils
from BeautifulSoup import BeautifulSoup
from soupselect import select

class Pynliner(object):
    """Pynliner class"""

    soup = False
    style_string = False
    stylesheet = False
    output = False
    
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
    
    def _get_url(self, url):
        """Returns the response content from the given url
        """
        return urllib2.urlopen(url).read()
    
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
        self._get_external_styles()
        self._get_internal_styles()
        self.stylesheet = cssutils.parseString(self.style_string)
    
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
            if url.startswith('http://'):
                pass
            elif url.startswith('/'):
                url = self.root_url + url
            else:
                url = self.relative_url + url
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

