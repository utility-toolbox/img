
default: build
.PHONY: build install clean

prefix="${HOME}"/.local/bin

build: build/img

build/img: $(wildcard **/*.py)
	@bash ./scripts/make-build.sh

install: build/img
	[ -f "${prefix}"/img ] && @rm "${prefix}"/img
	@cp build/img "${prefix}"/img

uninstall:
	@rm "${prefix}"/img

clean:
	@rm -rf build/src/
	@rm -rf build/requirements.txt
	@rm -rf build/img
