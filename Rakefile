#!/usr/bin/env rake -f

task :default => :extract_translations

task :extract_translations do
    sh "./tools/pygettext.py -v -a -o thing.pot crocad/*.py"
end
