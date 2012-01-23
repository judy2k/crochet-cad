require 'rake/clean'

task :default => 'js/gen/deps.js'
CLOBBER.include 'js/gen/deps.js'

directory "js/gen"
CLOBBER.include 'js/gen'

dep_reqs = FileList['js/lib/*.js']
file 'js/gen/deps.js' => dep_reqs do |t|
    sh "closure --warning_level QUIET --js_output_file js/gen/deps.js --js #{dep_reqs.join(' --js ')}"
end
task 'js/gen/deps.js' => 'js/gen'


FileList['coffee/*.coffee'].each do |src|
    target = File.join('js/gen', src.pathmap('%n.js'))
    file target => src do |t|
        sh "coffee -o #{File.dirname(t.name)} -c #{src}"
    end
    CLOBBER.include(target)
    task :default => target
end
        

FileList['sass/*.scss'].each do |src|
  target = File.join('stylesheets', src.pathmap('%n.css'))
  file target => src do
    sh "compass compile . #{src}"
  end
  
  CLOBBER.include(target)
  task :default => target
end
