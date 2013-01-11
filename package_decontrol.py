import sublime_plugin
import sublime
import subprocess
import os
import zipfile
import sys
import urllib2

urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler()))
packages_path = sublime.packages_path()


class PackageDecontrolCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Enter {username}/{repository name}', '', self.on_done, self.on_change, self.on_cancel)

    def on_done(self, name):
        print('Installing package %s' % name)
        tempfile = name.replace('/', '-') + '.zip'
        self.download(name, tempfile)
        self.unzip(name, tempfile)
        os.remove(tempfile)

    def download(self, name, tempfile):
        def exist(name):
            try:
                return subprocess.call([name, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
            except:
                return False

        if('ssl' in sys.modules):
            print 'installing with liburl'
            self.download_native(name, tempfile)
        else:
            if(os.name == 'nt'):
                print "can't download in Windows without ssl"
            else:
                if(exist('curl')):
                    print 'installing with curl'
                    self.download_with_curl(name, tempfile)
                elif(exist('wget')):
                    print 'installing with wget'
                    self.download_with_curl(name, tempfile)

    def download_native(self, name, tempfile):
        url = "https://github.com/%s/archive/master.zip" % name
        request = urllib2.urlopen(url)
        open(tempfile, 'wb').write(request.read())

    def download_with_curl(self, name, tempfile):
        url = "https://github.com/%s/archive/master.zip" % name
        command = ['curl', '-L', url]

        f = open(tempfile, 'w')
        proc = subprocess.Popen(command, stdout=f, stderr=subprocess.PIPE)
        proc.wait()

    def download_with_wget(self, name, tempfile):
        url = "https://github.com/%s/archive/master.zip" % name
        command = ['wget', '-O', tempfile, url]

        proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.wait()

    def unzip(self, name, tempfile):
        zf = zipfile.ZipFile(tempfile)
        for name in zf.namelist():
            (dirname, filename) = os.path.split(name)
            dirname = os.path.join(packages_path, dirname)

            if not os.path.exists(dirname):
                os.mkdir(dirname)

            if name[-1] == '/':
                #is a directory
                continue

            if filename == '.gitignore':
                continue

            fd = open(os.path.join(dirname, filename), "w")
            fd.write(zf.read(name))
            fd.close()

    def on_change(self, name):
        pass

    def on_cancel(self, name):
        pass
