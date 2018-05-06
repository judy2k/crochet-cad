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


import locale
import unittest

# Currently only English output is tested:
locale.setlocale(locale.LC_ALL, 'en_GB.utf-8')

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
        self.assertEqual(21, self._rtn(20.51))
        self.assertEqual(21, self._rtn(20.5))
        self.assertEqual(20, self._rtn(20.49))

        self.assertEqual(18, self._rtn(20, 6))
        self.assertEqual(18, self._rtn(19.99, 6))
        self.assertEqual(24, self._rtn(21, 6))
        self.assertEqual(24, self._rtn(22, 6))

        self.assertEqual(6, self._rtn(0, 2, 6))
        self.assertEqual(12, self._rtn(12, 2, 6))

    def test_round_to_nearest_iter(self):
        """ round_to_nearest_iter produces the correct output
        """
        self.assertEqual([4,4,4,4,4,6,6,8,8,10],
            list(self._rtni(list(range(10)), 2, 4)))

    def test_instruction(self):
        """ instruction produces the correct output
        """
        locale.setlocale(locale.LC_ALL, 'en_GB.utf-8')
        self.assertEqual('*, 2sc in next, 10sc, repeat from * 3 times 1sc ', self._inst(34.0, 37.0))
        self.assertEqual('*, 2sc in next, 10sc, repeat from * 3 times 1sc ', self._inst(34, 37))
        self.assertEqual('*, 2sc in next, 7sc, 2sc in next, 8sc, repeat from * 2 times', self._inst(34, 38))
        self.assertEqual(', 2sc in next, 10sc', self._inst(11, 12))
        self.assertEqual(', sc2tog, 10sc', self._inst(12, 11))
        self.assertEqual('sc in each sc', self._inst(12, 12))
        self.assertEqual('ch 12, sc in each chain', self._inst(None, 12))

    def test_gcd_backport(self):
        gcd = self._util.gcd_backport

        self.assertEqual(10, gcd(10,10))
        self.assertEqual(5, gcd(5,10))
        self.assertEqual(5, gcd(10,5))
        self.assertEqual(2, gcd(4,10))
        self.assertEqual(1, gcd(4,11))

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

    def test_merge_can_only_merge_Instruction(self):
        """ Only Instructions can be merged into other Instructions (not subclasses)
        """
        i = self._Instruction()
        not_i = self._MultipleStitchesInstruction()
        self.assertFalse(i.merge(not_i))
        not_i = self._StitchTogetherInstruction()
        self.assertFalse(i.merge(not_i))
        not_i = self._InstructionGroup()
        self.assertFalse(i.merge(not_i))

    def test_str(self):
        i = self._Instruction()
        self.assertEqual("sc in next 1", str(i))

        i = self._Instruction(stitch_count=2)
        self.assertEqual("sc in next 2", str(i))

    def test_eq(self):
        i1 = self._Instruction()
        i2 = self._Instruction()
        self.assertEqual(i1, i2)

        i2 = self._Instruction(stitch_count=2)
        self.assertNotEqual(i1, i2)


