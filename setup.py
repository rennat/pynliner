#!/usr/bin/env python

try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

setup(name='pynliner',
      version='0.4.0',
      description='Python CSS-to-inline-styles conversion tool for HTML using BeautifulSoup and cssutils',
      author='Tanner Netterville',
      author_email='tannern@gmail.com',
      packages=('pynliner',),
      requires=('BeautifulSoup(<4.0)',
                'cssutils(>=0.9.7)',
                ),
      provides=('pynliner',),
     )
