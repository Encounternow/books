# 《AI 工程實作：從 Skill、MCP 到 RAG、LoRA 與自架模型》全書大綱

共用規範：/Users/vichuang/Codes/electric-course/STYLE_GUIDE.md。檔名 `src/NN-章名.md`。
讀者：會一點 Python（讀過《AI 怎麼運作》或有基本程式經驗）的國中生到大人，想把 AI 接進自己的工具與專案。語氣仍照共用規範（親切、先直覺再細節），但這本書是技術實作書，程式是主角。
**工具與寫法規則（所有作者必守）**：
- 語言一律 Python 3.10+，在本機終端機或 Google Colab 執行；環境用 `python -m venv` + `pip`。
- 呼叫 Claude 一律用官方 `anthropic` SDK（不用 OpenAI 相容層、不用 requests 自己拼），模型用 `claude-opus-5-5`；要加 thinking 時用 `thinking={"type": "adaptive"}`；需要 JSON 結果用結構化輸出 `output_config={"format": {...}}` 或 `client.messages.parse()`；工具迴圈用 `@beta_tool` + `client.beta.messages.tool_runner()` 或自己寫 `while stop_reason == "tool_use"` 迴圈；長輸出用 `client.messages.stream()`。**作者寫任何 Anthropic SDK 程式前必須先用 Skill 工具載入 `claude-api` 並讀它的 python/claude-api/README.md 與 tool-use.md，照裡面的寫法，不憑記憶。**
- 本地模型一律用 Ollama（`ollama run`、`ollama pull`，Python 用 `ollama` 套件或 OpenAI 相容端點只在 Ollama 章節提及），示範模型用小型開源模型（例如 Qwen 系列小參數版、Llama 小參數版、Gemma 小參數版），只寫「例如」不保證特定版本存在。
- MCP 用官方 Python SDK `mcp`（`from mcp.server.fastmcp import FastMCP`）；接到 Claude Code 用 `claude mcp add`，接到 Claude Desktop 用設定檔 `claude_desktop_config.json`；API 端用 `mcp_servers` + `mcp_toolset` 工具。
- Skill 有兩種要分清楚：(1) Claude Code 的 Skill：資料夾裡的 `SKILL.md`（frontmatter 有 name、description），放在 `.claude/skills/<name>/`，用 `/<name>` 或自動觸發；(2) Claude API 的 Agent Skills（`client.skills`，搭配 code execution）。本書以 (1) 為主、(2) 一節帶過。
- RAG：嵌入用本地模型（Ollama 的 embedding 模型，例如 nomic-embed-text）或 sentence-transformers；向量庫用 chromadb；要講切塊、檢索、重排、評估。
- LoRA：用 Hugging Face `transformers` + `peft` + `datasets`，在 Colab 免費 GPU 上微調一個小模型（幾百 MB 等級）；本機驗證時用極小模型（例如 sshleifer/tiny-gpt2）跑幾步確認程式無誤。
- **每段程式都要完整可執行、每 2–3 行中文註解、作者必須實際用 python3 跑過**。需要 API 金鑰的程式：先用 `ant auth status` 或環境變數 `ANTHROPIC_API_KEY` 檢查；若本機沒有金鑰，至少要 `python -c "import ..."` 驗證匯入與建構物件無誤，並在書中把輸出標為「預期輸出」。需要下載模型或資料的程式，本機能跑就跑，不能跑要寫明原因與 Colab 上的預期結果。
- 套件版本變動快：書裡寫 `pip install anthropic mcp chromadb ...` 不釘死版本，但在附錄 B 記錄作者驗證時的版本。
- 安全：API 金鑰放環境變數不進程式碼與 git；MCP server 給的工具要最小權限；prompt injection 的風險與防法要講；自架服務不要開到公網沒驗證。
- 可連結《AI 怎麼用》 https://book.vichuang.tw/ai-use/ 、《AI 怎麼運作》 https://book.vichuang.tw/ai-theory/ 、《動手玩電》 https://book.vichuang.tw/electric/ 。

## 第一部　初階：把現成的 AI 接進你的工具

- 00-前言.md：給誰的、需要會什麼（Python 基礎、終端機）、兩部的關係、環境安裝（Python、venv、VS Code、Claude Code 或 Claude Desktop、Ollama、Anthropic API 金鑰怎麼拿與保管）、全書地圖、安全三原則。
- 01-用程式呼叫AI.md：API 是什麼、安裝 anthropic SDK、第一次呼叫、system prompt、多輪對話的 messages 結構、串流輸出、temperature 與 max_tokens、thinking 的用法、錯誤處理與重試、金鑰管理、費用與 token 計算。活動：做一個命令列聊天機器人；做一個「把文章變三句摘要」小工具。
- 02-結構化輸出與工具使用.md：讓 AI 回 JSON（結構化輸出與 pydantic）、工具（function calling）的概念與定義、tool_use → 執行 → tool_result 的迴圈、tool_runner 自動迴圈、並行工具、安全（工具要驗證輸入）。活動：做一個會查天氣（假資料）與算數的小助理；把第 1 章的摘要工具改成輸出 JSON。
- 03-Skill.md：什麼是 Skill（給 AI 的操作手冊）、Claude Code 的 SKILL.md 格式（frontmatter、觸發描述、步驟、附檔）、寫一個自己的 Skill（例如「寫實驗報告」或「檢查 Arduino 程式」）、slash command、怎麼讓 Skill 可靠（明確觸發條件、不要太長）、API 端的 Agent Skills 一節帶過。活動：寫一個 Skill 並在 Claude Code 觸發；為家裡的筆記規則寫一個 Skill。
- 04-MCP入門.md：Model Context Protocol 是什麼（USB-C 比喻）、server／client／tools／resources／prompts、現成的 MCP server（檔案系統、GitHub、資料庫類，只寫類型不寫可能失效的名稱）、在 Claude Code 用 `claude mcp add` 安裝、在 Claude Desktop 用設定檔、怎麼看它呼叫了什麼、安全（只給需要的資料夾、看清楚權限）。活動：裝一個檔案系統 MCP 讓 AI 整理你的資料夾；用 MCP 讀一個 SQLite 資料庫回答問題。
- 05-代理與工作流程.md：Agent 是什麼（會自己決定下一步並用工具的迴圈）、ReAct 直覺、Claude Code 的用法與 CLAUDE.md、記憶與上下文管理、子代理、什麼時候用 agent 什麼時候用單次呼叫、成本與失控的防範。活動：用 Claude Code 完成一個小專案並寫 CLAUDE.md；用 SDK 寫一個會自己查資料再回答的小 agent（用第 2 章的工具迴圈）。
- 06-提示工程與評估.md：system prompt 設計、few-shot、分步驟、輸出格式、提示版本管理、建立評估集（evals）與自動評分、用 AI 當評審、A/B 比較、提示快取（prompt caching）降成本。活動：為第 1 章摘要工具建 20 題評估集並改提示看分數；量測快取前後的費用。

