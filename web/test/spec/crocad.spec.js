describe('crocad', function() {
    var cc;

    beforeEach(function() {
        cc = new Crocad();
    });

    it('can be instantiated', function() {
        expect(cc).not.toBeUndefined();
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
            expect(new Crocad.MultipleStitches(2,4).toString()).toEqual("2sc into next 4 stitches");
            expect(new Crocad.MultipleStitches(3, 1).toString()).toEqual("3sc into stitch");
            expect(new Crocad.MultipleStitches(3, 4).toString()).toEqual("3sc into next 4 stitches");
        })
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
    });

    describe('', function() {
        it('', function() {
        })
    });
});
