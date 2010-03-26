# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from soupselect import select
import cssutils

class Pynliner(object):
    soup = False
    style_string = False
    stylesheet = False
    output = False
    
    def from_url(self, url):
        # TODO: implement url downloader
        pass
    
    def from_string(self, string):
        self.source_string = string
        return self
    
    def with_cssString(self, cssString):
        if not self.style_string:
            self.style_string = cssString + u'\n'
        else:
            self.style_string += cssString + u'\n'
        return self
    
    def run(self):
        if not self.soup:
            self._get_soup()
        if not self.stylesheet:
            self._get_styles()
        self._apply_styles()
        return self._get_output()
    
    def _get_soup(self):
        self.soup = BeautifulSoup(self.source_string)
    
    def _get_styles(self):
        # TODO: get the link tags and import them
        
        style_tags = self.soup.findAll('style')
        
        if not self.style_string:
            self.style_string = u''
        
        for tag in style_tags:
            self.style_string += u'\n'.join(tag.contents) + u'\n'
            tag.extract()
        
        self.stylesheet = cssutils.parseString(self.style_string)
    
    def _apply_styles(self):
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
                    el['style'] += u'; ' + ruleDict[selector]
                else:
                    el['style'] = ruleDict[selector]
    
    def _get_output(self):
        self.output = unicode(self.soup)
        return self.output

def fromURL(url):
    p = Pynliner()
    p.from_url(url)
    return p

def fromString(string):
    p = Pynliner()
    p.from_string(string)
    return p

