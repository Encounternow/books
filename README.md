# 書架　book.vichuang.tw

給國小高年級、國中生與零經驗大人的自學實作教材，每本書一個資料夾，用 [mdBook](https://rust-lang.github.io/mdBook/) 編成網頁，推上 `main` 就會自動發布到 https://book.vichuang.tw/ 。

| 資料夾 | 書名 | 網址 |
|---|---|---|
| `electric/` | 動手玩電：給國中生的電學、電子學與電路學實作課 | https://book.vichuang.tw/electric/ |
| `physics/` | 動手玩物理：家裡就能做的國中物理實驗課 | https://book.vichuang.tw/physics/ |
| `chemistry/` | 廚房裡的化學：安全又好玩的國中化學實驗課 | https://book.vichuang.tw/chemistry/ |
| `ai-use/` | AI 怎麼用：國中生與家長的 AI 應用課 | https://book.vichuang.tw/ai-use/ |
| `ai-theory/` | AI 怎麼運作：從機器學習到語言模型的直覺課 | https://book.vichuang.tw/ai-theory/ |
| `ai-build/` | AI 工程實作：從 Skill、MCP 到 RAG、LoRA 與自架模型 | https://book.vichuang.tw/ai-build/ |
| `mech/` | 動手玩機械與 3D 列印：從齒輪到自己設計零件 | https://book.vichuang.tw/mech/ |
| `statistics/` | 從資料看世界：零基礎統計學 | https://book.vichuang.tw/statistics/ |
| `economics/` | 生活經濟學：從零用錢看懂世界怎麼運作 | https://book.vichuang.tw/economics/ |
| `accounting/` | 看懂錢的流向：零基礎會計入門 | https://book.vichuang.tw/accounting/ |
| `math/` | 數學這樣想：從國小到國中的數學思考課 | https://book.vichuang.tw/math/ |
| `math2/` | 數學這樣想（進階）：從函數、三角到微積分 | https://book.vichuang.tw/math2/ |
| `english/` | 英文自學地圖：國中生的英文學習法與練習本 | https://book.vichuang.tw/english/ |

## 本機預覽

```bash
brew install mdbook          # 只要裝一次
./build.sh serve electric    # 邊改邊看，存檔自動重新整理
./build.sh                   # 建置整個書架到 _site/
./build.sh merge electric    # 把一本書合併成單一 electric/全書.md
```

## 修改內容

- 章節原始檔在 `electric/src/`，一章一個 Markdown 檔，目錄順序由 `electric/src/SUMMARY.md` 決定。
- 圖片放 `electric/src/images/`，用法見該資料夾的 README。
- 共用寫作規範在根目錄 `STYLE_GUIDE.md`，每本書的大綱在各自的 `OUTLINE.md`（電學書另有自己的 `electric/STYLE_GUIDE.md` 與接線圖工具 `tools/bbdraw.py`、`tools/DIAGRAM_GUIDE.md`）。
- 改完 `git commit` 並 `git push`，約 1–2 分鐘後網站更新。

## 加一本新書

1. `mdbook init physics`（資料夾名稱就是網址路徑）。
2. 在 `physics/book.toml` 的 `[output.html]` 加上 `site-url = "/physics/"`。
3. 在根目錄 `index.html` 的書架加一個連結。
4. 推上 `main`。

## 部署

`.github/workflows/deploy.yml` 會在每次推送時安裝 mdBook、執行 `./build.sh`，把 `_site/` 發布到 GitHub Pages。自訂網域由根目錄的 `CNAME` 檔與 Route 53 的 `book CNAME encounternow.github.io` 紀錄決定。
