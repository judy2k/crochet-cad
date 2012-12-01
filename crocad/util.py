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

import optparse
import logging
import localization
import sys

# from jinja2 import Template as T

_ = localization.get_translation()

LOG = logging.getLogger('crocad.util')


try:
    from fractions import gcd
except ImportError:
    def gcd(num1, num2):    # NOQA
        """Returns the greatest common divisor of two numbers."""
        while num2 != 0:
            num1, num2 = num2, num1 % num2
        return num1


class UnicodeOptionParser(optparse.OptionParser):
    def print_help(self, file=None):
        if file is None:
            file = sys.stdout
        file.write(
            self.format_help().decode('utf-8')
                .encode(file.encoding or 'utf-8', 'replace'))


class Instruction(object):
    """ A bunch of 'stitch' in 'stitch' instructions. """
    def __init__(self, stitch='sc', stitch_count=1):
        self.stitch = stitch
        self.stitch_count = stitch_count

    def stitches(self):
        """ The number of stitches represented by this row. """
        return self.stitch_count

    stitches_into = property(stitches)

    def merge(self, ob):
        if ob.__class__ == self.__class__ and ob.stitch == self.stitch:
            return self._merge(ob) is not False
        else:
            return False

    def _merge(self, ob):
        self.stitch_count += ob.stitch_count
        return True

    def __str__(self):
        """Plain-text representation of this instruction."""
        return _('%s in next %d') % (self.stitch, self.stitch_count)


class StitchTogetherInstruction(Instruction):
    """ A bunch of stXtog instructions. """
    def __init__(self, stitch='sc', stitch_count=1, together_count=2):
        super(StitchTogetherInstruction, self).__init__(stitch=stitch,
                stitch_count=stitch_count)
        self.together_count = together_count

    def stitches(self):
        """ The number of stitches represented by this row. """
        return self.stitch_count

    @property
    def stitches_into(self):
        """ The number of stitches required for the previous row. """
        return self.stitch_count * self.together_count

    def _merge(self, ob):
        if ob.together_count == self.together_count:
            self.stitch_count += ob.stitch_count
            return True
        else:
            return False

    def __str__(self):
        """Plain-text representation of this instruction."""
        inst = _('{together_count}{stitch}tog').format(
            together_count=self.together_count,
            stitch=self.stitch)
        if self.stitch_count > 1:
            inst += _(' in next %d') % self.stitch_count
        return inst


class MultipleStitchesInstruction(Instruction):
    """ A bunch of 'X st' in st commands. """
    def __init__(self, stitch=_('sc'), stitch_count=1, multiple_count=2):
        super(MultipleStitchesInstruction, self).__init__(stitch=stitch,
                stitch_count=stitch_count)
        self.multiple_count = multiple_count

    def _merge(self, ob):
        if ob.multiple_count == self.multiple_count:
            self.stitch_count += ob.stitch_count
            return True
        else:
            return False

    def stitches(self):
        """ The number of stitches represented by this row. """
        return self.stitch_count

    @property
    def stitches_into(self):
        """ The number of stitches required for the previous row. """
        return self.stitch_count / self.multiple_count

    def __str__(self):
        """Plain-text representation of this instruction."""
        inst = _('%d%s in each') % (self.multiple_count, self.stitch)
        if self.stitch_count > 1:
            inst += _(' in next %d') % self.stitch_count
        return inst


class InstructionGroup(Instruction):
    def __init__ (self, instructions=None, repeats=1):
        self._instructions = instructions or []
        self.repeats = repeats

    def _merge(self, ob):
        return False

    def append(self, instruction):
        last = self._instructions[-1] if self._instructions else None
        if last and last.merge(instruction):
            return
        else:
            self._instructions.append(instruction)

    def stitches(self):
        sum(x.stitches() for x in self._instructions) * self.repeats

    @property
    def stitches_into(self):
        sum(x.stitchesInto() for x in self._instructions) * self.repeats

    def __str__(self):
        if self.repeats == 1:
            ', '.join(x.toString() for x in self._instructions)
        else:
            return '[' + ', '.join(x.toString() for x in self._instructions)\
                   + ". Repeat {repeats} times.]".format(repeats=self.repeats)

def _first_instruction(count):
    """ Returns an instruction for a first row. """
    if count <= 6:
        return _('Make a magic circle, 6sc into centre.')
    else:
        return _('ch %d, sc in each chain') % count


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
            result += _('sc in each sc')
        else:
            repeats = gcd(count, prev)
            row_rem = 0
            if repeats == 1:
                repeats = abs(diff)
            prev = prev / repeats
            count, row_rem = divmod(count, repeats)
            diff = count - prev
            scs = min(prev, count) - abs(diff)
            stcount, sc_rem = divmod(scs, abs(diff))
            if repeats > 1:
                result += '*'
            part_count = int(abs(diff))
            LOG.debug(_('pc: %d, diff: %.4f'), part_count, diff)
            for i in range(part_count):
                result += (_(', 2sc in next') if diff > 0 else _(', sc2tog'))
                LOG.debug(_('result: %s'), result)
                if i < abs(diff) - 1:
                    if stcount:
                        result += _(', %dsc') % stcount
                else:
                    if (stcount + sc_rem):
                        result += _(', %dsc') % (stcount + sc_rem)
            if repeats > 1:
                result += _(', repeat from * %d times') % repeats

            if row_rem:
                result += _(' %dsc ') % row_rem

    return result


def instruction_txt(row, prev, count):
    """ Produce a line of output in plain text format. """
    return _('Row %d: ') % row + instruction(prev, count) + _(' (%d)') % count


def instruction_html(row, prev, count):
    """ Produce a line of output in HTML format. """
    return _('<div class="instruction">Row %d: ') % row + \
        instruction(prev, count) + \
        _(' <em class="stitch-count">(%d)</em></div>') % count


def print_instructions_txt(title, stitches):
    """ Print plain text instructions for `stitches`. """
    print title
    print '=' * len(title)
    prev = None
    for row, stitch_count in enumerate(stitches):
        print instruction_txt(row + 1, prev, stitch_count)
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
