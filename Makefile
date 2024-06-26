
default: build
.PHONY: build install uninstall clean pull clean

#prefix=/usr
prefix=$(HOME)/.local
executable=$(prefix)/bin/img
manpage=$(prefix)/share/man/man1/img.1

help:
	@echo "make"
	@echo "make build"
	@echo "make install"
	@echo "make uninstall"
	@echo "make clean"
	@echo ""
	@echo "make  # for a user install (default)"
	@echo "make prefix=/usr  # for a global install"

build: build/img build/img.1

build/img: $(wildcard src/**/*.py)
	@bash ./scripts/make-build.sh

build/img.1: docs/img.1.md
	@bash ./scripts/make-manpage.sh

install: | build uninstall
	cp build/img "${executable}"
	cp build/img.1 "${manpage}"

uninstall:
	rm -f "${executable}"
	rm -f "${manpage}"

clean:
	rm -rf build/src/
	rm -rf build/requirements.txt
	rm -rf build/img
	rm -rf build/img.?

pull:
	git pull

update: | uninstall clean pull build install
