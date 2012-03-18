#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
from copy import copy
import hashlib
import json
import os.path
import subprocess as sp
import sys

from lxml import html


class Config(object):
    def __init__(self, path):
        cdata = open(path, 'r').read()
        self.data = json.loads(cdata)
        self.hashes = {}

    @property
    def srcdir(self):
        return self.data.get('srcdir', '.')

    @property
    def destdir(self):
        return self.data.get('destdir', '.')

    @property
    def static_root(self):
        return self.data.get('static_root', '')

    @property
    def js_bundles(self):
        return self.data.get('js', {})

    def js_files(self, key):
        return [os.path.join(self.srcdir, f) for f in self.js_paths(key)]

    def js_paths(self, key):
        return self.js_bundles.get(key, [])

    def _js_hash(self, key):
        if key in self.hashes:
            hsh = self.hashes[key]
        else:
            hsh = hash(self.js_files(key))
            self.hashes[key] = hsh
        return hsh

    def js_dest_url(self, key):
        return os.path.join(self.static_root, 'js', '{}-{}.js'.format(key, self._js_hash(key)))

    def js_dest_path(self, key):
        return os.path.join(self.static_root, 'js', '{}-{}.js'.format(key, self._js_hash(key)))


def compress(config):
    for prefix, files in config.js_bundles: 
        srcdir = config.srcdir
        destdir = config.destdir
        files = config.files

        inputs = []
        for f in files:
            inputs.extend(['--js', f])
        fn = '{}-{}.js'.format(prefix, hash(files))
        output = os.path.join(destdir, 'js', fn)
        sp.call( ['java', '-jar', 'support/closure-compiler.jar'] + inputs + ['--js_output_file', output])


def hash(files):
    print 'hashing'
    hasher = hashlib.md5()
    for f in files:
        hasher.update(open(f, 'rb').read())
    return hasher.hexdigest()[:8]


def dohtml(input_path, output_path, config, compressed=True):
    doc = html.fromstring(open(input_path, 'rb').read())
    for tag in doc.xpath('//script[@src]'):
        if tag.attrib['src'].startswith('compress:'):
            bundle = tag.attrib['src'].split(':')[1]

            if compressed:
                files = [config.js_dest_url(bundle)]
            else:
                # TODO: rename js_paths - maybe integrate with dest_url
                files = config.js_paths(bundle)

            for f in files:
                newtag = copy(tag)
                newtag.attrib['src'] = f
                newtag.text = ''
                tag.addprevious(newtag)
            tag.getparent().remove(tag)
    with open(output_path, 'w') as out:
        out.write('<!DOCTYPE html>\n')
        out.write(html.tostring(doc, pretty_print=True, include_meta_content_type=True, encoding='utf-8'))
    
    
def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
            description='Compress JS and CSS resources in a static site.')
    parser.add_argument('-d', '--development', action='store_true')
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    options = parser.parse_args()
    config = Config('compress.json')
    # compress(config)
    dohtml(options.input_file, options.output_file, config, not options.development)

if __name__ == '__main__':
    main()
