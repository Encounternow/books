# 書架　book.vichuang.tw

給國小高年級、國中生與零經驗大人的自學實作教材，每本書一個資料夾，用 [mdBook](https://rust-lang.github.io/mdBook/) 編成網頁，推上 `main` 就會自動發布到 https://book.vichuang.tw/ 。

| 資料夾 | 書名 | 網址 |
|---|---|---|
| `electric/` | 動手玩電：給國中生的電學、電子學與電路學實作課 | https://book.vichuang.tw/electric/ |

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
- 寫作規範與全書大綱在 `electric/STYLE_GUIDE.md`、`electric/OUTLINE.md`，擴寫新章節時請遵守。
- 改完 `git commit` 並 `git push`，約 1–2 分鐘後網站更新。

## 加一本新書

1. `mdbook init physics`（資料夾名稱就是網址路徑）。
2. 在 `physics/book.toml` 的 `[output.html]` 加上 `site-url = "/physics/"`。
3. 在根目錄 `index.html` 的書架加一個連結。
4. 推上 `main`。

## 部署

`.github/workflows/deploy.yml` 會在每次推送時安裝 mdBook、執行 `./build.sh`，把 `_site/` 發布到 GitHub Pages。自訂網域由根目錄的 `CNAME` 檔與 Route 53 的 `book CNAME encounternow.github.io` 紀錄決定。
