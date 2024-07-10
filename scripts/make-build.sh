#!/usr/bin/env bash
set -e

cd "$(realpath "$(dirname "$(realpath "$0")")/..")"

function log() {
    >&2 echo -e "\e[36m$*\e[39m"
}

mkdir -p "build/"

log "Cleanup of previous build files"
[[ -d build/img ]] && rm -rf build/img
[[ -f build/requirements.txt ]] && rm build/requirements.txt

PIPENV_GOT_INSTALLED=false
if  ! command -v pipenv &> /dev/null; then
  log "Installing pipenv for build for dependency freeze"
  python3 -m pip install --user --isolated --no-input --disable-pip-version-check pipenv
  PIPENV_GOT_INSTALLED=true
fi

log "Freezing dependencies"
PIPENV_VERBOSITY=-1 pipenv requirements --exclude-markers > build/requirements.txt

if [ $PIPENV_GOT_INSTALLED = true ]; then
  log "Removing pipenv after freeze"
  python3 -m pip uninstall --yes --isolated --no-input --disable-pip-version-check pipenv
fi

log "Copying source code"
mkdir -p build/img/
cp -r src/img/ build/img/img/

log "Installing dependencies into build"
python3 -m pip install --isolated --no-input --disable-pip-version-check --requirement build/requirements.txt --target build/img/
rm -rf build/img/*.dist-info

log "Removing unnecessary packages"
rm -rf build/img/bin/  # executables/scripts
rm -rf build/img/pygments/  # syntax highlighting
rm -rf build/img/markdown_it/  # markdown parser
rm -rf build/img/urllib3/  # builtin urllib is enough
rm -rf build/img/bs4/tests/

log "Creating executable build"
# shellcheck disable=SC2016
echo '#!/usr/bin/env bash
set -e
THIS="$(dirname "$(realpath "${BASH_SOURCE[0]}")")"
PYTHONPATH="$THIS:$PYTHONPATH" python3 -X utf8 -X faulthandler -BO -m img "$@"
' > build/img/img.sh
chmod +x build/img/img.sh
