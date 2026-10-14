# 附錄 D　名詞對照表

全書出現過的名詞，按主題分組，每一條都是「中文｜英文｜一句話解釋」。找某個詞用瀏覽器的搜尋（Ctrl + F／⌘ + F）最快。

## D.1　API 與基本呼叫（第 0–1 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 1 | 應用程式介面 | API, Application Programming Interface | 程式和程式之間約定好的呼叫方式。 |
| 2 | 軟體開發套件 | SDK, Software Development Kit | 幫你把 API 包成好用函式的套件，本書用 `anthropic`。 |
| 3 | API 金鑰 | API Key | 證明「是你在呼叫」的一串祕密字元。 |
| 4 | 環境變數 | Environment Variable | 程式外部設定的鍵值，放金鑰與設定。 |
| 5 | 虛擬環境 | venv, Virtual Environment | 每個專案獨立的 Python 套件空間。 |
| 6 | 終端機 | Terminal | 打指令的文字介面。 |
| 7 | 模型 | Model | 回答你的那個 AI，用名稱指定，例如 claude-opus-5-5。 |
| 8 | 訊息 | Message | 對話裡的一則，有 role（user／assistant）與 content。 |
| 9 | 系統提示 | System Prompt | 給模型的背景指示，放在 system 參數。 |
| 10 | 使用者 | user | 訊息的角色之一：人說的話。 |
| 11 | 助理 | assistant | 訊息的角色之一：模型說的話。 |
| 12 | 多輪對話 | Multi-turn Conversation | 把整段歷史每次都送回去，模型才「記得」。 |
| 13 | 權杖 | Token | 模型處理文字的最小單位，約半個到一個中文字。 |
| 14 | 最大輸出 | max_tokens | 一次回答最多幾個 token。 |
| 15 | 溫度 | Temperature | 抽字的隨機程度，低穩定、高多變。 |
| 16 | 串流 | Streaming | 一邊生成一邊傳回，不用等全部完成。 |
| 17 | 思考 | Thinking | 模型回答前先推理；本書用 adaptive 模式。 |
| 18 | 努力程度 | Effort | 控制思考深度與 token 用量的設定（low 到 max）。 |
| 19 | 停止原因 | stop_reason | 模型為什麼停：end_turn、max_tokens、tool_use、refusal。 |
| 20 | 用量 | usage | 回應裡的 token 計數，用來算費用。 |
| 21 | 速率限制 | Rate Limit | 一段時間內最多呼叫幾次，超過回 429。 |
| 22 | 重試 | Retry | 失敗後再試一次，通常加等待。 |
| 23 | 逾時 | Timeout | 等待回應的最長時間。 |
| 24 | 內容區塊 | Content Block | 回應內容的一段，有 text、thinking、tool_use 等型別。 |

## D.2　結構化輸出與工具使用（第 2 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 25 | 結構化輸出 | Structured Output | 要求模型回傳符合固定格式（JSON Schema）的結果。 |
| 26 | JSON | JSON | 程式間交換資料的文字格式。 |
| 27 | JSON Schema | JSON Schema | 描述 JSON 格式的標準。 |
| 28 | pydantic | pydantic | 用 Python 類別定義與驗證資料格式的套件。 |
| 29 | 工具 | Tool | 模型可以要求呼叫的函式，有名稱、說明、參數格式。 |
| 30 | 函式呼叫 | Function Calling | 工具使用的另一個名字。 |
| 31 | 工具使用 | tool_use | 模型回應裡「我要呼叫某工具」的區塊。 |
| 32 | 工具結果 | tool_result | 你執行完工具後回給模型的區塊，要帶 tool_use_id。 |
| 33 | 工具迴圈 | Tool Loop | 呼叫→執行→回傳→再呼叫，直到模型不再要工具。 |
| 34 | 工具執行器 | Tool Runner | SDK 幫你跑工具迴圈的功能（`@beta_tool` + `tool_runner`）。 |
| 35 | 並行工具呼叫 | Parallel Tool Use | 模型一次要求呼叫多個工具，結果要一起回。 |
| 36 | 嚴格模式 | strict | 工具參數保證完全符合 schema。 |
| 37 | 工具選擇 | tool_choice | 讓模型自由決定（auto）或不用工具（none）。 |

