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

from __future__ import absolute_import

import logging
from crocad import localization

__all__ = ['instruction_txt', 'round_to_nearest',
           'round_to_nearest_iter', 'print_instructions_txt']

_ = localization.get_translation()

LOG = logging.getLogger('crocad.util')


def gcd_backport(num1, num2):    # NOQA
    """Returns the greatest common divisor of two numbers."""
    while num2 != 0:
        num1, num2 = num2, num1 % num2
    return num1


try:
    from fractions import gcd
except ImportError:
    gcd = gcd_backport


class Instruction(object):
    """ A bunch of 'stitch' in 'stitch' instructions. """
    def __init__(self, stitch='sc', stitch_count=1):
        self.stitch = stitch
        self.stitch_count = stitch_count

    @property
    def stitches(self):
        """ The number of stitches represented by this row. """
        return self.stitch_count

    stitches_into = stitches

    def merge(self, other):
        """ Attempt to merge two stitches of the same type.

        This method simply checks that the two instructions are of the exact
        same class, and that the stitch is the same. Each Instruction subclass
        has additional criteria as to whether the merge is allowed - this
        is delegated to the subclasses '_merge' method.

        This method returns False if the merge not possible.
        """
        if other.__class__ == self.__class__ and other.stitch == self.stitch:
            return self._merge(other) is not False
        else:
            return False

    def _merge(self, other):
        """ Provides subclass-specific merge validation and behaviour. This
        method should not be called directly.
        """
        self.stitch_count += other.stitch_count
        return True

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__
            and self.stitch == other.stitch
            and self.stitch_count == other.stitch_count
        )

    def __str__(self):
        """Plain-text representation of this instruction."""
        return _('%s in next %d') % (self.stitch, self.stitch_count)


class StitchTogetherInstruction(Instruction):
    """ A bunch of stXtog instructions. """
    def __init__(self, stitch='sc', stitch_count=1, together_count=2):
        super(StitchTogetherInstruction, self).__init__(stitch=stitch,
                stitch_count=stitch_count)
        self.together_count = together_count

    @property
    def stitches(self):
        """ The number of stitches represented by this row. """
        return self.stitch_count

    @property
    def stitches_into(self):
        """ The number of stitches required for the previous row. """
        return self.stitch_count * self.together_count

    def _merge(self, other):
        """ Provides subclass-specific merge validation and behaviour. This
        method should not be called directly.
        """
        if other.together_count == self.together_count:
            self.stitch_count += other.stitch_count
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

    def __eq__(self, other):
        return (
            super(StitchTogetherInstruction, self).__eq__(other)
            and self.together_count == other.together_count
        )


class MultipleStitchesInstruction(Instruction):
    """ A bunch of 'X st' in st commands. """
    def __init__(self, stitch=_('sc'), stitch_count=1, multiple_count=2):
        super(MultipleStitchesInstruction, self).__init__(stitch=stitch,
                stitch_count=stitch_count)
        self.multiple_count = multiple_count

    def _merge(self, other):
        """ Provides subclass-specific merge validation and behaviour. This
        method should not be called directly.
        """
        if other.multiple_count == self.multiple_count:
            self.stitch_count += other.stitch_count
            return True
        else:
            return False

    @property
    def stitches(self):
        """ The number of stitches represented by this row. """
        return self.stitch_count * self.multiple_count

    @property
    def stitches_into(self):
        """ The number of stitches required for the previous row. """
        return self.stitch_count

    def __str__(self):
        """Plain-text representation of this instruction."""
        inst = _('%d%s') % (self.multiple_count, self.stitch)
        if self.stitch_count > 1:
            inst += _(' in next %d') % self.stitch_count
        else:
            inst += _(' in next')
        return inst

    def __eq__(self, other):
        return (
            super(MultipleStitchesInstruction, self).__eq__(other)
            and self.multiple_count == other.multiple_count
        )


class InstructionGroup(Instruction):
    """
    Encapsulates a sequence of instructions which may or may not be repeated.
    """
    def __init__(self, instructions=None, repeats=1):
        self.stitch = None
        self._instructions = instructions or []
        self.repeats = repeats

    def _merge(self, other):
        """ Provides subclass-specific merge validation and behaviour. This
        method should not be called directly.
        """
        return False

    def append(self, inst):
        """ Append an instruction to this group.
        """
        last = self._instructions[-1] if self._instructions else None
        if last and last.merge(inst):
            return
        else:
            self._instructions.append(inst)

    @property
    def stitches(self):
        return sum(x.stitches() for x in self._instructions) * self.repeats

    @property
    def stitches_into(self):
        """ The number of stitches in the previous row required to crochet
        this InstructionGroup.
        """
        return sum(x.stitchesInto() for x in self._instructions) * self.repeats

    def __str__(self):
        if self.repeats == 1 or len(self._instructions) == 0:
            return ', '.join(str(x) for x in self._instructions)
        else:
            return '[' + ', '.join(str(x) for x in self._instructions)\
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
            for i in range(part_count):
                result += (_(', 2sc in next') if diff > 0 else _(', sc2tog'))
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
    return _('Row {row_number}: {instructions} ({stitch_count})').format(
        row_number=row,
        instructions=instruction(prev, count),
        stitch_count=int(count)
    )


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
