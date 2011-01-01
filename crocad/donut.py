#!python
# -*- coding: utf-8 -*-

from math import cos, pi, sin

from crocad.util import instruction, round_to_nearest_iter as snap


__all__ = ['donut']


def donut(init_stitches, rows, initial_angle=0):
    """
    init_stitches - stitch-count of the inside row.
    rows - number of rows around the torus
    inital_angle - The angle (in radians) of the first row crocheted.
    """
    R = init_stitches / (2 * pi)
    r = rows / ( 2 * pi)
    row_angle = 2 * pi / rows
    for row in range(rows):
        rad = R + (r - (r * cos(row * row_angle + initial_angle)))
        stitch_count = int(round(rad * 2 * pi))
        yield stitch_count


def print_donut_text(stitches):
    prev = None
    for row, stitch_count in enumerate(stitches):
        # print stitch_count
        print 'Row %d: ' % (row+1),
        print instruction(prev, stitch_count)
        prev = stitch_count


def main(argv, global_options):
    """
    Command entry-point for the donut pattern-generator.
    """
    import optparse
    
    op = optparse.OptionParser()
    op.add_option('-i', '--inner-radius', action='store', type='int', default=18,
            metavar='STITCHES')
    op.add_option('-r', '--row-count', action='store', type='int', default=16,
            metavar='ROWS')
    command_opts, _ = op.parse_args(argv)
    print_donut_text(snap(donut(command_opts.inner_radius, command_opts.row_count), 6))


if __name__ == '__main__':
    main()