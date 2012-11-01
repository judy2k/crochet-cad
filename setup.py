#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.command.install_data import install_data as INST

import glob, string, os

class inst_translations(INST):

    # Return triples for installations
    def __locales(self, rootdir):
        _globstr = '%s/*/*/*.mo' % rootdir
        paths = glob.glob(_globstr)
        _locales = []
        for p in paths:
            rp = string.split(p, '/', 2)
            (lang, loc, mo) = string.split(rp[2], '/')
            _locales.append( (lang, loc, mo) )
        return _locales

    def run(self):
        locales = self.__locales('crocad/locale')
        for (lang, loc, mo_file) in locales:
            lang_dir = os.path.join('share', 'locale', lang, loc)
            lang_file = os.path.join('crocad/locale', lang, loc, mo_file)
            self.data_files.append( (lang_dir, [lang_file]) )
        INST.run(self)

commands = {
    'install_data': inst_translations
}

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
    cmdclass=commands,
    data_files=[],
)
