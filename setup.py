#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='pynliner',
      version='0.8.0',
      description='Python CSS-to-inline-styles conversion tool for HTML using'
                  ' BeautifulSoup and cssutils',
      author='Tanner Netterville',
      author_email='tannern@gmail.com',
      install_requires=[
          'BeautifulSoup4 >= 4.4.1',
          'cssutils >=0.9.7',
          'lxml',
      ],
      tests_require=[
          'mock'
      ],
      test_suite='tests',
      packages=['pynliner'],
      license='MIT',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Topic :: Text Processing :: Markup :: HTML',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5'
      ])
