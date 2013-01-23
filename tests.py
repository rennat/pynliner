#!/usr/bin/env python

import unittest
import pynliner
import StringIO
import logging
import cssutils
from pynliner import Pynliner, fromString

class Basic(unittest.TestCase):

    def setUp(self):
        self.html = "<style>h1 { color:#ffcc00; }</style><h1>Hello World!</h1>"
        self.p = Pynliner().from_string(self.html)

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
        self.p = Pynliner().from_string(self.html).with_cssString(cssString)
        self.assertEqual(self.p.style_string, cssString + '\n')

        output = self.p.run()
        self.assertEqual(output, u'<h1 style="font-size: 2em; color: #fc0">Hello World!</h1>')


    def test_07_fromString(self):
        """Test 'fromString' complete"""
        output = pynliner.fromString(self.html)
        desired = u'<h1 style="color: #fc0">Hello World!</h1>'
        self.assertEqual(output, desired)

    def test_08_fromURL(self):
        """Test 'fromURL' constructor"""
        url = 'http://media.tannern.com/pynliner/test.html'
        p = Pynliner()
        p.from_url(url)
        self.assertEqual(p.root_url, 'http://media.tannern.com')
        self.assertEqual(p.relative_url, 'http://media.tannern.com/pynliner/')

        p._get_soup()

        p._get_external_styles()
        self.assertEqual(p.style_string, "p {color: #999}")

        p._get_internal_styles()
        self.assertEqual(p.style_string, "p {color: #999}\nh1 {color: #ffcc00;}\n")

        p._get_styles()

        output = p.run()
        desired = u"""<?xml version='1.0' encoding='utf-8'?>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>test</title>


</head>
<body>
<h1 style="color: #fc0">Hello World!</h1>
<p style="color: #999">Possim tincidunt putamus iriure eu nulla. Facer qui volutpat ut aliquam sequitur. Mutationem legere feugiat autem clari notare. Nulla typi augue suscipit lectores in.</p>
<p style="color: #999">Facilisis claritatem eum decima dignissim legentis. Nulla per legentis odio molestie quarta. Et velit typi claritas ipsum ullamcorper.</p>
</body>
</html>"""
        self.assertEqual(output, desired)

    def test_09_overloadedStyles(self):
        html = '<style>h1 { color: red; } #test { color: blue; }</style><h1 id="test">Hello world!</h1>'
        expected = '<h1 id="test" style="color: blue">Hello world!</h1>'
        output = Pynliner().from_string(html).run()
        self.assertEqual(expected, output)


class CommaSelector(unittest.TestCase):

    def setUp(self):
        self.html = """<style>.b1,.b2 { font-weight:bold; } .c {color: red}</style><span class="b1">Bold</span><span class="b2 c">Bold Red</span>"""
        self.p = Pynliner().from_string(self.html)

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
        self.assertEqual(self.p.style_string, u'.b1,.b2 { font-weight:bold; } .c {color: red}\n')
        self.assertEqual(unicode(self.p.soup), u'<span class="b1">Bold</span><span class="b2 c">Bold Red</span>')

    def test_04_apply_styles(self):
        """Test '_apply_styles' method"""
        self.p._get_soup()
        self.p._get_styles()
        self.p._apply_styles()
        self.assertEqual(unicode(self.p.soup), u'<span class="b1" style="font-weight: bold">Bold</span><span class="b2 c" style="color: red; font-weight: bold">Bold Red</span>')

    def test_05_run(self):
        """Test 'run' method"""
        output = self.p.run()
        self.assertEqual(output, u'<span class="b1" style="font-weight: bold">Bold</span><span class="b2 c" style="color: red; font-weight: bold">Bold Red</span>')

    def test_06_with_cssString(self):
        """Test 'with_cssString' method"""
        cssString = '.b1,.b2 {font-size: 2em;}'
        self.p = Pynliner().from_string(self.html).with_cssString(cssString)
        self.assertEqual(self.p.style_string, cssString + '\n')

        output = self.p.run()
        self.assertEqual(output, u'<span class="b1" style="font-size: 2em; font-weight: bold">Bold</span><span class="b2 c" style="color: red; font-size: 2em; font-weight: bold">Bold Red</span>')

    def test_07_fromString(self):
        """Test 'fromString' complete"""
        output = pynliner.fromString(self.html)
        desired = u'<span class="b1" style="font-weight: bold">Bold</span><span class="b2 c" style="color: red; font-weight: bold">Bold Red</span>'
        self.assertEqual(output, desired)

    def test_08_comma_whitespace(self):
        """Test excess whitespace in CSS"""
        html = '<style>h1,  h2   ,h3,\nh4{   color:    #000}  </style><h1>1</h1><h2>2</h2><h3>3</h3><h4>4</h4>'
        desired_output = '<h1 style="color: #000">1</h1><h2 style="color: #000">2</h2><h3 style="color: #000">3</h3><h4 style="color: #000">4</h4>'
        output = Pynliner().from_string(html).run()
        self.assertEqual(output, desired_output)

