Sublime Package to install packages from github repositories.

![](http://content.screencast.com/users/JoseFR/folders/Jing/media/2774b50b-89c1-4980-a51c-e2db27e5d136/2013-01-11_1041.png)

## Installation

Paste this in sublime console:

> import urllib2,os,zipfile; pf='Package Decontrol.sublime-package'; pp=sublime.packages_path(); fp=os.path.join(pp,pf); urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler())); open(fp,'wb').write(urllib2.urlopen('http://bit.ly/package-decontrol').read()); zipfile.ZipFile(fp).extractall(os.path.join(pp, 'Package Decontrol'))


## Why?

Sublime's [Package Control](http://wbond.net/sublime_packages/package_control) is a nice way to **discover** and install sublime plugins and themes. However, is a pain for a plugin developer to publish to the package control because you have to edit [this **69KB** file](https://github.com/wbond/package_control_channel/blob/master/repositories.json) and wait to someone to approve your pull request.

I build this sublime extension because I believe that the github search engine and google itself are good enough for the discovering part. With ```Package Decontrol``` you can install plugin from github as follows:

- ```command+shift+p``` 
- Package Decontrol: Install from github
- Enter the name of the user/repository, eg: ```jfromaniello/sublime-node-require```

## Todo

- add "Remove Package", for now just delete the folder or use package control "remove package" :)
- add other sources of packages, like gist or bitbucket

## License 

MIT
