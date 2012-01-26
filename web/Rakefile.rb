require 'rake/clean'

# Digest::MD5.file('Vagrantfile').hexdigest[0...8]

task :default => 'dev/index.html'

directory "dev"
CLOBBER.include 'dev'

file 'dev/index.html' => ['dev', 'src/index.html'] do
    cp 'src/index.html', 'dev/index.html'
end
CLOBBER.include 'dev/index.html'

for dep in FileList['src/js/lib/*.js']

if false then
    dep_reqs = FileList['js/lib/*.js']
    file 'js/gen/deps.js' => dep_reqs do |t|
        sh "java -jar support/closure-compiler.jar --warning_level QUIET --js_output_file js/gen/deps.js --js #{dep_reqs.join(' --js ')}"
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
end
