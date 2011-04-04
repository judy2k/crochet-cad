goog.provide('crochet');

crochet.sphere = function(row_count) {
	return ["Row 1: Make a magic circle, 6sc into centre. (6)",
	"Row 2: *, 2sc in next, repeat from * 6 times (12)",
	"Row 3: *, 2sc in next, 1sc, repeat from * 6 times (18)",
	"Row 4: *, 2sc in next, 2sc, repeat from * 6 times (24)",
	"Row 5: *, 2sc in next, 3sc, repeat from * 6 times (30)",
	"Row 6: sc in each sc (30)",
	"Row 7: sc in each sc (30)",
	"Row 8: *, 2sc in next, 4sc, repeat from * 6 times (36)",
	"Row 9: sc in each sc (36)",
	"Row 10: *, 2sctog, 4sc, repeat from * 6 times (30)",
	"Row 11: sc in each sc (30)",
	"Row 12: sc in each sc (30)",
	"Row 13: *, 2sctog, 3sc, repeat from * 6 times (24)",
	"Row 14: *, 2sctog, 2sc, repeat from * 6 times (18)",
	"Row 15: *, 2sctog, 1sc, repeat from * 6 times (12)",
	"Row 16: *, 2sctog, repeat from * 6 times (6)"];
};

goog.exportSymbol('crochet.sphere', crochet.sphere);