## D.3　Skill（第 3 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 38 | 技能 | Skill | 給 AI 的操作手冊：什麼時候做、怎麼做。 |
| 39 | SKILL.md | SKILL.md | Claude Code 的 Skill 檔案，放 `.claude/skills/<name>/`。 |
| 40 | 前言區 | Frontmatter | SKILL.md 開頭 `---` 包起來的 name 與 description。 |
| 41 | 觸發描述 | Trigger Description | description 欄位，決定什麼話會啟用這個 Skill。 |
| 42 | 斜線指令 | Slash Command | 在 Claude Code 打 `/<name>` 手動啟用。 |
| 43 | 代理技能 | Agent Skills | API 端的 Skill（`client.skills`），搭配程式執行。 |
| 44 | CLAUDE.md | CLAUDE.md | 專案根目錄的說明檔，Claude Code 每次都會讀。 |

## D.4　MCP（第 4、13 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 45 | 模型上下文協定 | MCP, Model Context Protocol | AI 與外部工具、資料之間的通用接頭。 |
| 46 | MCP 伺服器 | MCP Server | 提供工具、資源、提示的程式。 |
| 47 | MCP 客戶端 | MCP Client | 連到伺服器呼叫工具的一方。 |
| 48 | 資源 | Resource | 伺服器提供的唯讀資料，用 URI 標示。 |
| 49 | 提示 | Prompt | 伺服器提供的提示詞範本。 |
| 50 | MCPServer／FastMCP | MCPServer / FastMCP | 官方 Python SDK 的高階伺服器類別（2.x／1.x 名稱）。 |
| 51 | 裝飾器 | Decorator | `@mcp.tool()` 這種把函式登記成工具的語法。 |
| 52 | 文件字串 | Docstring | 函式開頭的說明文字，MCP 拿它當工具說明。 |
| 53 | 型別提示 | Type Hint | `voltage: float` 這種標註，MCP 拿它產生參數格式。 |
| 54 | 標準輸入輸出傳輸 | stdio transport | 用子程序的 stdin／stdout 傳 JSON。 |
| 55 | 串流 HTTP 傳輸 | Streamable HTTP transport | 用 HTTP 與 SSE 傳，網址結尾 /mcp。 |
| 56 | 伺服器推送事件 | SSE, Server-Sent Events | 伺服器持續推資料給瀏覽器或 client 的 HTTP 機制。 |
| 57 | 握手 | initialize | 連線後交換版本與能力的第一步。 |
| 58 | 工具錯誤 | ToolError | mcp 2.x 工具回報錯誤的例外，訊息會傳給 client。 |
| 59 | claude mcp add | claude mcp add | Claude Code 加 MCP 伺服器的指令。 |
| 60 | 設定範圍 | Scope | `-s local／user／project`，設定存在哪。 |
| 61 | .mcp.json | .mcp.json | 專案層級的 MCP 設定檔，可進 git。 |
| 62 | claude_desktop_config.json | claude_desktop_config.json | Claude Desktop 的 MCP 設定檔。 |
| 63 | MCP connector | MCP connector | API 端用 mcp_servers 連遠端 MCP 伺服器。 |
| 64 | mcp_toolset | mcp_toolset | tools 參數裡指定用哪個 MCP 伺服器的工具。 |
| 65 | MCP Inspector | MCP Inspector | 官方圖形化除錯工具。 |
| 66 | 最小權限 | Least Privilege | 只給完成任務所需的最少能力。 |
| 67 | 參數化查詢 | Parameterized Query | SQL 用 ? 佔位，防 SQL injection。 |
| 68 | SQL 注入 | SQL Injection | 把惡意字串拼進 SQL。 |

