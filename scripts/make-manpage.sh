#!/usr/bin/env bash
set -e

cd "$(realpath "$(dirname "$(realpath "$0")")/..")"

function log() {
    echo -e "\e[36m$*\e[39m"
}

mkdir -p "build/"

MANPAGE="build/img.1"

log "Cleanup of previous files"
[[ -f "$MANPAGE" ]] && rm "$MANPAGE"


ROFF_GOT_INSTALLED=false
if  ! command -v roff &> /dev/null; then
  log "Installing roff to create man-pages"
  python3 -m pip install --user --isolated --no-input --disable-pip-version-check roff
  ROFF_GOT_INSTALLED=true
fi

log "Creating man-page"
roff convert "docs/img.1.md" "$MANPAGE"

if [ $ROFF_GOT_INSTALLED = true ]; then
  log "Removing roff after man-page creation"
  python3 -m pip uninstall --yes --isolated --no-input --disable-pip-version-check roff
fi

log "man-page created ($MANPAGE)"
