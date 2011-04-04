CLOSURE = ~/.bin/closure
CALCDEPS = python $(CLOSURE)/closure-library/closure/bin/calcdeps.py

all: crochet-cad.js

crochet-cad.js: crochet.js ui.js
	$(CALCDEPS)\
	    --path $(CLOSURE)/closure-library \
	    --input ui.js \
	    --path crochet.js \
	    --compiler_jar $(CLOSURE)/closure-compiler/compiler.jar \
	    --output_mode compiled \
	    --compiler_flags="--compilation_level=ADVANCED_OPTIMIZATIONS" \
	    --compiler_flags="--create_source_map=./crochet-cad-map.json" \
	    > crochet-cad.js

# --path $(CLOSURE)/closure-templates/javascript/soyutils_usegoog.js \
# --path hello.soy.js \

clean:
	rm -f crochet-cad.js

.PHONY: all clean