## D.5　代理與提示工程（第 5、6 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 69 | 代理 | Agent | 會自己決定下一步、呼叫工具、直到完成的迴圈。 |
| 70 | ReAct | ReAct | 「想一下→做一步→看結果」交替的代理模式。 |
| 71 | 子代理 | Subagent | 代理派出去做一部分工作的另一個代理。 |
| 72 | 上下文 | Context | 模型這一次看得到的全部文字。 |
| 73 | 上下文視窗 | Context Window | 模型一次最多能看的 token 數。 |
| 74 | 記憶 | Memory | 跨對話保留資訊的機制（檔案、資料庫、摘要）。 |
| 75 | 壓縮 | Compaction | 把過長的歷史摘要掉以節省上下文。 |
| 76 | 提示工程 | Prompt Engineering | 設計提示讓模型表現更好。 |
| 77 | 少量範例 | Few-shot | 在提示裡給幾個例子。 |
| 78 | 零範例 | Zero-shot | 不給例子直接問。 |
| 79 | 分步驟 | Step-by-step | 要求模型一步一步來。 |
| 80 | 評估集 | Eval Set | 固定的一組題目與標準答案，用來量分數。 |
| 81 | AI 評審 | LLM-as-Judge | 用另一個模型幫回答打分。 |
| 82 | A/B 比較 | A/B Test | 兩個版本各跑一遍比分數。 |
| 83 | 提示快取 | Prompt Caching | 固定前綴只算一次，之後便宜很多。 |
| 84 | 快取命中 | Cache Hit | 這次請求用到了快取，看 cache_read_input_tokens。 |
| 85 | 提示版本 | Prompt Versioning | 把提示當程式碼管理，改了要記錄。 |

## D.6　嵌入與 RAG（第 7、8 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 86 | 嵌入 | Embedding | 把文字變成一串數字（向量），意思相近的向量相近。 |
| 87 | 向量 | Vector | 一串數字，例如 768 維。 |
| 88 | 餘弦相似度 | Cosine Similarity | 兩個向量方向有多接近，1 最像。 |
| 89 | 向量資料庫 | Vector Database | 存向量、做相似搜尋的資料庫，本書用 chromadb。 |
| 90 | 集合 | Collection | chromadb 裡一組向量與文件的容器。 |
| 91 | 索引 | Index | 建好可以快速搜尋的資料結構。 |
| 92 | 檢索增強生成 | RAG, Retrieval-Augmented Generation | 先找相關資料，再把資料和問題一起交給模型。 |
| 93 | 切塊 | Chunking | 把長文件切成小段再嵌入。 |
| 94 | 塊 | Chunk | 切出來的一段。 |
| 95 | 重疊 | Overlap | 相鄰塊共用的一小段，避免句子被切斷。 |
| 96 | 檢索 | Retrieval | 依問題找出最相關的幾塊。 |
| 97 | 前 k 筆 | Top-k | 檢索取相似度最高的 k 筆。 |
| 98 | 重排 | Rerank | 用更精細的模型把檢索結果重新排序。 |
| 99 | 引用來源 | Citation | 回答時標出用了哪一塊。 |
| 100 | 幻覺 | Hallucination | 模型講得很像真的但其實是編的。 |
| 101 | 答對率 | Accuracy | 評估集裡答對的比例。 |
| 102 | 關鍵字搜尋 | Keyword Search | 比對字面是否出現，和向量搜尋互補。 |
| 103 | 句子轉換器 | sentence-transformers | 本地跑嵌入模型的套件。 |
| 104 | nomic-embed-text | nomic-embed-text | Ollama 上常用的嵌入模型之一。 |

## D.7　本地模型與 Ollama（第 9 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 105 | 本地模型 | Local Model | 在自己電腦上跑的模型，不連網、不付費。 |
| 106 | Ollama | Ollama | 在本機下載與執行開源模型的工具。 |
| 107 | 拉取 | ollama pull | 下載模型。 |
| 108 | 開源模型 | Open-weight Model | 權重公開可下載的模型，例如 Qwen、Llama、Gemma 系列。 |
| 109 | 參數量 | Parameter Count | 模型有幾個可調數字，0.5B = 5 億。 |
| 110 | 量化 | Quantization | 把參數從 32 位元縮成 8 或 4 位元，檔案小、跑得快、品質略降。 |
| 111 | Q4／Q8 | Q4 / Q8 | 4 位元／8 位元量化。 |
| 112 | GGUF | GGUF | llama.cpp 與 Ollama 用的單檔模型格式。 |
| 113 | llama.cpp | llama.cpp | 在 CPU／GPU 上高效跑模型的開源程式，Ollama 的底層。 |
| 114 | Modelfile | Modelfile | 告訴 Ollama 用哪個 GGUF 與設定的檔案。 |
| 115 | 顯示記憶體 | VRAM | 顯示卡上的記憶體，決定能跑多大的模型。 |
| 116 | OpenAI 相容端點 | OpenAI-compatible Endpoint | Ollama 提供的另一種呼叫介面，本書只在第 9 章提及。 |

