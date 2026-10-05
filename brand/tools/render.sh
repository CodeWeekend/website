#!/bin/bash
# render.sh <input.svg|input.html> <output.png> <width> <height>
# Renders an SVG or HTML file to PNG with headless Chrome (webfonts in HTML are allowed to load).
set -e
[ -f "$1" ] || { echo "render.sh: input not found: $1" >&2; exit 1; }
mkdir -p "$(dirname "$2")"
IN="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"; OUT="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"; W="${3:-1200}"; H="${4:-800}"
rm -f "$OUT"
perl -e 'alarm shift; exec @ARGV' 45 "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --virtual-time-budget=4000 \
  --screenshot="$OUT" --window-size="$W,$H" "file://$IN" >/dev/null 2>&1 || true
[ -f "$OUT" ] || { echo "render.sh: chrome failed to write $OUT" >&2; exit 1; }
echo "$OUT"
