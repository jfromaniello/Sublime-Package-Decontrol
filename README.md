Sublime's [Package Control](http://wbond.net/sublime_packages/package_control) is a nice way to **discover** and install sublime plugins and themes. However, is a pain for a plugin developer to publish to the package control because you have to edit [this **69KB** file](https://github.com/wbond/package_control_channel/blob/master/repositories.json) and wait to someone to approve your pull request.

I build this sublime extension because I believe that the github search engine and google itself are good enough for the discovering part. With ```Package Decontrol``` you can install plugin from github as follows:

- ```command+shift+p``` 
- Package Decontrol: Install from github
- Enter the name of the user/repository, eg: ```jfromaniello/sublime-node-require```


**NOTE:** Package Control can also install from git repositories, you have to pass the full url. The function is call "Add Repository".

### Installation

Paste this in sublime console:

<pre style="word-wrap: break-word;"><code>import urllib2,os; pf='Package Decontrol.sublime-package'; ipp=sublime.installed_packages_path(); os.makedirs(ipp) if not os.path.exists(ipp) else None; urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler())); open(os.path.join(ipp,pf),'wb').write(urllib2.urlopen('http://bit.ly/package-decontrol').read()); print 'Please restart Sublime Text to finish installation'
</code></pre>

### Todo

- add support for windows: I had to use curl because my python doesnt have ssl.
- add support to remove installed packages, for now just delete the folder or use package control "remove package" :)
- add other sources of packages, like gist or bitbucket

### License 

MIT