class TestStitchTogetherInstruction(unittest.TestCase, StitchTestCaseMixin):
    def test_init(self):
        """ StitchTogetherInstructions are initialised correctly.
        """
        i = self._StitchTogetherInstruction()
        self.assertEqual('sc', i.stitch)
        self.assertEqual(1, i.stitch_count)
        self.assertEqual(2, i.stitches_into)
        self.assertEqual(1, i.stitches)

    def test_merge(self):
        """ StitchTogetherInstructions can be successfully merged
        """
        i = self._StitchTogetherInstruction()
        i.merge(self._StitchTogetherInstruction())
        self.assertEqual(i.stitch_count, 2)

        # Can't merge two stitch-togethers with different together_counts.
        self.assertFalse(i.merge(self._StitchTogetherInstruction(together_count=3)))

    def test_merge_can_only_merge_StitchTogetherInstruction(self):
        """ Only StitchTogetherInstructions can be merged into other StitchTogetherInstructions
        """
        i = self._StitchTogetherInstruction()
        not_i = self._Instruction()
        self.assertFalse(i.merge(not_i))
        not_i = self._MultipleStitchesInstruction()
        self.assertFalse(i.merge(not_i))
        not_i = self._InstructionGroup()
        self.assertFalse(i.merge(not_i))

    def test_str(self):
        locale.setlocale(locale.LC_ALL, 'en_GB.utf-8')
        self.assertEqual("2sctog",
            str(self._StitchTogetherInstruction()))
        self.assertEqual("2dctog",
            str(self._StitchTogetherInstruction(stitch='dc')))
        self.assertEqual("2sctog in next 2",
            str(self._StitchTogetherInstruction(stitch_count=2)))
        self.assertEqual("3sctog",
            str(self._StitchTogetherInstruction(together_count=3)))
        sc3tog = self._StitchTogetherInstruction(together_count=3, stitch_count=2)
        self.assertEqual("3sctog in next 2",
            str(sc3tog))

    def test_eq(self):
        i1 = self._StitchTogetherInstruction()
        i2 = self._StitchTogetherInstruction()
        self.assertEqual(i1, i2)

        # Subclasses should never be equal to their parent stitch class:
        self.assertFalse(i1 == self._Instruction())

        i2 = self._StitchTogetherInstruction(stitch_count=2)
        self.assertNotEqual(i1, i2)


class TestMultipleStitchesInstruction(unittest.TestCase, StitchTestCaseMixin):
    def test_init(self):
        """ MultipleStitchesInstruction are initialised correctly.
        """
        i = self._MultipleStitchesInstruction()
        self.assertEqual('sc', i.stitch)
        self.assertEqual(1, i.stitch_count)
        self.assertEqual(1, i.stitches_into)
        self.assertEqual(2, i.stitches)

    def test_merge(self):
        i = self._MultipleStitchesInstruction()
        self.assertTrue(i.merge(self._MultipleStitchesInstruction()))
        self.assertEqual(2, i.stitch_count)
        self.assertEqual(2, i.stitches_into)
        self.assertEqual(4, i.stitches)

        three_sc_in_next = self._MultipleStitchesInstruction(multiple_count=3)
        self.assertFalse(i.merge(three_sc_in_next))

    def test_can_only_merge_MultipleStitchesInstructions(self):
        """ Only StitchTogetherInstructions can be merged into other StitchTogetherInstructions
        """
        i = self._MultipleStitchesInstruction()
        not_i = self._Instruction()
        self.assertFalse(i.merge(not_i))
        not_i = self._StitchTogetherInstruction()
        self.assertFalse(i.merge(not_i))
        not_i = self._InstructionGroup()
        self.assertFalse(i.merge(not_i))

    def test_str(self):
        locale.setlocale(locale.LC_ALL, 'en_GB.utf-8')
        self.assertEqual("2sc in next",
            str(self._MultipleStitchesInstruction()))
        self.assertEqual("2dc in next",
            str(self._MultipleStitchesInstruction(stitch='dc')))
        self.assertEqual("2sc in next 2",
            str(self._MultipleStitchesInstruction(stitch_count=2)))
        self.assertEqual("3sc in next",
            str(self._MultipleStitchesInstruction(multiple_count=3)))
        sc3tog = self._MultipleStitchesInstruction(multiple_count=3, stitch_count=2)
        self.assertEqual("3sc in next 2",
            str(sc3tog))

    def test_eq(self):
        i1 = self._MultipleStitchesInstruction()
        i2 = self._MultipleStitchesInstruction()
        self.assertEqual(i1, i2)

        i3 = self._MultipleStitchesInstruction(multiple_count=3)
        self.assertTrue(i1 != i3)
        self.assertFalse(i1 == i3)

        # Subclasses should never be equal to their parent stitch class:
        self.assertFalse(i1 == self._Instruction())

        i2 = self._MultipleStitchesInstruction(stitch_count=2)
        self.assertNotEqual(i1, i2)


