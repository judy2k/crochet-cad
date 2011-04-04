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
crocad.util - Shared functionality for crochet pattern generation.
"""

__all__ = ['instruction_txt', 'instruction_html', 'round_to_nearest',
        'round_to_nearest_iter', 'print_instructions_txt']

import logging

LOG = logging.getLogger('crocad.util')

try:
    from fractions import gcd
except ImportError:
    def gcd(num1, num2):
        """Returns the greatest common divisor of two numbers."""
        while num2 != 0:
            num1, num2 = num2 , num1 % num2
        return num1


class Instruction(object):
    """ A bunch of 'stitch' in 'stitch' instructions. """
    def __init__(self, stitch='sc', stitch_count=1):
        self.stitch = stitch
        self.stitch_count = stitch_count
        
    def stitches(self):
        """ The number of stitches represented by this row. """
        return self.stitch_count
    
    stitches_into = stitches
    
    def str(self):
        """Plain-text representation of this instruction."""
        return '%s in next %d' % (self.stitch, self.stitch_count)


class StitchTogetherInstruction(Instruction):
    """ A bunch of stXtog instructions. """
    def __init__(self, stitch='sc', stitch_count=1, together_count=2):
        super(StitchTogetherInstruction, self).__init__(stitch=stitch,
                stitch_count=stitch_count)
        self.together_count = together_count
    
    def stitches(self):
        """ The number of stitches represented by this row. """
        return self.stitch_count
    
    def stitches_into(self):
        """ The number of stitches required for the previous row. """
        return self.stitch_count * self.together_count
    
    def str(self):
        """Plain-text representation of this instruction."""
        inst = '%d%stog' % (self.together_count, self.stitch)
        if self.stitch_count > 1:
            inst += ' in next %d' % self.stitch_count
        return inst


class MultipleStitchesInstruction(Instruction):
    """ A bunch of 'X st' in st commands. """
    def __init__(self, stitch='sc', stitch_count=1, multiple_count=2):
        super(MultipleStitchesInstruction, self).__init__(stitch=stitch,
                stitch_count=stitch_count)
        self.multiple_count = multiple_count
    
    def stitches(self):
        """ The number of stitches represented by this row. """
        return self.stitch_count
    
    def stitches_into(self):
        """ The number of stitches required for the previous row. """
        return self.stitch_count / self.multiple_count
    
    def str(self):
        """Plain-text representation of this instruction."""
        inst = '%d%s in each' % (self.multiple_count, self.stitch)
        if self.stitch_count > 1:
            inst += ' in next %d' % self.stitch_count
        return inst


def _first_instruction(count):
    """ Returns an instruction for a first row. """
    if count <= 6:
        return 'Make a magic circle, 6sc into centre.'
    else:
        return 'ch %d, sc in each chain' % count


def instruction(prev, count):
    """
    Returns the instructions for a circular row with `count` stitches,
    crocheted on to a row of `prev` stitches.
    """
    prev = int(prev) if prev else None
    count = int(count) if count else None
    result = ''
    if prev is None:
        return _first_instruction(count)
    else:
        diff = count - prev
        if diff == 0:
            result += 'sc in each sc'
        else:
            repeats = gcd(count, prev)
            row_rem = 0
            if repeats == 1:
                repeats = abs(diff)
            prev = prev/repeats
            count, row_rem =  divmod(count, repeats)
            diff = count - prev
            scs = min(prev, count) - abs(diff)
            stcount, sc_rem = divmod(scs, abs(diff))
            if repeats:
                result += '*'
            part_count = int(abs(diff))
            LOG.debug('pc: %d, diff: %.4f', part_count, diff)
            for i in range(part_count):
                result += (', 2sc in next' if diff > 0 else ', 2sctog')
                LOG.debug('result: %s', result)
                if i < abs(diff) - 1:
                    if stcount:
                        result += ', %dsc' % stcount
                else:
                    if (stcount + sc_rem):
                        result += ', %dsc' % (stcount + sc_rem)
            if repeats:
                result += ', repeat from * %d times' % repeats
                
            if row_rem:
                result += ' %dsc ' % row_rem
    
    return result


def instruction_txt(row, prev, count):
    """ Produce a line of output in plain text format. """
    return 'Row %d: ' % row  + instruction(prev, count) + ' (%d)' % count


def instruction_html(row, prev, count):
    """ Produce a line of output in HTML format. """
    return '<div class="instruction">Row %d: ' % row + \
        instruction(prev, count) + \
        ' <em class="stitch-count">(%d)</em></div>' % count


def print_instructions_txt(title, stitches):
    """ Print plain text instructions for `stitches`. """
    print title
    print '=' * len(title)
    prev = None
    for row, stitch_count in enumerate(stitches):
        print instruction_txt(row+1, prev, stitch_count)
        prev = stitch_count


def round_to_nearest(i, margin=1, min_val=0):
    """ Return i rounded to the nearest margin. """
    val = ((i // margin) + round(float(i % margin) / margin)) * margin
    return max(min_val, val)


def round_to_nearest_iter(i, margin=1, min_val=0):
    """
    Return an iterable that produces each item in i, rounded to the
    nearest margin.
    """
    for val in i:
        yield round_to_nearest(val, margin, min_val)


def print_row_counts(stitches):
    """
    Simply prints out the each stitch-count on its own line, as an integer.
    """
    for stitch in stitches:
        print int(stitch)