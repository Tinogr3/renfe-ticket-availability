#!/usr/bin/env bash

set -euo pipefail
IFS=$'\n\t'

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

if [[ ! -d "venv" ]]; then
  echo "No se encuentra venv. Crea uno con: python3 -m venv venv" >&2
  exit 1
fi

source venv/bin/activate

# Parámetros de ejemplo, puedes modificarlos según tus necesidades
ORIGEN="MADRID (TODAS)"
DESTINO="BARCELONA (TODAS)"
FECHA="02/05/2026"
SALIDA="15:00"
LLEGADA="18:00"
DURACION="120"

python mainAuto.py --origen "$ORIGEN" --destino "$DESTINO" --fecha "$FECHA" --salida "$SALIDA" --llegada "$LLEGADA" --duracion "$DURACION"

# python main.py --salida "$SALIDA" --llegada "$LLEGADA" --duracion "$DURACION"

