#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

install_requires = [
    'BeautifulSoup >=3.2.1,<4.0',
    'cssutils >=0.9.7',
]

tests_require = [
    'mock'
] + install_requires

setup(name='pynliner',
      version='0.5.0',
      description='Python CSS-to-inline-styles conversion tool for HTML using'
                  ' BeautifulSoup and cssutils',
      author='Tanner Netterville',
      author_email='tannern@gmail.com',
      install_requires=install_requires,
      tests_require=tests_require,
      test_suite='tests',
      packages=['pynliner'],
      provides=['pynliner'])
