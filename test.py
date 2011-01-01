#!/usr/bin/env python
# -*- coding: utf-8 -*-


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
        self.assertEquals([4,4,4,4,4,6,6,8,8,10], list(self._rtni(range(10), 2, 4)))


if __name__ == '__main__':
    unittest.main()