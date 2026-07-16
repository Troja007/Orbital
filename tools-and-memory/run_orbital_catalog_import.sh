#!/bin/zsh
set -euo pipefail

cd "$(dirname "$0")/.."

python3 tools-and-memory/import_orbital_catalog.py
