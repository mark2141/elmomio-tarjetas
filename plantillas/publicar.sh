#!/bin/bash
# Uso: publicar.sh imagen.png [nombre-destino.png]
# Sube la imagen a mark2141/elmomio-tarjetas en carpeta AAAA-MM-DD y muestra su URL raw directa.
set -e
SRC="$1"; NAME="${2:-$(basename "$SRC")}"
REPO_DIR=/workspace/elmomio-tarjetas
DAY=$(date +%F)
cd "$REPO_DIR"
git pull -q --rebase origin main 2>/dev/null || true
mkdir -p "$DAY"; cp "$SRC" "$DAY/$NAME"
git add "$DAY/$NAME"
git commit -q -m "Tarjeta $DAY/$NAME"
git -c http.extraHeader="Authorization: Basic $(printf 'x-access-token:%s' "$GITHUB_TARJETAS_TOKEN" | base64 -w0)" push -q origin main
URL="https://raw.githubusercontent.com/mark2141/elmomio-tarjetas/main/$DAY/$NAME"
for i in $(seq 1 12); do
  CT=$(curl -s -o /dev/null -w '%{http_code} %{content_type}' "$URL")
  [[ "$CT" == 200* ]] && break; sleep 5
done
echo "$URL ($CT)"
