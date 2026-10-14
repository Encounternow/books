# 附錄 B　程式索引與驗證版本

每一章的程式做什麼、需要哪些套件、作者實際驗證的方式與結果。「驗證」欄：**實跑** = 作者在本機 venv 執行並把輸出寫進書；**匯入驗證** = 沒有金鑰或裝置，只確認匯入、建構請求無誤，書中輸出標為「預期」；**語法檢查** = 只做 `py_compile`。

## B.1　驗證環境

| 項目 | 版本／規格 |
|---|---|
| 驗證日期 | 2026 年 10 月 14 日 |
| 作業系統 | macOS（Darwin 25.6.0，Apple Silicon） |
| Python | 3.13.7 |
| 建立 venv | `python3 -m venv venv` |
| Claude Code | 2.1.299 |
| GPU | 無（全部在 CPU 上跑） |
| API 金鑰 | 本機未設定；需要金鑰的程式用假金鑰確認請求能送出（收到 401） |
| Ollama | 本機未安裝；相關程式只做語法檢查 |
| ESP32 實機 | 未接；用 `fake_esp32.py` 模擬 |

## B.2　套件版本（第 11–15 章驗證時 `pip list`）

| 套件 | 版本 | 用在 |
|---|---|---|
| anthropic | 1.13.0 | 13、14、15 |
| mcp | 2.3.0 | 13、15 |
| torch | 2.14.1 | 11、12 |
| transformers | 5.19.0 | 11、15 |
| peft | 0.21.2 | 11、15 |
| datasets | 5.1.0 | 11 |
| accelerate | 1.15.0 | 11 |
| fastapi | 0.143.0 | 14 |
| uvicorn | 0.54.0 | 14 |
| pydantic | 2.14.1 | 14 |
| starlette | 1.8.0 | 14（fastapi 相依） |
| requests | 2.34.2 | 13、15 |
| httpx | 0.28.1 | 13（mcp 相依） |
| numpy | 2.5.4 | 11、12 |

兩個版本相關的注意事項：

- **mcp 2.x**：`FastMCP` 改名 `MCPServer`（`from mcp.server.mcpserver import MCPServer`），回應屬性改 snake_case（`server_info`、`input_schema`、`is_error`），工具錯誤用 `mcp.server.mcpserver.exceptions.ToolError`。HTTP client 的 `streamable_http_client()` 回傳 `(read, write)` 兩條串流。要留在 1.x：`pip install "mcp<2"`。
- **transformers 5.x**：`from_pretrained(torch_dtype=...)` 改成 `dtype=...`（舊名還能用但會警告）。

## B.3　程式索引

### 第 11 章　微調二 LoRA 實作

| 程式 | 做什麼 | 套件 | 驗證 | 結果摘要 |
|---|---|---|---|---|
| lora_train.py | 用 16 筆「三行格式」資料做 LoRA 微調，存補丁 | torch、transformers、peft、datasets、accelerate | 實跑（tiny-gpt2 30 步；Qwen2.5-0.5B-Instruct 60 步） | Qwen：trainable 4,399,104／498,431,872（0.88%），loss 2.49→0.088，CPU 103.8 秒，補丁 17.6 MB |
| lora_compare.py | 同一問題比較微調前後 | 同上 | 實跑 | 微調後 100% 三行格式、講完就停；內容只在訓練資料內的才對 |
| lora_merge.py | `merge_and_unload()` 合併成完整模型 | 同上 | 實跑 | 合併後 model.safetensors 1.98 GB |
| GGUF 轉換指令 | llama.cpp 的 convert_hf_to_gguf.py + Modelfile | llama.cpp、Ollama | 未跑（只列指令） | — |

### 第 12 章　從零訓練小模型

| 程式 | 做什麼 | 套件 | 驗證 | 結果摘要 |
|---|---|---|---|---|
| mini_gpt.py | 字元級迷你 Transformer（2 層、64 維、4 頭），訓練 600 步並產生文字 | torch | 實跑 | 111,693 參數；loss 4.469→0.049；CPU 約 5 秒；產生文字逐字重現故事 |

### 第 13 章　自架 MCP 伺服器

