describe('crocad', function() {
    describe('row', function() {
        var row;
        beforeEach(function() {
            row = Crocad.row;
        });
        it('can generate the first row', function() {
            var gen = row(null, 12);
            var exp = new Crocad.InstructionGroup([new Crocad.Instruction(12,'ch')]);
            expect(gen).toEqual(exp);
        });
        it('can generate an equal row', function() {
            var gen = row(12, 12);
            var exp = new Crocad.InstructionGroup([new Crocad.Instruction(12)]);
            expect(gen).toEqual(exp);
        });
        it('can generate an increasing row', function() {
            var gen = row(12, 13);
            var exp = new Crocad.InstructionGroup([
                new Crocad.MultipleStitches(),
                new Crocad.Instruction(11)
            ]);
            expect(gen).toEqual(exp);
            expect(gen.stitches()).toBe(13)
            expect(gen.stitchesInto()).toBe(12)
        });
        it('can generate a decreasing row', function() {
            var gen = row(13, 12);
            var exp = new Crocad.InstructionGroup([
                new Crocad.StitchTogether(),
                new Crocad.Instruction(11)
            ]);
            expect(gen).toEqual(exp);
            expect(gen.stitches()).toBe(12)
            expect(gen.stitchesInto()).toBe(13)
        });
        it('can generate an increasing row with a repeat', function() {
            var gen = row(6, 9);
            var exp = new Crocad.InstructionGroup([
                new Crocad.InstructionGroup([
                    new Crocad.MultipleStitches(),
                    new Crocad.Instruction()
                ],3)
            ]);
            expect(gen).toEqual(exp);
            expect(gen.stitches()).toBe(9)
            expect(gen.stitchesInto()).toBe(6)
        });
        it('can generate a decreasing row with a repeat', function() {
            var gen = row(9, 6);
            var exp = new Crocad.InstructionGroup([
                new Crocad.InstructionGroup([
                    new Crocad.StitchTogether(),
                    new Crocad.Instruction()
                ],3)
            ]);
            expect(gen.stitches()).toBe(6)
            expect(gen.stitchesInto()).toBe(9)
            expect(gen).toEqual(exp);
        });
        it('can generate an increasing row with a repeat and a remainder', function() {
            var gen = row(8, 11);
            var exp = new Crocad.InstructionGroup([
                new Crocad.InstructionGroup([
                    new Crocad.MultipleStitches(),
                    new Crocad.Instruction()
                ],3),
                new Crocad.Instruction(2)
            ]);
            expect(gen).toEqual(exp);
            expect(gen.stitches()).toBe(11)
            expect(gen.stitchesInto()).toBe(8)
        });
        it('can generate a decreasing row with a repeat and a remainder', function() {
            var gen = row(10, 7);
            var exp = new Crocad.InstructionGroup([
                new Crocad.InstructionGroup([
                    new Crocad.StitchTogether(),
                    new Crocad.Instruction()
                ],3),
                new Crocad.Instruction()
            ]);
            expect(gen.stitches()).toBe(7)
            expect(gen.stitchesInto()).toBe(10)
            expect(gen).toEqual(exp);
        });
 
    });

    describe('gcd', function() {
        it('can calculate greatest common divisors', function() {
            var gcd = Crocad.gcd;

            expect(gcd(12,15)).toBe(3);
        });
    });

    describe('sum', function() {
        it('can add up numbers', function() {
            var sum = Crocad.sum;
            expect(sum([])).toBe(0);
            expect(sum([57])).toBe(57);
            expect(sum([1,2,3])).toBe(6);
            expect(sum([2,2,3])).toBe(7);
        });
    });

    describe('roundToNearest', function() {
        var rtn;
        beforeEach(function() {
            rtn = Crocad.roundToNearest;
        });
        it('can round to the nearest n', function() {
            expect(rtn(0, 6)).toBe(0);
            expect(rtn(1, 6)).toBe(0);
            expect(rtn(2, 6)).toBe(0);
            expect(rtn(2.99999, 6)).toBe(0);
            expect(rtn(3, 6)).toBe(6);
            expect(rtn(3.11111, 6)).toBe(6);
            expect(rtn(4, 6)).toBe(6);
            expect(rtn(5, 6)).toBe(6);
            expect(rtn(6, 6)).toBe(6);
            expect(rtn(7, 6)).toBe(6);
            expect(rtn(8, 6)).toBe(6);
            expect(rtn(8.99999, 6)).toBe(6);
            expect(rtn(9, 6)).toBe(12);
        });
        it('should ensure a minimum value', function() {
            expect(rtn(0, 6, 4)).toBe(4);
            expect(rtn(1, 6, 4)).toBe(4);
            expect(rtn(2, 6, 4)).toBe(4);
            expect(rtn(2.99999, 6, 4)).toBe(4);
        });
        it('should operate on lists', function() {
            expect(rtn([0,2,4,5], 6)).toEqual([0,0,6,6]);
        })
        it('should operate on numbers', function() {
            expect(rtn(0, 6)).toBe(0);
            expect(rtn(5, 6)).toBe(6);
        });
    });

    describe('Instruction', function() {
        it('can be instantiated', function() {
            var i = new Crocad.Instruction();
            expect(i).not.toBeUndefined();
            expect(i.stitches()).toBe(1);
            expect(i.stitchesInto()).toBe(1);
        });
        it('should be human-readable in the console', function(){
            expect(new Crocad.Instruction().toString()).toEqual("sc");
            expect(new Crocad.Instruction(2).toString()).toEqual("2sc");
            expect(new Crocad.Instruction(2, 'sc').toString()).toEqual("2sc");
        });
        it('should have the same value for stitches as for stitchesInto', function() {
            expect(new Crocad.Instruction(2).stitchesInto()).toBe(2);
        });
        it('should merge with other Instructions', function() {
            var i = new Crocad.Instruction(3);
            var j = new Crocad.Instruction(4);
            expect(i.merge(j)).toBe(true);
            expect(i.stitches()).toBe(7);
            expect(i.merge(new Crocad.StitchTogether())).toBe(false);
        });
    });

    describe('StitchTogether', function() {
        it('can be instantiated', function() {
            var st = new Crocad.StitchTogether();
            expect(st).not.toBeUndefined();
            expect(st.stitches()).toBe(1);
            expect(st.stitchesInto()).toBe(2);
        })
        it('should be human-readable in the console', function(){
            expect(new Crocad.StitchTogether().toString()).toEqual("sc2tog");
            expect(new Crocad.StitchTogether(5).toString()).toEqual("sc2tog in next 5");
            expect(new Crocad.StitchTogether(5, 3).toString()).toEqual("sc3tog in next 5");
            expect(new Crocad.StitchTogether(1, 3).toString()).toEqual("sc3tog");
        });
        it('should merge with other Instructions', function() {
            var i = new Crocad.StitchTogether(3);
            var j = new Crocad.StitchTogether(4);
            expect(i.merge(j)).toBe(true);
            expect(i.stitches()).toBe(7);
            expect(i.stitchesInto()).toBe(14);
            expect(i.merge(new Crocad.Instruction())).toBe(false);
        });
    });

    describe('MultipleStitches', function() {
        it('can be instantiated', function() {
            var st = new Crocad.MultipleStitches();
            expect(st).not.toBeUndefined();
            expect(st.stitches()).toBe(2);
            expect(st.stitchesInto()).toBe(1);
        })
        it('should be human-readable in the console', function() {
            expect(new Crocad.MultipleStitches().toString()).toEqual("2sc into stitch");
            expect(new Crocad.MultipleStitches(4, 2).toString()).toEqual("2sc into next 4 stitches");
            expect(new Crocad.MultipleStitches(1, 3).toString()).toEqual("3sc into stitch");
            expect(new Crocad.MultipleStitches(4, 3).toString()).toEqual("3sc into next 4 stitches");
        })
        it('should merge with other Instructions', function() {
            var i = new Crocad.MultipleStitches(3);
            var j = new Crocad.MultipleStitches(4);
            expect(i.merge(j)).toBe(true);
            expect(i.stitches()).toBe(14);
            expect(i.stitchesInto()).toBe(7);
            expect(i.merge(new Crocad.Instruction())).toBe(false);
        });
    });
    
    describe('InstructionGroup', function() {
        it('can be instantiated', function(){
            var g = new Crocad.InstructionGroup();
            expect(g).not.toBeUndefined();
            expect(g.stitches()).toBe(0);
            expect(g.stitchesInto()).toBe(0);
        });
        it('can hold Instructions', function() {
            var Instruction = Crocad.Instruction;
            var g = new Crocad.InstructionGroup([
                new Instruction(),
                new Instruction(),
                new Instruction(),
            ]);
            expect(g.stitches()).toBe(3);
            expect(g.stitchesInto()).toBe(3);
            expect(g.toString()).toBe('sc, sc, sc');
        });

        it('can correctly merge instructions', function() {
            var Instruction = Crocad.Instruction;

            var g = new Crocad.InstructionGroup();
            g.append(new Instruction());
            g.append(new Instruction());
            g.append(new Instruction());
            expect(g.toString()).toBe('3sc')
            g.append(new Crocad.MultipleStitches())
            expect(g.toString()).toBe('3sc, 2sc into stitch')
            g.append(new Crocad.MultipleStitches())
            expect(g.toString()).toBe('3sc, 2sc into next 2 stitches')
            g.append(new Crocad.MultipleStitches(1,3))
            expect(g.toString()).toBe('3sc, 2sc into next 2 stitches, 3sc into stitch')
        })
        it('can handle repeats', function() {
            var g = new Crocad.InstructionGroup([
                new Crocad.MultipleStitches(6)
            ], 3);
            expect(g.stitches()).toBe(36);
            expect(g.stitchesInto()).toBe(18);
        });
    });

});
