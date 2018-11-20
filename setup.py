#!/usr/bin/env python

from setuptools import setup

try:
    from multiply_forward_operators import __version__ as version
except ImportError:
    version = 'unknown'

setup(name='multiply-forward-operators',
      version=__version__,
      description='MULTIPLY Forward Operators',
      author='MULTIPLY Team',
      packages=['multiply_forward_operators']
      )
