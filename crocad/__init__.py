#!python
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
crocad - A Python library for generating crochet patterns.

This module provides `main`, which is the entry-point for command-line
execution of the module's functionality.
"""

import locale
import logging
import optparse
import sys


class NullHandler(logging.Handler):
    """
    A Handler that does nothing. Prevents error messages if crocad is used
    as a library and logging is not configured.
    """
    def emit(self, record):
        """Do nothing."""
        pass

logging.getLogger('crocad').addHandler(NullHandler())

from crocad import donut, ball, cone
from crocad.util import UnicodeOptionParser

__all__ = ['main']


LOG = logging.getLogger('crocad')


COMMAND_ALIASES = {}
for module in [ball, cone, donut]:
    for name in module.NAMES:
        COMMAND_ALIASES[name] = module


def find_command(command):
    """
    Attempts to find an imported module with the name `command`, and then
    obtains and returns that moule's `main` function.
    """
    command_module = COMMAND_ALIASES.get(command, None)
    if hasattr(command_module, 'main'):
        return getattr(command_module, 'main')
    else:
        raise Exception('Unknown command: %s' % command)


def main(argv=sys.argv[1:]):
    """ Crochet CAD's command-line entry-point. """
    global _

    locale.setlocale(locale.LC_ALL, '')
    print 'set locale to:', locale.setlocale(locale.LC_ALL)
    print 'current locale', locale.getlocale()

    from crocad import localization
    _ = localization.get_translation()

    opt_parser = UnicodeOptionParser("""%prog [-va] COMMAND [COMMAND-OPTIONS]

Help:
  %prog --help
  %prog COMMAND --help""",
description=_("""
Generate a crochet pattern for a geometric primitive, specified as COMMAND.
Supported commands are 'ball', 'donut', and 'cone'. For details of options for
a specific command, run '%prog COMMAND --help' with the name of the command.
""").strip()
)
    opt_parser.disable_interspersed_args()

    optgroup = optparse.OptionGroup(opt_parser, _('Global Options'),
    _('Global options must be provided before the name of the crochet-cad'
    ' COMMAND. They can be used with all crochet-cad commands.'))
    optgroup.add_option('-v', '--verbose', action='count', default=0,
        help=_('print out extra information - only really used for debugging.')
    )
    optgroup.add_option('-a', '--accurate', action='store_true',
        default=False, help=_('generate an exact pattern'
        ' which may not produce such an even end-product.'))
    optgroup.add_option('-i', '--inhuman', action='store_true',
        default=False,
        help=_('Instead of printing instructions, just print the row-counts,'
        ' one per line.'))
    opt_parser.add_option_group(optgroup)

    global_options, args = opt_parser.parse_args(argv)

    logging.basicConfig()
    # logging.getLogger().addHandler(logging.StreamHandler(sys.stderr))
    if global_options.verbose == 1:
        logging.getLogger().setLevel(logging.INFO)
    elif global_options.verbose > 1:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.WARNING)

    if args:
        command = args.pop(0)
        find_command(command)(args, global_options)
    else:
        opt_parser.error(_('No command was provided.'))


if __name__ == '__main__':
    main()
