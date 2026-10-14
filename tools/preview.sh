#!/usr/bin/env bash
# 把一張接線圖規格畫成 SVG 並截圖成 PNG 方便檢查：
#   tools/preview.sh electric/diagrams/09-2-transistor-motor.json [輸出目錄]
# SVG 會寫到 electric/src/images/<名稱>.svg，PNG 寫到輸出目錄（預設 /tmp/bbpreview）。
set -e
cd "$(dirname "$0")/.."
spec="$1"; out="${2:-/tmp/bbpreview}"; mkdir -p "$out"
name="$(basename "${spec%.json}")"
book="$(basename "$(dirname "$(dirname "$spec")")")"
svg="$book/src/images/$name.svg"
python3 tools/bbdraw.py "$spec" "$svg"
W=$(grep -o 'width="[0-9]*"' "$svg" | head -1 | tr -dc 0-9)
H=$(grep -o 'height="[0-9]*"' "$svg" | head -1 | tr -dc 0-9)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --hide-scrollbars \
  --window-size="$W,$H" --screenshot="$out/$name.png" "file://$PWD/$svg" >/dev/null 2>&1
echo "$out/$name.png"
