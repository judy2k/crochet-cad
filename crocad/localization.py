# -*- coding: utf-8 -*-
#
# This file is part of Crochet CAD, a library and script for generating
# crochet patterns for simple 3D shapes.
#
# Copyright (C) 2010, 2011 Mark Smith <mark.smith@practicalpoetry.co.uk>
#
# Crochet CAD is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
crocad.localization - i18n support for crochet-cad.
"""

import os.path
import gettext
import locale
import logging


LOG = logging.getLogger('crocad.localization')


def pass_through(to_translate):
    """ A translation function for unsupported locales.
    """
    return to_translate


class Translation(object):
    """ A callable which provides translations for provided strings.
    """
    def __init__(self, current_locale=None):
        self.translator = pass_through
        if current_locale is None:
            self.lang, self.charset = locale.getlocale()
        else:
            self.lang, self.charset = current_locale
        self._lookup_translations()

    def __call__(self, to_translate):
        """ Return translation for to_translate.

        Checks to ensure the locale hasn't changed  (and re-loads translations
        if it has) and returns suitable translation.
        """
        if (self.lang, self.charset) != locale.getlocale():
            self.lang, self.charset = locale.getlocale()
            self._lookup_translations()
        return self.translator(to_translate)

    def _lookup_translations(self):
        """ Load translations from disk.
        """
        if self.lang is None:
            self.translator = pass_through
        else:
            for localedir in [
                "usr/local/share/locale",
                os.path.join(os.path.dirname(__file__), "locale"),
                ]:
                try:
                    trans = gettext.translation("crochet-cad",
                        localedir=localedir,
                        languages=[self.lang])
                    trans.install(unicode=True)
                    self.translator = _   # NOQA
                    break
                except IOError:
                    pass
            else:
                self.translator = pass_through

    def is_passthrough(self):
        """ Returns True if the current locale is not supported.
        """
        return self.translator == pass_through


TRANSLATION = Translation()


def get_translation():
    """ Return a function for translating strings.
    """
    return TRANSLATION