| 程式 | 做什麼 | 套件 | 驗證 | 結果摘要 |
|---|---|---|---|---|
| home_mcp.py | 家庭資料伺服器：find_item（SQLite）、read_sensor、ohm；resource、prompt；stdio／HTTP | mcp、sqlite3 | 實跑 | 兩種傳輸都連通 |
| test_client.py | stdio client 呼叫全部工具、resource、prompt，含 ToolError 案例 | mcp | 實跑 | 輸出如書 |
| test_client_http.py | streamable HTTP client | mcp | 實跑 | `HTTP 連線成功` |
| fake_esp32.py | 模擬《動手玩電》第 16 章 ESP32 網頁伺服器（/、/on、/off） | 標準庫 | 實跑 | — |
| esp32_mcp.py | light_on／light_off／read_weather，透過 requests 打 ESP32 | mcp、requests | 實跑（對 fake_esp32） | 離線時 3 秒逾時後回傳文字，不當掉 |
| test_esp32.py | 呼叫三個 ESP32 工具 | mcp | 實跑 | — |
| api_mcp.py | API 端 mcp_servers + mcp_toolset | anthropic | 匯入驗證（假金鑰→401） | 書中輸出為預期 |
| local_mcp_agent.py | tool_runner + async_mcp_tool 把本機 MCP 工具接給 Claude | anthropic[mcp]、mcp | 匯入驗證（伺服器啟動、工具轉換成功、請求→401） | 書中輸出為預期 |
| claude mcp add 指令 | 接到 Claude Code | Claude Code 2.1.299 | 用 `claude mcp add --help` 查證格式 | — |

### 第 14 章　組裝與部署

| 程式 | 做什麼 | 套件 | 驗證 | 結果摘要 |
|---|---|---|---|---|
| main.py | FastAPI 後端：/、/health、/ask；字重疊檢索；假生成或 Claude；黑名單、長度上限、日誌、費用 | fastapi、uvicorn、pydantic、anthropic | 實跑（USE_FAKE=1）；generate_claude 匯入驗證 | curl 五個案例輸出如書；app.log 三行 |
| static/index.html | 一頁式前端，fetch /ask | — | 實跑（curl 取回） | — |
| notes.txt | 8 條範例筆記 | — | — | — |

### 第 15 章　專題

| 程式 | 做什麼 | 套件 | 驗證 | 結果摘要 |
|---|---|---|---|---|
| p1/rag_ollama.py | chromadb + Ollama 嵌入與生成 | chromadb、ollama | 語法檢查（本機無 Ollama） | 書中輸出為預期 |
| p2/logger.py | 每 60 秒抓 ESP32 溫濕度寫 sensor.json／history.csv | requests | 實跑（對 fake_esp32，75 秒） | 兩筆紀錄 |
| p3/chat_lora.py | 載入原模型 + LoRA 補丁的終端機聊天 | transformers、peft、torch | 實跑（用第 11 章 Qwen 補丁） | 輸出如書 |
| p4/lab_mcp.py | 實驗數據 MCP：list_csv、describe、fit_line；路徑越界用 ToolError 擋 | mcp | 實跑 | slope 4.54、r² 0.9998；越界被擋 |
| p4/test_lab.py | 呼叫三個工具與越界案例 | mcp | 實跑 | — |
| p4/SKILL.md | lab-report Skill | Claude Code | 未在互動對話中執行 | 書中對話為預期 |

## B.4　常見錯誤訊息對照

| 錯誤訊息 | 章 | 原因 | 解法 |
|---|---|---|---|
| `ModuleNotFoundError: No module named 'mcp.server.fastmcp'` | 13 | mcp 2.x | 改 `from mcp.server.mcpserver import MCPServer` |
| `'CallToolResult' object has no attribute 'isError'` | 13、15 | 2.x 改 snake_case | 用 `is_error` |
| `torch_dtype is deprecated! Use dtype instead!` | 11 | transformers 5.x | 改 `dtype=` |
| `AuthenticationError: 401 invalid x-api-key` | 13、14 | 金鑰沒設或錯 | 檢查 `ANTHROPIC_API_KEY` |
| `Address already in use` | 13、14 | 埠被占 | `pkill -f uvicorn` 或換埠 |
| `HTTPConnectionPool ... ConnectTimeoutError` | 13、15 | ESP32 IP 錯或離線 | 看序列埠印的 IP、同一個 Wi-Fi |
| `CUDA out of memory` | 11 | Colab 記憶體不夠 | batch 降 1、max_length 降 64 |
| `size mismatch` 載入補丁時 | 11 | 補丁與模型不符 | 訓練與載入用同一個 MODEL |
| 微調後輸出停不下來 | 11 | 訓練文字沒加 eos | `build_text` 加 `tok.eos_token` |
