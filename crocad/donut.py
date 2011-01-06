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
crocad.ball - donut crochet pattern generation for crochet-cad.
"""

import logging
from math import pi, cos

from crocad.util import instruction_txt, round_to_nearest_iter as snap
from crocad.util import print_instructions_txt


__all__ = ['donut']


log = logging.getLogger('crocad.donut')


def donut(init_stitches, rows, initial_angle=0):
    """
    Generator for stitch-counts for a donut crochet pattern.
    
    init_stitches - stitch-count of the inside row.
    rows - number of rows around the torus
    inital_angle - The angle (in radians) of the first row crocheted.
    """
    R = init_stitches / (2 * pi)
    r = rows / ( 2 * pi)
    row_angle = 2 * pi / rows
    for row in range(rows):
        rad = R + (r - (r * cos(row * row_angle + initial_angle)))
        circ = rad * 2 * pi
        # stitch_count = int(round(circ))
        yield circ # stitch_count


def main(argv, global_options):
    """
    Command entry-point for the donut pattern-generator.
    """
    import optparse
    
    op = optparse.OptionParser(
        '%prog [GLOBAL-OPTIONS] '
        'donut [--inner-radius=STITCHES] [--row-count=ROWS]',
        description="""
Generate a pattern for a donut (torus). The pattern
starts off with a row in the centre (the donut hole) and crocheted up
and around.""".strip())
    op.add_option('-i', '--inner-radius', action='store', type='int',
        default=18, metavar='STITCHES',
        help='the circumference of the donut hole, in stitches [%default]')
    op.add_option('-r', '--row-count', action='store', type='int', default=16,
        metavar='ROWS',
        help="the number of rows in the pattern - defines the 'thickness'"
            " of the donut [%default]")
    command_opts, _ = op.parse_args(argv)
    stitches = donut(command_opts.inner_radius, command_opts.row_count)
    stitches = snap(stitches, 1 if global_options.accurate else 6)
    title = "Donut (inner-radius: %d, %d rows)" % (command_opts.inner_radius,
            command_opts.row_count)
    print title
    print '=' * len(title)
    print_instructions_txt(stitches)