## D.8　微調（第 10、11 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 117 | 微調 | Fine-tuning | 用自己的資料繼續訓練現成模型。 |
| 118 | 全參數微調 | Full Fine-tuning | 所有參數都訓練，最貴。 |
| 119 | 低秩適應 | LoRA, Low-Rank Adaptation | 凍結原權重，只訓練旁邊兩個小矩陣。 |
| 120 | 秩 | Rank, r | LoRA 補丁的厚度。 |
| 121 | alpha | LoRA alpha | 補丁輸出的縮放倍率（alpha ÷ r）。 |
| 122 | 目標模組 | target_modules | 要貼補丁的層。 |
| 123 | 補丁檔 | Adapter | LoRA 存出來的小檔案。 |
| 124 | 合併 | merge_and_unload | 把補丁加回原權重。 |
| 125 | 凍結 | Freeze | 參數不參與訓練。 |
| 126 | 指令／回應對 | Instruction / Response Pair | 微調資料的基本單位。 |
| 127 | 合成資料 | Synthetic Data | 用模型產生的訓練資料。 |
| 128 | 去重 | Deduplication | 移除重複或幾乎重複的資料。 |
| 129 | 訓練／驗證切分 | Train / Validation Split | 留一部分資料不訓練，用來測有沒有背起來。 |
| 130 | 學習率 | Learning Rate | 每一步調整參數的幅度。 |
| 131 | 批次 | Batch | 一次餵進模型的幾筆資料。 |
| 132 | 訓練步 | Step | 用一個批次更新一次參數。 |
| 133 | 週期 | Epoch | 整份資料看過一遍。 |
| 134 | 損失 | Loss | 模型猜得有多差的數字，越低越好。 |
| 135 | 優化器 | Optimizer | 決定怎麼用梯度更新參數的演算法，本書用 AdamW。 |
| 136 | 梯度 | Gradient | 損失對每個參數的斜率，告訴它往哪調。 |
| 137 | 結束符號 | EOS, End of Sequence | 告訴模型「講完了」的特殊 token。 |
| 138 | 填充 | Padding | 把長短不一的序列補到一樣長。 |
| 139 | 標籤 | Labels | 訓練時要預測的目標。 |
| 140 | 分詞器 | Tokenizer | 把文字切成 token 並編號的工具。 |
| 141 | transformers | transformers | Hugging Face 的模型載入與訓練套件。 |
| 142 | peft | peft | Hugging Face 的 LoRA 等「參數高效微調」套件。 |
| 143 | datasets | datasets | Hugging Face 的資料集處理套件。 |
| 144 | Trainer | Trainer | transformers 裡包好訓練迴圈的類別。 |
| 145 | 煙霧測試 | Smoke Test | 用極小設定先跑一遍確認程式不會當掉。 |
| 146 | 過擬合 | Overfitting | 把訓練資料背起來，對新資料沒用。 |

## D.9　從零訓練（第 12 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 147 | Transformer | Transformer | 現代語言模型的基本架構，核心是注意力。 |
| 148 | 字元級 | Character-level | 一個字當一個 token。 |
| 149 | 字彙表 | Vocabulary | 模型認得的 token 清單。 |
| 150 | 位置編碼 | Positional Encoding | 告訴模型每個 token 是第幾個。 |
| 151 | 注意力 | Attention | 每個字看前面的字、決定誰重要的機制。 |
| 152 | 查詢／鑰匙／價值 | Query / Key / Value | 注意力的三個向量。 |
| 153 | 遮罩 | Mask | 讓模型不能看未來的字。 |
| 154 | 多頭注意力 | Multi-head Attention | 幾組注意力並排各看各的。 |
| 155 | 前饋網路 | Feed-forward Network | 每個位置各自過的兩層小網路。 |
| 156 | 殘差連接 | Residual Connection | 輸入加回輸出，深層才訓練得動。 |
| 157 | 層正規化 | LayerNorm | 把向量拉回合理範圍。 |
| 158 | softmax | softmax | 把一排分數變成加總為 1 的機率。 |
| 159 | 交叉熵 | Cross Entropy | 損失函數：−log(正確答案的機率)。 |
| 160 | 上下文長度 | Context Length / block_size | 模型一次能看的 token 數。 |
| 161 | 算力 | Compute | 訓練要做的運算次數，約 6 × 參數量 × token 數。 |
| 162 | PyTorch | PyTorch | 本書寫模型用的深度學習框架。 |
| 163 | nanoGPT | nanoGPT | 一個極簡 GPT 實作，第 12 章的風格來源。 |

