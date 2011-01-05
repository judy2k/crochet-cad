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

import logging
from math import cos, pi, sin

from crocad.util import instruction_txt, round_to_nearest_iter as snap


__all__ = ['ball']


log = logging.getLogger('crocad.ball')


def ball(rows):
    """ Generator for stitch-counts for a ball crochet pattern. """
    r = (rows + 1) / pi
    row_angle = pi / (rows + 1)
    log.debug('Ball - radius: %.2f, row-angle: %.2f rads', r, row_angle)
    for row in range(rows):
        row_rad = r * sin((row + 1) * row_angle)
        stitches = 2 * pi * row_rad
        log.debug('Circumference: %.2f', stitches)
        yield stitches


def print_instructions(stitches):
    """ Print plain text instructions for `stitches`. """
    prev = None
    for row, stitch_count in enumerate(stitches):
        print instruction_txt(row+1, prev, stitch_count)
        prev = stitch_count


def main(argv, global_options):
    """ Command entry-point for the donut pattern-generator. """
    import optparse

    op = optparse.OptionParser(
        '%prog [GLOBAL-OPTIONS] ball [--row-count=ROWS]',
        description="""
Generate a crochet pattern for a ball (sphere).
""".strip())
    op.add_option('-r', '--row-count', action='store', type='int',
        default=16, metavar='ROWS',
        help='the number of rows in the pattern. Defines the size'
        ' of the ball - the circumference is 2x this value. [%default]')
    command_opts, _ = op.parse_args(argv)
    stitches = ball(command_opts.row_count)
    stitches = snap(stitches, 1 if global_options.accurate else 6, 6)
    title = "Ball (%d rows)" % (command_opts.row_count,)
    print title
    print '=' * len(title)
    print_instructions(stitches)
