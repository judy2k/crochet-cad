#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from math import cos, pi, sin

from crocad.util import instruction_txt, round_to_nearest_iter as snap


__all__ = ['ball']


log = logging.getLogger('crocad.ball')


def ball(rows):
    r = (rows + 1) / pi
    row_angle = pi / (rows + 1)
    log.debug('Ball - radius: %.2f, row-angle: %.2f rads', r, row_angle)
    for row in range(rows):
        row_rad = r * sin((row + 1) * row_angle)
        stitches = 2 * pi * row_rad
        log.debug('Circumference: %.2f', stitches)
        yield stitches


def print_instructions(stitches):
    prev = None
    for row, stitch_count in enumerate(stitches):
        print instruction_txt(row+1, prev, stitch_count)
        prev = stitch_count


def main(argv, global_options):
    """
    Command entry-point for the donut pattern-generator.
    """
    import optparse

    op = optparse.OptionParser()
    op.add_option('-r', '--row-count', action='store', type='int', default=16,
            metavar='ROWS')
    command_opts, _ = op.parse_args(argv)
    stitches = ball(command_opts.row_count)
    stitches = snap(stitches, 1 if global_options.accurate else 6, 6)
    title = "Ball (%d rows)" % (command_opts.row_count,)
    print title
    print '=' * len(title)
    print_instructions(stitches)


if __name__ == '__main__':
    main()