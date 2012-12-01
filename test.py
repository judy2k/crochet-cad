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


class TestUtil(unittest.TestCase):
    @property
    def _rtn(self):
        import crocad.util
        return crocad.util.round_to_nearest
    
    @property
    def _rtni(self):
        import crocad.util
        return crocad.util.round_to_nearest_iter
    
    @property
    def _inst(self):
        import crocad.util
        return crocad.util.instruction
    
    def test_round_to_nearest(self):
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
        self.assertEquals([4,4,4,4,4,6,6,8,8,10],
                list(self._rtni(range(10), 2, 4)))

    def test_instruction(self):
        self.assertEqual('*, 2sc in next, 10sc, repeat from * 3 times 1sc ', self._inst(34.0, 37.0))
        self.assertEqual('*, 2sc in next, 10sc, repeat from * 3 times 1sc ', self._inst(34, 37))
        self.assertEqual(', 2sc in next, 10sc', self._inst(11, 12))
        self.assertEqual(', sc2tog, 10sc', self._inst(12, 11))
        self.assertEqual('sc in each sc', self._inst(12, 12))



if __name__ == '__main__':
    unittest.main()