class TestInstructionGroup(unittest.TestCase, UtilTestCaseMixin):
    def test_init(self):
        i = self._util.InstructionGroup()
        self.assertEqual(0, i.stitches)
        self.assertEqual(0, i.stitches_into)

    def test_merge(self):
        self.assertFalse(self._util.InstructionGroup().merge(self._util.InstructionGroup()))

    def test_append(self):
        i = self._util.InstructionGroup()

        # Appending one item adds that item to the group:
        i1 = self._util.Instruction()
        i.append(i1)
        self.assertEqual(i._instructions[0], i1)

        # Adding further instructions merges with the existing instruction:
        i.append(self._util.Instruction())
        self.assertEqual(i._instructions[0],
            self._util.Instruction(stitch_count=2))

        i.append(self._util.Instruction(stitch_count=3))
        self.assertEqual(i._instructions[0],
            self._util.Instruction(stitch_count=5))

        # Adding a different type, appends the new instruction:
        i.append(self._util.StitchTogetherInstruction())
        self.assertEqual(i._instructions[0],
            self._util.Instruction(stitch_count=5))
        self.assertEqual(i._instructions[1],
            self._util.StitchTogetherInstruction())

        # Adding further instructions merges with the existing instruction:
        i.append(self._util.StitchTogetherInstruction())
        self.assertEqual(i._instructions[1],
            self._util.StitchTogetherInstruction(stitch_count=2))

    def test_str(self):
        self.assertEqual('', str(self._util.InstructionGroup()))
        self.assertEqual('', str(self._util.InstructionGroup(repeats=6)))
        self.assertEqual('sc in next 1', str(self._util.InstructionGroup([
            self._util.Instruction()
        ])))
        self.assertEqual(
            '[sc in next 1. Repeat 6 times.]',
            str(self._util.InstructionGroup(
                [self._util.Instruction()],
                repeats=6)))
        self.assertEqual(
            '[sc in next 1, 2sc in next. Repeat 6 times.]',
            str(self._util.InstructionGroup(
                [self._util.Instruction(), self._util.MultipleStitchesInstruction()],
                repeats=6)))


class Test_output_txt(unittest.TestCase, UtilTestCaseMixin):
    def test_output_text(self):
        locale.setlocale(locale.LC_ALL, 'en_GB.utf-8')
        self.assertEqual('Row 1: Make a magic circle, 6sc into centre. (6)', self._util.instruction_txt(1, None, 6))
        self.assertEqual('Row 2: sc in each sc (6)', self._util.instruction_txt(2, 6., 6.))

        locale.setlocale(locale.LC_ALL, 'fi_FI.utf-8')
        self.assertEqual('1. krs: Tee taikarengas, 6 ks keskustaan.(6)', self._util.instruction_txt(1, None, 6))
        self.assertEqual('2. krs: ks jokaiseen ks:aan(6)', self._util.instruction_txt(2, 6., 6.))


class TestInit(unittest.TestCase):
    @property
    def _crocad(self):
        import crocad
        return crocad

    def test_find_command(self):
        import crocad.ball
        import crocad.donut
        import crocad.cone
        self.assertEqual(self._crocad.find_command('ball'), crocad.ball.main)
        self.assertEqual(self._crocad.find_command('sphere'), crocad.ball.main)
        self.assertEqual(self._crocad.find_command('donut'), crocad.donut.main)
        self.assertEqual(self._crocad.find_command('torus'), crocad.donut.main)
        self.assertEqual(self._crocad.find_command('cone'), crocad.cone.main)
        self.assertRaises(self._crocad.UserError, lambda: self._crocad.find_command('notexist'))



if __name__ == '__main__':
    unittest.main()