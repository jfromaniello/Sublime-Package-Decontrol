import sublime_plugin
import sublime
import subprocess
import os
import zipfile
import sys
import urllib.request, urllib.error, urllib.parse

urllib.request.install_opener(urllib.request.build_opener(urllib.request.ProxyHandler()))
packages_path = sublime.packages_path()


class PackageDecontrolCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Enter {username}/{repository name}', '', self.on_done, self.on_change, self.on_cancel)

    def on_done(self, name):
        print('Installing package %s' % name)
        
        name, branch = (name.split("#") + ["master"])[:2]

        tempfile = name.replace('/', '-') + '.zip'
        self.download(name, tempfile, branch)
        self.unzip(name, tempfile)
        os.remove(tempfile)

    def download(self, name, tempfile, branch = "master"):
        def exist(name):
            try:
                return subprocess.call([name, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0
            except:
                return False

        url = "https://github.com/%s/archive/%s.zip" % (name, branch)
        
        if('ssl' in sys.modules):
            print('installing with liburl')
            self.download_native(url, tempfile)
        else:
            if(os.name == 'nt'):
                print("can't download in Windows without ssl")
            else:
                if(exist('curl')):
                    print('installing with curl')
                    self.download_with_curl(url, tempfile)
                elif(exist('wget')):
                    print('installing with wget')
                    self.download_with_curl(url, tempfile)
                else:
                    print('you need to install curl or wget in order to install packages')

    def download_native(self, url, tempfile):
        request = urllib.request.urlopen(url)
        open(tempfile, 'wb').write(request.read())

    def download_with_curl(self, url, tempfile):
        command = ['curl', '-L', url]

        f = open(tempfile, 'w')
        proc = subprocess.Popen(command, stdout=f, stderr=subprocess.PIPE)
        proc.wait()

    def download_with_wget(self, url, tempfile):
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

            fd = open(os.path.join(dirname, filename), "wb")
            fd.write(zf.read(name))
            fd.close()

    def on_change(self, name):
        pass

    def on_cancel(self, name):
        pass