class Extended(unittest.TestCase):

    def test_overwrite(self):
        """Test overwrite inline styles"""
        html = '<style>h1 {color: #000;}</style><h1 style="color: #fff">Foo</h1>'
        desired_output = '<h1 style="color: #000; color: #fff">Foo</h1>'
        output = Pynliner().from_string(html).run()
        self.assertEqual(output, desired_output)

    def test_overwrite_comma(self):
        """Test overwrite inline styles"""
        html = '<style>h1,h2,h3 {color: #000;}</style><h1 style="color: #fff">Foo</h1><h3 style="color: #fff">Foo</h3>'
        desired_output = '<h1 style="color: #000; color: #fff">Foo</h1><h3 style="color: #000; color: #fff">Foo</h3>'
        output = Pynliner().from_string(html).run()
        self.assertEqual(output, desired_output)

class LogOptions(unittest.TestCase):
    def setUp(self):
        self.html = "<style>h1 { color:#ffcc00; }</style><h1>Hello World!</h1>"

    def test_no_log(self):
        self.p = Pynliner()
        self.assertEqual(self.p.log, None)
        self.assertEqual(cssutils.log.enabled, False)

    def test_custom_log(self):
        self.log = logging.getLogger('testlog')
        self.log.setLevel(logging.DEBUG)

        self.logstream = StringIO.StringIO()
        handler = logging.StreamHandler(self.logstream)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.log.addHandler(handler)

        self.p = Pynliner(self.log).from_string(self.html)

        self.p.run()
        log_contents = self.logstream.getvalue()
        self.assertIn("DEBUG", log_contents)

class BeautifulSoupBugs(unittest.TestCase):

    def test_double_doctype(self):
        self.html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">"""
        output = pynliner.fromString(self.html)
        self.assertNotIn("<!<!", output)

    def test_double_comment(self):
        self.html = """<!-- comment -->"""
        output = pynliner.fromString(self.html)
        self.assertNotIn("<!--<!--", output)

class ComplexSelectors(unittest.TestCase):

    def test_multiple_class_selector(self):
        html = """<h1 class="a b">Hello World!</h1>"""
        css = """h1.a.b { color: red; }"""
        expected = u"""<h1 class="a b" style="color: red">Hello World!</h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_combination_selector(self):
        html = """<h1 id="a" class="b">Hello World!</h1>"""
        css = """h1#a.b { color: red; }"""
        expected = u"""<h1 id="a" class="b" style="color: red">Hello World!</h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_descendant_selector(self):
        html = """<h1><span>Hello World!</span></h1>"""
        css = """h1 span { color: red; }"""
        expected = u"""<h1><span style="color: red">Hello World!</span></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_child_selector(self):
        html = """<h1><span>Hello World!</span></h1>"""
        css = """h1 > span { color: red; }"""
        expected = u"""<h1><span style="color: red">Hello World!</span></h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_adjacent_selector(self):
        html = """<h1>Hello World!</h1><h2>How are you?</h2>"""
        css = """h1 + h2 { color: red; }"""
        expected = u"""<h1>Hello World!</h1><h2 style="color: red">How are you?</h2>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)

    def test_attribute_selector(self):
        html = """<h1 title="foo">Hello World!</h1>"""
        css = """h1[title="foo"] { color: red; }"""
        expected = u"""<h1 title="foo" style="color: red">Hello World!</h1>"""
        output = Pynliner().from_string(html).with_cssString(css).run()
        self.assertEqual(output, expected)



class UnicodeTest(unittest.TestCase):
    """Tests for unicode."""

    def test_unicode_characters(self):
        self.assertEqual(fromString('<p>\xe4\xbd\xa0\xe5\xa5\xbd</p>'),
                                    u'<p>\u4f60\u597d</p>')

if __name__ == '__main__':
    unittest.main()
