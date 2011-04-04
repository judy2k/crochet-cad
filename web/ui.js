goog.provide('cui');

goog.require('crochet');
goog.require('goog.dom');

cui.sphere = function(row_count) {
	var instructions = crochet.sphere(row_count);
	var parent = goog.dom.getElement('instructions');
	goog.array.forEach(instructions, function(instruction) {
		var elem = goog.dom.createTextNode(instruction);
		goog.dom.appendChild(parent, elem);
	});
};
goog.exportSymbol('cui.sphere', cui.sphere);