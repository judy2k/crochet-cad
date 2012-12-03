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
    def __init__(self, lc=None):
        self.tranlator = pass_through
        if lc is None:
            self.lang, self.charset = locale.getlocale()
        else:
            self.lang, self.charset = lc
        self._lookup_translations()

    def __call__(self, to_translate):
        """ Return translation for to_translate.

        Checks to ensure the locale hasn't changed  (and re-loads translations
        if it has) and returns suitable translation.
        """
        logging.debug('Comparing locales: %r, %r', (self.lang, self.charset), locale.getlocale())
        if (self.lang, self.charset) != locale.getlocale():
            self.lang, self.charset = locale.getlocale()
            self._lookup_translations()
        return self.translator(to_translate)

    def _lookup_translations(self):
        """ Load translations from disk.
        """
        LOG.debug("Looking up translations for %s", self.lang)
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
                    trans.install()
                    self.translator = _   # NOQA
                    break
                except IOError, ioe:
                    pass
            else:
                self.translator = pass_through

    def is_passthrough(self):
        """ Returns True if the current locale is not supported.
        """
        return self.translator == pass_through


translation = Translation()


def get_translation():
    """ Return a function for translating strings.
    """
    return translation
