
default: build
.PHONY: build install clean

#prefix="/usr"  # global install
prefix="${HOME}"/.local  # user install
executable="${prefix}/bin/img"
manpage="${prefix}/share/man/man1/img.1"

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

build/img: $(wildcard **/*.py)
	@bash ./scripts/make-build.sh

build/img.1: docs/img.1.md
	@bash ./scripts/make-manpage.sh

install: | build uninstall
	cp build/img "${executable}"

uninstall:
	[ -f "${executable}" ] && rm "${executable}"
	[ -f "${manpage}" ] && rm "${manpage}"

clean:
	rm -rf build/src/
	rm -rf build/requirements.txt
	rm -rf build/img
