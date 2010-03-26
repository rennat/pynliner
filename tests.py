#!/usr/bin/env python

import unittest
import pynliner

class Basic(unittest.TestCase):
    
    def setUp(self):
        self.html = "<style>h1 { color:#ffcc00; }</style><h1>Hello World!</h1>"
        self.p = pynliner.fromString(self.html)
    
    def test_01_fromString(self):
        """Test 'fromString' constructor"""
        self.assertEqual(self.p.source_string, self.html)
    
    def test_02_get_soup(self):
        """Test '_get_soup' method"""
        self.p._get_soup()
        self.assertEqual(unicode(self.p.soup), self.html)
    
    def test_03_get_styles(self):
        """Test '_get_styles' method"""
        self.p._get_soup()
        self.p._get_styles()
        self.assertEqual(self.p.style_string, u'h1 { color:#ffcc00; }\n')
        self.assertEqual(unicode(self.p.soup), u'<h1>Hello World!</h1>')
    
    def test_04_apply_styles(self):
        """Test '_apply_styles' method"""
        self.p._get_soup()
        self.p._get_styles()
        self.p._apply_styles()
        self.assertEqual(unicode(self.p.soup), u'<h1 style="color: #fc0">Hello World!</h1>')
    
    def test_05_run(self):
        """Test 'run' method"""
        output = self.p.run()
        self.assertEqual(output, u'<h1 style="color: #fc0">Hello World!</h1>')
    
    def test_06_with_cssString(self):
        """Test 'with_cssString' method"""
        cssString = 'h1 {font-size: 2em;}'
        self.p = pynliner.fromString(self.html).with_cssString(cssString)
        self.assertEqual(self.p.style_string, cssString + '\n')
        
        output = self.p.run()
        self.assertEqual(output, u'<h1 style="font-size: 2em; color: #fc0">Hello World!</h1>')
    

class Extended(unittest.TestCase):
    
    def test_overwrite(self):
        """Test overwrite inline styles"""
        html = '<style>h1 {color: #000;}</style><h1 style="color: #fff">Foo</h1>'
        desired_output = '<h1 style="color: #000; color: #fff">Foo</h1>'
        output = pynliner.fromString(html).run()
        self.assertEqual(output, desired_output)
    
    def test_


if __name__ == '__main__':
    unittest.main()
