import locale


def pass_through(to_translate):
    return to_translate


(lang, charset) = locale.getdefaultlocale()
if lang is None or lang[:2] == "en":
    translation = pass_through
else:
    import gettext
    try:
        trans = gettext.translation("crochet-cad",
            localedir="/usr/local/share/locale",
            languages=[lang])
        trans.install()
        translation = _   # NOQA
    except IOError:
        translation = pass_through


def get_translation():
    return translation
