#!/bin/bash
# compile.sh — Compile stats.c en bibliothèque partagée stats.so
# Usage : chmod +x compile.sh && ./compile.sh

set -e  # Arrêter si une commande échoue

SRC_DIR="src"
LIB_DIR="lib"
SRC_FILE="${SRC_DIR}/stats.c"
OUT_FILE="${LIB_DIR}/stats.so"

# Créer le dossier lib/ si nécessaire
mkdir -p "${LIB_DIR}"

echo "[1/2] Compilation de ${SRC_FILE}..."

# Détection du système d'exploitation
OS=$(uname -s)
if [ "$OS" = "Darwin" ]; then
    # macOS
    OUT_FILE="${LIB_DIR}/stats.dylib"
    gcc -dynamiclib -fPIC -O2 -Wall -lm -o "${OUT_FILE}" "${SRC_FILE}"
else
    # Linux
    gcc -shared -fPIC -O2 -Wall -lm -o "${OUT_FILE}" "${SRC_FILE}"
fi

echo "[2/2] Bibliothèque créée : ${OUT_FILE}"
echo "Compilation réussie !"
