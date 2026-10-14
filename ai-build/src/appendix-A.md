# 附錄 A　環境安裝速查

這一頁是「照著打」用的。每一節先列 macOS 再列 Windows，指令前面的 `$` 不用打。全書驗證環境：macOS（Apple Silicon）、Python 3.13.7；Windows 的差異另外標。

## A.1　Python 與 venv

**macOS**

```bash
# 用 Homebrew 裝（沒有 Homebrew 先到 https://brew.sh 照指令裝）
brew install python
python3 --version          # 要 3.10 以上

# 每本書、每個專案各建一個 venv（虛擬環境），套件互不干擾
cd 你的專案資料夾
python3 -m venv venv
source venv/bin/activate   # 提示字元前面會出現 (venv)
pip install --upgrade pip
```

**Windows**

1. 到 https://www.python.org/downloads/ 下載安裝檔，**勾選「Add python.exe to PATH」**再按 Install。
2. 開「終端機」或「PowerShell」：

```powershell
python --version
cd 你的專案資料夾
python -m venv venv
venv\Scripts\activate      # 若出現「無法載入指令碼」，先執行 Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
pip install --upgrade pip
```

**共同**

- 關掉 venv：`deactivate`。
- 看裝了什麼：`pip list`。
- 把目前版本記下來：`pip freeze > requirements.txt`；別人重建：`pip install -r requirements.txt`。
- 書裡所有 `python xxx.py` 都假設 venv 已經啟動。看到 `ModuleNotFoundError` 第一件事：確認提示字元前有 `(venv)`。

## A.2　VS Code

1. 到 https://code.visualstudio.com 下載安裝。
2. 裝擴充套件：左側方塊圖示 → 搜尋 `Python`（Microsoft 出的）→ Install。
3. 開專案資料夾：File → Open Folder。
4. 選直譯器：`Ctrl/⌘ + Shift + P` → 「Python: Select Interpreter」→ 選 `./venv/bin/python`（Windows 是 `.\venv\Scripts\python.exe`）。
5. 內建終端機：`` Ctrl + ` ``。它會自動啟動 venv。

## A.3　Claude Code

需要 Node.js 18 以上（到 https://nodejs.org 裝 LTS 版）。

```bash
npm install -g @anthropic-ai/claude-code
claude --version           # 作者驗證時 2.1.299
cd 你的專案資料夾
claude                     # 第一次會引導登入
```

常用指令（都不用進互動模式）：

```bash
claude mcp add <name> -- <command> [args]        # 加 stdio MCP 伺服器
claude mcp add --transport http <name> <url>     # 加 HTTP MCP 伺服器
claude mcp add <name> -e KEY=value -- <command>  # 傳環境變數
claude mcp add -s project <name> -- ...          # 存到專案的 .mcp.json
claude mcp list                                  # 看狀態
claude mcp get <name> / claude mcp remove <name>
```

Skill 放在專案的 `.claude/skills/<name>/SKILL.md`（第 3 章），CLAUDE.md 放專案根目錄（第 5 章）。

**Windows**：建議在 WSL（Windows Subsystem for Linux）裡裝，指令和 macOS 一樣；原生 PowerShell 也可以，但 MCP 伺服器的路徑要用 Windows 格式。

## A.4　Claude Desktop

1. 到 https://claude.ai/download 下載、安裝、登入。
2. MCP 設定檔位置：
   - macOS：`~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows：`%APPDATA%\Claude\claude_desktop_config.json`
3. 檔案不存在就自己建，內容見第 13 章。`command` 要用 venv 裡 python 的**絕對路徑**。
4. 改完要**完全關閉**（macOS 是 ⌘Q，不是關視窗）再開。

## A.5　Anthropic API 金鑰

1. 到 https://console.anthropic.com 註冊、建立 API key，複製（只會顯示一次）。
2. 設成環境變數，不要寫進程式：

**macOS**（寫進 `~/.zshrc` 永久生效）

```bash
echo 'export ANTHROPIC_API_KEY=sk-ant-...' >> ~/.zshrc
source ~/.zshrc
```

**Windows PowerShell**（永久）

```powershell
[System.Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "sk-ant-...", "User")
# 重開終端機才生效
```

3. 驗證：`python -c "import anthropic; print(anthropic.Anthropic().models.list().data[0].id)"`。
4. 在主控台設**每月費用上限**（Settings → Limits），這比任何程式裡的保護都重要。
5. 另一種登入方式：裝了 `ant` CLI 後 `ant auth login`，SDK 會自動用登入的帳號，不用設環境變數。

## A.6　Ollama

**macOS**：到 https://ollama.com/download 下載安裝，或 `brew install ollama`。
**Windows**：同網站下載安裝檔。

```bash
ollama --version
ollama pull nomic-embed-text        # 第 7、8 章的嵌入模型（約 270 MB）
ollama pull qwen2.5:1.5b            # 例子：一個小的聊天模型；用 ollama list 看實際名稱
ollama run qwen2.5:1.5b             # 試聊，/bye 離開
ollama list                         # 看有哪些
pip install ollama                  # Python 套件
```

硬體：8 GB 記憶體跑 1.5B 到 3B 的模型，16 GB 跑 7B 到 8B（Q4 量化）。沒有 GPU 會慢但能跑。

## A.7　Google Colab GPU

1. https://colab.research.google.com ，新增筆記本。
2. 執行階段 → 變更執行階段類型 → 硬體加速器選 **T4 GPU** → 儲存。
3. 第一格：`!nvidia-smi` 看到顯示卡資訊就對了。
4. 裝套件：`!pip install -q transformers peft datasets accelerate`。
5. 免費版限制：閒置約 90 分鐘斷線、每天 GPU 時數有限、檔案斷線後清空。要保留訓練結果：`from google.colab import drive; drive.mount('/content/drive')` 再把輸出資料夾存到 `/content/drive/MyDrive/`。
6. 書裡的程式本機和 Colab 都能跑；Colab 上把 `pip install` 改成 `!pip install`，環境變數用 `import os; os.environ["MODEL"] = "..."` 設在程式最前面。

## A.8　本書用到的套件一覽

```bash
pip install anthropic                      # 第 1–6、13、14 章
pip install "anthropic[mcp]"               # 第 13 章 local_mcp_agent.py
pip install mcp requests                   # 第 4、13、15 章
pip install chromadb ollama sentence-transformers   # 第 7、8、9、15 章
pip install torch transformers peft datasets accelerate   # 第 11、12 章
pip install fastapi uvicorn                # 第 14、15 章
```

版本不釘死；作者驗證時的版本見附錄 B。

## A.9　Windows 與 macOS 差異速查

| 項目 | macOS | Windows |
|---|---|---|
| 啟動 venv | `source venv/bin/activate` | `venv\Scripts\activate` |
| venv 的 python 路徑 | `venv/bin/python` | `venv\Scripts\python.exe` |
| 環境變數（一次性） | `KEY=value python x.py` | `$env:KEY="value"; python x.py` |
| 路徑分隔 | `/` | `\`（Python 裡用 `/` 也行） |
| curl | 內建 | Windows 10 以上內建；PowerShell 裡 `curl` 是別名，用 `curl.exe` |
| 殺掉占埠的程式 | `pkill -f uvicorn` | `Get-Process -Name python \| Stop-Process` |
| Claude Desktop 設定檔 | `~/Library/Application Support/Claude/` | `%APPDATA%\Claude\` |
