import sublime_plugin
import subprocess
import os
import zipfile

packages_path = os.path.join(os.getcwdu(), '../')


class PackageDecontrolCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel('Enter {username}/{repository name}', '', self.on_done, self.on_change, self.on_cancel)

    def on_done(self, name):
        print('Installing' + name)
        tempfile = name.replace('/', '-') + '.zip'
        self.download_with_curl(name, tempfile)
        self.unzip(name, tempfile)
        os.remove(tempfile)

    # TODO, create a version for windows..
    # I am using this because my python doesnt have ssl.
    def download_with_curl(self, name, tempfile):
        url = "https://github.com/%s/archive/master.zip" % name
        command = ['curl', '-L', url]

        f = open(tempfile, 'w')
        proc = subprocess.Popen(command, stdout=f, stderr=subprocess.PIPE)
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
