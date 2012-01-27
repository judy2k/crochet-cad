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

directory "dev/css/lib"
FileList['src/css/lib/*.css'].each do |src|
    target = src.pathmap('dev/css/lib/%n.css')
    file target => ['dev/css/lib', src] do |t|
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