## 第二部　進階：自己做 RAG、本地模型、微調與自架 MCP

- 07-嵌入與向量搜尋.md：嵌入（embedding）是什麼、餘弦相似度、向量資料庫（chromadb）、建立索引與查詢、中文的注意事項。活動：把自己的 50 條筆記做成可搜尋的向量庫；比較關鍵字搜尋與向量搜尋。
- 08-RAG實作.md：RAG 流程（切塊 → 嵌入 → 檢索 → 組提示 → 生成）、切塊策略與大小、檢索幾筆、重排（rerank）概念、引用來源、評估（答對率、有沒有亂講）、常見失敗（切壞、檢索不到、上下文塞爆）。活動：做一個「問我的筆記」問答機器人（本地 Ollama 或 Claude 擇一，兩種都給程式）；做一個 RAG 評估表。
- 09-本地模型與Ollama.md：為什麼要本地模型（隱私、離線、免費）、安裝 Ollama、拉模型、硬體需求與量化（GGUF、Q4 是什麼）、用 Python 呼叫、本地模型與 Claude 的差異與選擇、用本地模型跑第 8 章 RAG。活動：比較三個不同大小的本地模型回答同一組問題的品質與速度。
- 10-微調一資料與選擇.md：微調是什麼、什麼時候用微調 vs RAG vs 提示（決策表）、資料集格式（指令／回應對）、資料品質比數量重要、合成資料與去重、訓練／驗證切分、授權與隱私。活動：整理一份 200 筆「用我的語氣回覆」的資料集；寫資料清洗腳本。
- 11-微調二LoRA實作.md：全參數微調為什麼貴、LoRA 的直覺（只訓練一小塊「補丁」）、rank 與 alpha 的意思、用 transformers + peft 在 Colab 微調小模型、評估前後差異、合併與匯出、轉成 GGUF 給 Ollama 用（概念與指令）。活動：微調一個小模型學會固定格式回覆；比較微調前後的輸出。
- 12-從零訓練小模型.md：延續《AI 怎麼運作》，用 PyTorch 寫一個迷你字元級 Transformer（nanoGPT 風格、幾百行內）在 Colab 訓練一段文字，看 loss 下降與產生文字；參數量、資料量、算力的關係；為什麼大模型要那麼多資源。活動：用自己的文字訓練並調整層數與訓練步數。
- 13-自架MCP伺服器.md：用 `mcp` SDK 的 FastMCP 寫一個 server（工具：查家裡的 SQLite、讀感測器數據、算東西）、resources 與 prompts、stdio 與 HTTP 傳輸、接到 Claude Code 與 Claude Desktop、在 API 端用 mcp_servers 連接、測試與除錯（MCP Inspector 概念）、安全（驗證輸入、最小權限、不要暴露在公網）。活動：寫一個「家庭資料 MCP」；寫一個控制 ESP32 燈的 MCP（透過 HTTP 呼叫《動手玩電》第 16 章的網頁伺服器）。
- 14-組裝與部署.md：把 RAG + 工具 + 模型組成一個應用（FastAPI 後端 + 簡單網頁）、設定與金鑰管理、日誌與監控、成本估算、prompt injection 與資料外洩防範、部署到自己的電腦／樹莓派／雲端的選擇（概念）。活動：把第 8 章的問答機器人做成可以用瀏覽器問的小網站。
- 15-專題.md：四個專題：(1) 家庭筆記問答機器人（RAG + 本地模型 + 網頁）；(2) 自架 MCP 控制家裡裝置（ESP32）並在 Claude Code 裡用自然語言開關燈；(3) LoRA 微調「用我的語氣」小模型並接進聊天介面；(4) 一套 Skill + MCP 的 Claude Code 工作流（例如「自動整理實驗數據並寫報告」）。附專題報告格式。
- appendix-A.md：環境安裝速查（Python、venv、VS Code、Claude Code、Claude Desktop、Ollama、Colab GPU；Windows／macOS 差異）。
- appendix-B.md：程式索引與驗證版本（每章程式做什麼、需要的套件、作者驗證時的套件版本與日期）。
- appendix-C.md：安全與成本檢查表（金鑰、權限、prompt injection、費用上限、本地 vs 雲端選擇）。
- appendix-D.md：名詞對照表（中英，至少 150 條）。
