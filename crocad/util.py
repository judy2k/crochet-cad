#!python
# -*- coding: utf-8 -*-


from fractions import gcd


__all__ = ['instruction', 'round_to_nearest', 'round_to_nearest_iter']


class Instruction(object):
    def __init__(self, stitch='sc', stitch_count=1):
        self.stitch = stitch
        self.stitch_count = stitch_count
        
    def stitches(self):
        return self.stitch_count
    
    stitches_into = stitches
    
    def str(self):
        return '%s in next %d' % (self.stitch, self.stitch_count)


class StitchTogetherInstruction(Instruction):
    """
    stXtog
    """
    def __init__(self, stitch_count=1, together_count=2):
        super(StitchTogetherInstruction, self).__init__(stitch=stitch,
                stitch_count=stitch_count)
        self.together_count = together_count
    
    def stitches(self):
        return self.stitch_count
    
    def stitches_into(self):
        return self.stitch_count * self.together_count
    
    def str(self):
        s = '%d%stog' % (self.together_count, self.stitch)
        if self.stitch_count > 1:
            s += ' in next %d' % self.stitch_count
        return s
        
class MultipleStitchesInstruction(Instruction):
    """
    X st in st
    """
    def __init__(self, stitch_count=1, multiple_count=2):
        super(MultipleStitchesInstruction, self).__init__(stitch=stitch,
                stitch_count=stitch_count, multiple_count=multiple_count)
    
    def stitches(self):
        return self.stitch_count

def instruction(prev, count):
    """
    Returns the instructions for a circular row with `count` stitches,
    crocheted on to a row of `prev` stitches.
    """
    result = ''
    if prev is None:
        result += 'ch %d, sc in each chain' % count
    else:
        row_count = count
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
            sc, sc_rem = divmod(scs, abs(diff))
            if repeats:
                result += '*'
            part_count = int(abs(diff))
            for i in range(part_count):
                result += (' 2sc in next' if diff > 0 else ' 2sctog')
                if i < abs(diff) - 1:
                    if sc:
                        result += ', %dsc' % sc
                else:
                    if (sc + sc_rem):
                        result += ', %dsc' % (sc + sc_rem)
            if repeats:
                result += ', repeat from * %d times' % repeats
                
            if row_rem:
                result += ' %dsc ' % row_rem
            
        result += ' (%d)' % row_count
    
    return result


def round_to_nearest(i, n=1, min_val=0):
    """Return i rounded to the nearest n."""
    return max(min_val, ((i // n) + round(float(i % n) / n)) * n)


def round_to_nearest_iter(i, n=1, min_val=0):
    for val in i:
        yield round_to_nearest(val, n, min_val)