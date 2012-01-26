require 'rake/clean'

# Digest::MD5.file('Vagrantfile').hexdigest[0...8]

task :default => :devel

directory "dev"
CLOBBER.include 'dev'

file 'dev/index.html' => ['dev', 'src/index.html'] do
    cp 'src/index.html', 'dev/index.html'
end
task :devel => 'dev/index.html'

directory "dev/js/lib"

FileList['src/js/lib/*.js'].each do |src|
    target = src.pathmap('dev/js/lib/%n.js')
    file target => ['dev/js/lib', src] do |t|
        cp(src, t.name)
    end
    task :devel => target
end

FileList['src/coffee/*.coffee'].each do |src|
    target = src.pathmap('dev/js/gen/%n.js')
    file target => src do |t|
        sh "coffee -o #{File.dirname(t.name)} -c #{src}"
    end
    task :devel => target
end
        

FileList['src/sass/*.scss'].each do |src|
    target = src.pathmap('dev/css/%n.css')
    file target => src do
        sh "compass compile . #{src}"
    end
    task :devel => target
end


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
