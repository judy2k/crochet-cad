#!/usr/bin/env rake -f

task :default => 'translations:extract'

desc "Translation management tasks."
namespace :translations do
    desc "Extract tagged strings from the python source into crochet-cad.pot"
    task :extract do
        sh "./tools/pygettext.py -v -a -o crocad/locale/crochet-cad.pot crocad/*.py"
    end

    desc "Pull available translations from Transifex."
    task :pull do
        FileUtils.cd('crocad/locale') do
            sh "tx pull --all"
        end
    end

    desc "Push crochet-cad.pot to Transifex server. (Privileged operation)"
    task :push => :extract do
        FileUtils.cd('crocad/locale') do
            sh "tx push -s"
        end
    end

    desc "Compile translation source (.po) files into .mo files."
    task :compile do
        Dir.glob('crocad/locale/*.po') do |fn|
            FileUtils.mkdir_p(fn.pathmap("crocad/locale/%n/LC_MESSAGES"))
            sh "./tools/msgfmt.py -o '#{fn.pathmap('crocad/locale/%n/LC_MESSAGES/crochet-cad.mo')}' '#{fn}'"
        end
    end

    desc "Pull and compile translations from Transifex"
    task :update => [:pull, :compile]
end