## D.10　組裝、部署與安全（第 14 章、附錄 C）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 164 | 後端 | Backend | 伺服器上處理請求的程式。 |
| 165 | 前端 | Frontend | 瀏覽器裡的網頁。 |
| 166 | FastAPI | FastAPI | Python 寫網頁 API 的框架。 |
| 167 | uvicorn | uvicorn | 執行 FastAPI 的伺服器程式。 |
| 168 | 端點 | Endpoint | 一個路徑加方法，例如 POST /ask。 |
| 169 | 路由 | Route | 網址對應到函式的設定。 |
| 170 | HTTP 狀態碼 | HTTP Status Code | 200 成功、400 輸入錯、422 格式錯、429 太頻繁、502 後端失敗。 |
| 171 | curl | curl | 命令列 HTTP 工具。 |
| 172 | 日誌 | Log | 程式執行的紀錄檔。 |
| 173 | 監控 | Monitoring | 持續看日誌或指標。 |
| 174 | 提示注入 | Prompt Injection | 把指令藏在資料裡騙模型。 |
| 175 | 直接注入 | Direct Injection | 使用者自己下惡意指令。 |
| 176 | 間接注入 | Indirect Injection | 指令藏在模型讀到的文件或工具結果裡。 |
| 177 | 資料外洩 | Data Exfiltration | 祕密透過模型回答流出去。 |
| 178 | 黑名單 | Blocklist | 用固定字樣擋輸入。 |
| 179 | 速率限制 | Rate Limiting | 限制每人每段時間的請求數。 |
| 180 | .gitignore | .gitignore | 告訴 git 哪些檔案不要進版本庫。 |
| 181 | .env | .env | 放環境變數的檔案，要進 .gitignore。 |
| 182 | 部署 | Deployment | 把程式放到會一直跑、別人能用的地方。 |
| 183 | 樹莓派 | Raspberry Pi | 一直開著的小電腦，適合家用伺服器。 |
| 184 | HTTPS | HTTPS | 加密的 HTTP。 |
| 185 | 費用上限 | Spend Limit | 主控台設定的每月最高花費。 |
| 186 | 驗證 | Authentication | 確認「你是誰」才讓用。 |
| 187 | 權杖驗證 | Token Auth | 請求帶一串祕密字串，伺服器比對。 |

## D.11　硬體與其他（第 13、15 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 188 | ESP32 | ESP32 | 有 Wi-Fi 的微控制器開發板，《動手玩電》第 16 章。 |
| 189 | 網頁伺服器 | Web Server | ESP32 上回應 /on、/off 的程式。 |
| 190 | 路徑 | Route / Path | 網址後面的 /on、/off。 |
| 191 | 序列埠 | Serial Port | ESP32 與電腦傳訊息的通道，印 IP 用。 |
| 192 | DHT11 | DHT11 | 溫濕度感測器。 |
| 193 | 正規表示式 | Regular Expression | 用模式從文字裡抓數字或字串。 |
| 194 | SQLite | SQLite | 單檔的小型資料庫，Python 內建支援。 |
| 195 | CSV | CSV | 逗號分隔的表格文字檔。 |
| 196 | 最小平方法 | Least Squares | 找讓誤差平方和最小的直線。 |
| 197 | 決定係數 | R² | 直線解釋了多少變異，1 是完美。 |
| 198 | Google Colab | Google Colab | 免費的線上 Python 環境，有 GPU。 |
| 199 | GPU | GPU | 顯示卡，訓練模型快很多。 |
| 200 | Hugging Face | Hugging Face | 存放開源模型與資料集的平台。 |
