#!/bin/zsh
set -euo pipefail

cd "$(dirname "$0")/.."
set -a
. 02_Working_Files/orbital_credentials.env
set +a

python3 02_Working_Files/import_orbital_catalog.py
