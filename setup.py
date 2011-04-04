#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='Crochet CAD',
    version='0.0.1dev',
    packages=['crocad',],
    scripts=['crochet-cad'],
    license='GNU General Public License',
    description=
    'A collection of utilities to aid in designing circular crochet patterns, such as Amigurumi.',
    long_description=''.join(open('README.rst').readlines()[2:]),
    
    author='Mark Smith',
    author_email='mark.smith@practicalpoetry.co.uk',
    url='https://github.com/bedmondmark/crochet-cad',
)