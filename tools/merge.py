#!/usr/bin/env python3
"""把某本書 src/ 裡的章節依 SUMMARY.md 的順序合併成單一 Markdown。用法：tools/merge.py electric"""
import re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
book = root / (sys.argv[1] if len(sys.argv) > 1 else "electric")
src = book / "src"
summary = (src / "SUMMARY.md").read_text(encoding="utf-8")
files = re.findall(r"\]\(([^)]+\.md)\)", summary)

parts = []
for f in files:
    p = src / f
    if not p.exists():
        print(f"缺少：{f}")
        continue
    parts.append(p.read_text(encoding="utf-8").rstrip() + "\n")

out = book / "全書.md"
out.write_text("\n\n---\n\n".join(parts), encoding="utf-8")
print(f"已合併 {len(parts)} 個檔案 → {out}（約 {sum(len(x) for x in parts):,} 字元）")
