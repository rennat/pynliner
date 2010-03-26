#!/usr/bin/env python

from distutils.core import setup

setup(name='pynliner',
      version='0.1.1',
      description='Python CSS-to-inline-styles conversion tool for HTML using BeautifulSoup and cssutils',
      author='Tanner Netterville',
      author_email='tannern@gmail.com',
      packages=('pynliner',),
      requires=('BeautifulSoup(>=3.0.3)',
                'cssutils(>=0.9.7)',
                ),
      provides=('pynliner',),
     )
