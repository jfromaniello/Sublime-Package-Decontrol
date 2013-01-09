clean:
	rm -f "Package Decontrol.sublime-package"

build: clean
	zip -r "Package Decontrol.sublime-package" . -x "Package Decontrol.sublime-package"