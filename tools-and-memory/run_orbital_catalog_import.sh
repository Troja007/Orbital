#!/bin/zsh
set -euo pipefail

cd "$(dirname "$0")/.."
set -a
. tools-and-memory/orbital_credentials.env
set +a

python3 tools-and-memory/import_orbital_catalog.py
