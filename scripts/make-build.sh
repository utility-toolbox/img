#!/usr/bin/env bash
set -e

cd "$(realpath "$(dirname "$(realpath "$0")")/..")"

function log() {
    echo -e "\e[36m$*\e[39m"
}

mkdir -p "build/"

log "Cleanup of previous build files"
[[ -f "build/img" ]] && rm "build/img"
[[ -f "build/requirements.txt" ]] && rm "build/requirements.txt"
[[ -d "build/src/" ]] && rm -rf "build/src/"

PIPENV_GOT_INSTALLED=false
if  ! command -v pipenv &> /dev/null; then
  log "Installing pipenv for build for dependency freeze"
  python3 -m pip install --user --isolated --no-input --disable-pip-version-check pipenv
  PIPENV_GOT_INSTALLED=true
fi

log "Freezing dependencies"
PIPENV_VERBOSITY=-1 pipenv requirements > build/requirements.txt

if [ $PIPENV_GOT_INSTALLED = true ]; then
  log "Removing pipenv after freeze"
  python3 -m pip uninstall --user --isolated --no-input --disable-pip-version-check pipenv
fi

log "Copying source code"
cp -r src/img/ build/src/

log "Installing dependencies into build"
python3 -m pip install --isolated --no-input --disable-pip-version-check --requirement build/requirements.txt --target build/src/ --no-compile
rm -rf build/src/*.dist-info

log "Removing unnecessary packages"
rm -rf build/src/bin/  # executables/scripts
rm -rf build/src/pygments/  # syntax highlighting
rm -rf build/src/markdown_it/  # markdown parser
rm -rf build/src/urllib3/  # builtin urllib is enough

log "Creating executable build"
python3 -m zipapp --compress --python "/usr/bin/env -S python3 -X utf8 -X faulthandler -B -O" build/ --main src.__main__:main --output build/img
chmod +x build/img
