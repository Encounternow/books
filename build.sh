#!/usr/bin/env bash
# 建置書架上所有的書到 _site/：
#   ./build.sh            → _site/index.html + _site/<書>/
#   ./build.sh serve 電書  → 只預覽一本（例如 ./build.sh serve electric）
#   ./build.sh merge 書   → 把一本書合併成單一 Markdown（例如 ./build.sh merge electric）
set -e
cd "$(dirname "$0")"

case "$1" in
  serve) exec mdbook serve "$2" --open ;;
  merge) exec python3 tools/merge.py "$2" ;;
esac

command -v mdbook >/dev/null 2>&1 || { echo "請先安裝 mdbook：brew install mdbook"; exit 1; }

rm -rf _site && mkdir -p _site
cp index.html CNAME _site/
for dir in */; do
  dir="${dir%/}"
  [ -f "$dir/book.toml" ] || continue
  echo "== 建置 $dir =="
  mdbook build "$dir" --dest-dir "$PWD/_site/$dir"
done
echo "完成：open _site/index.html"
