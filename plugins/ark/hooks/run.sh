#!/usr/bin/env bash
# Roda um hook Python da ARK com o interpretador que existir na máquina (PC: python, Mac: python3).
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# No Windows o python é o 3.13 real: pula a checagem de versão, que abria um segundo Python a cada hook.
if [ -n "$WINDIR" ] && command -v python >/dev/null 2>&1; then PY=python
elif command -v python >/dev/null 2>&1 && python -c "import sys;sys.exit(0 if sys.version_info[0]==3 else 1)" 2>/dev/null; then PY=python
elif command -v python3 >/dev/null 2>&1; then PY=python3
else exit 0; fi
exec "$PY" "$DIR/$1.py"
