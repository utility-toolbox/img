#!/usr/bin/env bash
set -e

cd "$(realpath "$(dirname "$(realpath "$0")")/..")"

# create build directory
mkdir -p "build/"

# remove old source-code
[[ -f "build/img" ]] && rm "build/img"
[[ -f "build/requirements.txt" ]] && rm "build/requirements.txt"
[[ -d "build/src/" ]] && rm -rf "build/src/"

PIPENV_INSTALLED=false
if ! python3 -c 'import pipenv' &> /dev/null; then
  python3 -m pip install --isolated --no-input --disable-pip-version-check pipenv
fi

PIPENV_VERBOSITY=-1 pipenv requirements > build/requirements.txt

if [ $PIPENV_INSTALLED = true ]; then
  python3 -m pip uninstall --isolated --no-input --disable-pip-version-check pipenv
fi

# copy source code
cp -r src/img/ build/src/

# install dependencies into (new) copied source-code directory
python3 -m pip install --isolated --no-input --disable-pip-version-check --requirement build/requirements.txt --target build/src/ --compile
rm -rf build/src/*.dist-info

# cleanup of necessary packages
rm -rf build/src/bin/  # executables/scripts
rm -rf build/src/pygments/  # syntax highlighting
rm -rf build/src/markdown_it/  # markdown parser
rm -rf build/src/urllib3/  # builtin urllib is enough

# make archive (from the new source-code directory)
python3 -m zipapp --compress --python "/usr/bin/env -S python3 -X utf8 -X faulthandler -B -O" build/ --main src.__main__:main --output build/img
