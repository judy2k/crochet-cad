#!/usr/bin/env python
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

import unittest

class UtilTestCaseMixin(object):
    @property
    def _util(self):
        import crocad.util
        return crocad.util




class StitchTestCaseMixin(object):
    @property
    def _Instruction(self):
        import crocad.util
        return crocad.util.Instruction

    @property
    def _MultipleStitchesInstruction(self):
        import crocad.util
        return crocad.util.MultipleStitchesInstruction

    @property
    def _StitchTogetherInstruction(self):
        import crocad.util
        return crocad.util.StitchTogetherInstruction

    @property
    def _InstructionGroup(self):
        import crocad.util
        return crocad.util.InstructionGroup


class TestUtil(unittest.TestCase, UtilTestCaseMixin):
    @property
    def _rtn(self):
        return self._util.round_to_nearest

    @property
    def _rtni(self):
        return self._util.round_to_nearest_iter

    @property
    def _inst(self):
        return self._util.instruction

    def test_round_to_nearest(self):
        """ round_to_nearest produces the correct output
        """
        self.assertEquals(21, self._rtn(20.51))
        self.assertEquals(21, self._rtn(20.5))
        self.assertEquals(20, self._rtn(20.49))

        self.assertEquals(18, self._rtn(20, 6))
        self.assertEquals(18, self._rtn(19.99, 6))
        self.assertEquals(24, self._rtn(21, 6))
        self.assertEquals(24, self._rtn(22, 6))

        self.assertEquals(6, self._rtn(0, 2, 6))
        self.assertEquals(12, self._rtn(12, 2, 6))

    def test_round_to_nearest_iter(self):
        """ round_to_nearest_iter produces the correct output
        """
        self.assertEquals([4,4,4,4,4,6,6,8,8,10],
            list(self._rtni(range(10), 2, 4)))

    def test_instruction(self):
        """ instruction produces the correct output
        """
        self.assertEqual('*, 2sc in next, 10sc, repeat from * 3 times 1sc ', self._inst(34.0, 37.0))
        self.assertEqual('*, 2sc in next, 10sc, repeat from * 3 times 1sc ', self._inst(34, 37))
        self.assertEqual(', 2sc in next, 10sc', self._inst(11, 12))
        self.assertEqual(', sc2tog, 10sc', self._inst(12, 11))
        self.assertEqual('sc in each sc', self._inst(12, 12))


class TestInstruction(unittest.TestCase, StitchTestCaseMixin):
    def test_init(self):
        """ Instructions are initialised correctly
        """
        i = self._Instruction()
        self.assertEqual('sc', i.stitch)
        self.assertEqual(1, i.stitch_count)
        self.assertEqual(1, i.stitches_into)

    def test_merge(self):
        """ Instructions can be merged into other Instructions
        """
        # Two instructions that are the same should merge:
        i = self._Instruction()
        i.merge(self._Instruction())
        self.assertEqual(i.stitch_count, 2)

    def test_merge_cannot_merge_non_Instruction(self):
        """ Only Instructions can be merged into other Instructions (not subclasses)
        """
        i = self._Instruction()
        not_i = self._MultipleStitchesInstruction()
        self.assertFalse(i.merge(not_i))
        not_i = self._StitchTogetherInstruction()
        self.assertFalse(i.merge(not_i))
        not_i = self._InstructionGroup()
        self.assertFalse(i.merge(not_i))

        self.assertTrue(False)


def suite():
    ts = unittest.TestSuite()
    return ts


if __name__ == '__main__':
    unittest.main()