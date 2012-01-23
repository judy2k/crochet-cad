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

    describe('', function() {
        it('', function() {
        })
    });
});
