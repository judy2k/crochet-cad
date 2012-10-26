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
crocad.cone - cone crochet pattern generation for crochet-cad.
"""


import logging

from crocad.util import round_to_nearest_iter as snap
from crocad.util import print_instructions_txt, print_row_counts


__all__ = ['cone']


LOG = logging.getLogger('crocad.cone')


def cone(rows, max_circ):
    """ Generator for stitch-counts for a cone crochet pattern. """
    min_circ = 6
    yield min_circ
    for row in range(rows-2):
        stitches = float(row)/(rows-2) * (max_circ-min_circ) + min_circ
        LOG.debug(_('Row %d, Stitches: %.2f'), row+1, stitches)
        yield stitches
    yield max_circ


def main(argv, global_options):
    """ Command entry-point for the cone pattern-generator. """
    import optparse

    opt_parser = optparse.OptionParser(
        _('%prog [GLOBAL-OPTIONS] cone [--row-count=ROWS]'),
        description="""
Generate a crochet pattern for a cone.
""".strip())
    opt_parser.add_option(_('-r'), _('--row-count'), action='store', type='int',
        default=16, metavar='ROWS',
        help=_('the number of rows in the pattern. Defines the height'
        ' of the cone [%default]'))
    opt_parser.add_option(_('-c'), _('--max-circumference'), action='store',
        type='int', default=60, metavar='STITCHES',
        help=_('the number of stitches at the base of the pattern. Defines the'
        ' circumference of the base of the cone [%default]'))
    command_opts, _ = opt_parser.parse_args(argv)
    stitches = cone(command_opts.row_count, command_opts.max_circumference)
    stitches = snap(stitches, 1 if global_options.accurate else 6, 6)
    if not global_options.inhuman:
        title = _("Cone (%d rows, %d max-circumference)") % (
                command_opts.row_count, command_opts.max_circumference)
        print_instructions_txt(title, stitches)
    else:
        print_row_counts(stitches)
