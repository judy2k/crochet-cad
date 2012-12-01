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
crocad.ball - sphere crochet pattern generation for crochet-cad.
"""

import logging
from crocad import localization
_ = localization.get_translation()
from math import pi, sin

from crocad.util import round_to_nearest_iter as snap
from crocad.util import print_instructions_txt, print_row_counts,\
    UnicodeOptionParser

__all__ = ['ball']
NAMES = ['ball', 'sphere']
LOG = logging.getLogger('crocad.ball')


def ball(rows):
    """ Generator for stitch-counts for a ball crochet pattern. """
    rad = (rows + 1) / pi
    row_angle = pi / (rows + 1)
    LOG.debug(_('Ball - radius: %.2f, row-angle: %.2f rads'), rad, row_angle)
    for row in range(rows):
        row_rad = rad * sin((row + 1) * row_angle)
        stitches = 2 * pi * row_rad
        LOG.debug(_('Circumference: %.2f'), stitches)
        yield stitches


def main(argv, global_options):
    """ Command entry-point for the ball pattern-generator. """
    _ = localization.get_translation()
    opt_parser = UnicodeOptionParser(
        '%prog [GLOBAL-OPTIONS] ball [--row-count=ROWS]',
        description=_("""
Generate a crochet pattern for a ball (sphere).
""").strip())
    opt_parser.add_option('-r', '--row-count', action='store',
        type='int', default=16, metavar='ROWS',
        help=_('the number of rows in the pattern. Defines the size'
        ' of the ball - the circumference is 2x this value. [%default]'))
    command_opts, __ = opt_parser.parse_args(argv)
    stitches = ball(command_opts.row_count)
    stitches = snap(stitches, 1 if global_options.accurate else 6, 6)

    if not global_options.inhuman:
        title = _("Ball (%d rows)") % (command_opts.row_count)
        print_instructions_txt(title, stitches)
    else:
        print_row_counts(stitches)
