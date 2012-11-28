import os.path
import locale


def pass_through(to_translate):
    return to_translate


(lang, charset) = locale.getdefaultlocale()
if lang is None:
    translation = pass_through
else:
    import gettext
    for localedir in [
            "usr/local/share/locale",
            os.path.join(os.path.dirname(__file__), "locale"),
            ]:
        try:
            trans = gettext.translation("crochet-cad",
                localedir=localedir,
                languages=[lang])
            trans.install()
            translation = _   # NOQA
            break
        except IOError, ioe:
            pass
    else:
        translation = pass_through

def get_translation():
    return translation
