# 第 13 章　自架MCP伺服器

## 本章目標

- 學完你會用官方 `mcp` 套件寫一個自己的 MCP 伺服器，提供工具（tools）、資源（resources）和提示（prompts）。
- 學完你會分得出 stdio 與 HTTP 兩種傳輸方式，知道什麼時候用哪一種。
- 學完你會把伺服器接進 Claude Code（`claude mcp add`）、Claude Desktop（設定檔）與 API 端（`mcp_servers`），三種接法各試一次。
- 學完你會先用 mcp 的 client 程式把伺服器跑通、再接給 AI，碰到問題知道從哪裡查。
- 學完你會替工具加上輸入驗證與最小權限，並說出為什麼不能把它開到公網。

## 開場：讓 AI 幫你找家裡的電池

第 4 章你裝過別人寫好的 MCP 伺服器，讓 Claude 讀你的資料夾、查 SQLite。那時候你可能已經想到：我家的東西放在哪、客廳現在幾度、ESP32 上那顆燈——這些資料只有我有，沒有人會幫我寫伺服器。

這一章就是自己寫。你會發現一個 MCP 伺服器真的只是「幾個 Python 函式加上裝飾器」：函式的名稱是工具名、docstring 是給 AI 看的說明、型別提示是參數格式，剩下的握手、序列化、傳輸全由 `mcp` 套件包辦。寫完之後，在 Claude Code 裡打一句「家裡的 AA 電池放在哪？」，它就會呼叫你的 `find_item` 工具，從你的 SQLite 查出「客廳抽屜，8 個」。

本章兩個活動：先做「家庭資料 MCP」（查物品、讀感測器、算歐姆定律），再做「ESP32 燈 MCP」——透過 HTTP 呼叫《動手玩電》第 16 章你做過的網頁伺服器（ https://book.vichuang.tw/electric/ ），讓 Claude 用自然語言開關那顆 LED。沒有 ESP32 實機也沒關係，書裡附一個假的 ESP32，先把程式跑通。

## 核心概念

### 複習：MCP 的三種東西

第 4 章用過，這裡從「寫伺服器的人」的角度再看一次：

| 種類 | 誰主動 | 像什麼 | 本章的例子 |
|---|---|---|---|
| 工具（Tool） | AI 決定要不要叫 | 函式：給參數、回結果 | `find_item("電池")`、`light_on()` |
| 資源（Resource） | 使用者或程式掛進對話 | 唯讀的檔案或資料 | `home://items` 整張物品表 |
| 提示（Prompt） | 使用者選用 | 預先寫好的提示詞範本 | `weekly_check` 每週檢查庫存 |

大部分時候你只需要工具。資源適合「一整份背景資料」（AI 不用一筆一筆查），提示適合「固定要做的例行任務」。

### 一個裝飾器就是一個工具

官方 Python SDK（`pip install mcp`，本書用 2.x）的高階寫法長這樣：

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("home")

@mcp.tool()
def ohm(voltage: float, resistance: float) -> str:
    """用歐姆定律算電流：I = V / R（伏特、歐姆）。"""
    return f"{voltage / resistance * 1000:.1f} mA"
```

三件事自動發生：函式名 `ohm` 變成工具名；docstring 變成工具說明，AI 靠它決定什麼時候用；型別提示 `float` 變成 JSON Schema，AI 送來的參數會先被檢查。回傳值可以是字串、數字、dict、list，SDK 會轉成 MCP 的內容格式。

> **版本提醒：mcp 1.x 與 2.x**
>
> 作者寫作時 `pip install mcp` 裝到的是 **2.3.0**。第 4 章已經用 2.x 的寫法，本章延續；但網路上很多教學還是 1.x 的 `from mcp.server.fastmcp import FastMCP`，兩者**用法完全等價**（`FastMCP("home")` 就是 `MCPServer("home")`，裝飾器一模一樣），只是 2.x 改了名字，而且 1.x 的匯入在 2.x 會直接報 `ModuleNotFoundError` 並告訴你改名了。2.x 另外兩個會碰到的差異：
>
> - 回應物件的屬性全部改成 snake_case：`server_info`、`protocol_version`、`input_schema`、`is_error`（1.x 是 `serverInfo`、`inputSchema`、`isError`）。
> - 工具裡要回報錯誤，丟 `mcp.server.mcpserver.exceptions.ToolError`，訊息才會原樣傳回 client；丟一般的 `ValueError` 只會收到「Error executing tool xxx」，看不到原因。
>
> 如果你手上有一堆 1.x 的程式不想改，`pip install "mcp<2"` 可以留在舊版；本書的程式一律用 2.x 寫法。

### 回報錯誤：用 ToolError

工具不可能每次都成功：電阻給 0、關鍵字太長、檔案不存在。這時候有兩種做法：回傳一段「錯誤文字」當結果，或丟 `ToolError`。本章兩種都用，分工是：

- **使用者輸入不合理**（電阻 ≤ 0、關鍵字太長）：丟 `ToolError("電阻必須大於 0")`。client 收到的結果 `is_error = True`、內容是 `Error executing tool ohm: 電阻必須大於 0`，AI 看得懂、會重新問使用者。
- **外部裝置連不到**（ESP32 離線）：回傳文字「連不到 ESP32……」。這不算工具寫錯，而是一個正常的狀態，讓 AI 告訴使用者裝置離線就好。

不管哪一種，**不要讓例外直接炸出來**：SDK 會把它包成通用錯誤，訊息會被吃掉，你在 AI 那邊只看到「工具失敗」，除錯要花很久。

### 兩種傳輸：stdio 與 HTTP

伺服器寫好了，AI 怎麼跟它講話？MCP 定義了傳輸層，常用兩種：

```
stdio（標準輸入輸出）                HTTP（streamable HTTP）
┌──────────┐ 啟動子程序 ┌─────────┐   ┌──────────┐  http://host:8000/mcp  ┌─────────┐
│ Claude   │──────────►│ 你的    │   │ Claude   │───────────────────────►│ 你的    │
│ Code/    │ stdin ──► │ server  │   │ / 任何   │        JSON 請求        │ server  │
│ Desktop  │ ◄── stdout│ (python)│   │ client   │◄───────────────────────│ (uvicorn)│
└──────────┘           └─────────┘   └──────────┘        JSON/SSE 回應     └─────────┘
 一對一、AI 負責啟動與關閉            伺服器自己跑著，多個 client 都能連
```

- **stdio**：AI 程式把你的伺服器當子程序啟動，透過 stdin／stdout 傳 JSON。最簡單、最安全（只有啟動它的程式能用），本機用這個。注意：**子程序不會自動繼承你終端機的環境變數**，要靠 `-e` 或設定檔明確傳。
- **streamable HTTP**：伺服器自己用 uvicorn 跑在某個埠，client 用網址連。適合伺服器在另一台機器（例如樹莓派）、或多個 client 要共用。預設只聽 `127.0.0.1`，要給區網用得改 host，而且一定要加驗證（本章最後講）。

程式裡切換只差一行：`mcp.run()` 是 stdio，`mcp.run(transport="streamable-http")` 是 HTTP。

### 三種接法

| 接到哪 | 怎麼接 | 誰啟動伺服器 |
|---|---|---|
| Claude Code | `claude mcp add home -- /path/venv/bin/python /path/home_mcp.py` | Claude Code（stdio） |
| Claude Desktop | 編輯 `claude_desktop_config.json` 加一段 `mcpServers` | Claude Desktop（stdio） |
| API（`client.beta.messages.create`） | `mcp_servers=[{"type":"url", ...}]` + `tools=[{"type":"mcp_toolset", ...}]` | 你自己，而且要在公網 |
| 自己的 Python 程式 | `anthropic.lib.tools.mcp` 把 MCP 工具包成 tool_runner 的工具 | 你的程式（stdio） |

前兩種是日常用法。第三種要特別注意：API 端的 MCP connector 是 **Anthropic 的伺服器去連你的 URL**，所以 `127.0.0.1` 絕對連不到，你得把伺服器放到有公網網址、有驗證的地方。想在自己電腦上「用 API 接本機 MCP」，用第四種：你的 Python 程式同時當 MCP client 和 Claude API client，工具在本機執行，只有對話送到 API。

### 先跑通，再接 AI

接給 AI 之前，一定先用 `mcp` 套件自己的 client 把每個工具呼叫一遍。原因是 AI 那邊的錯誤訊息很不直接（常常只看到「工具呼叫失敗」），而 client 程式會直接把 Python 的例外印給你。流程：

```
1. python test_client.py       ← 自己當 client，列出工具、每個呼叫一次
2. 看輸出對不對、改程式
3. claude mcp add ...          ← 接給 Claude Code
4. claude mcp list             ← 確認狀態是 Connected
5. 在對話裡試一句
```

官方還有一個圖形化工具 MCP Inspector（用 `npx @modelcontextprotocol/inspector` 啟動，需要 Node.js），可以在瀏覽器裡看伺服器有哪些工具、手動填參數呼叫、看原始 JSON。本章用 Python client 就夠，Inspector 留給你想看協定細節時用。

### 安全：你的伺服器就是 AI 的手

MCP 工具是 AI「真的能做事」的地方，所以安全全在這一層：

1. **驗證輸入**：AI 送來的參數不一定合理。SQL 一律用參數化查詢（`?`），不要字串拼接；檔名要擋 `..`；數字要檢查範圍；長度要設上限。
2. **最小權限**：工具只做它該做的。查物品的工具不給「執行任意 SQL」；讀 CSV 的工具只讀固定資料夾。一個工具一件事，AI 組合起來用。
3. **不暴露公網**：stdio 天生只有本機能用。HTTP 模式預設只聽 `127.0.0.1`；要開給區網或公網，一定要加 token 驗證、用 HTTPS，而且先問自己「真的需要嗎」。
4. **危險動作要確認**：開燈沒關係，「刪資料」「轉帳」「寄信」這類工具，要嘛不提供，要嘛在工具裡要求使用者輸入確認碼。
5. **別把祕密寫進回傳值**：工具回傳的任何文字都會進到 AI 的上下文、可能出現在對話裡。Wi-Fi 密碼、API 金鑰不要讓工具讀得到。

第 14 章的 prompt injection 會再談：如果工具讀到的資料裡藏著「叫 AI 做壞事」的文字，AI 可能照做——所以工具能做的事越少越安全。

## 動手做

### 活動 13-1：寫一個「家庭資料 MCP」

**材料／工具**：Python 3.10+、venv、`pip install mcp`、Claude Code 或 Claude Desktop。

**步驟**：

1. 建資料夾 `home-mcp`，把本章的 `home_mcp.py`、`sensor.json`、`test_client.py` 放進去。
2. 執行 `python test_client.py`，應該看到三個工具各回傳一次結果、資源前兩行、提示內容。
3. 把 `init_db()` 裡的範例資料改成你家真的東西（至少五筆）。
4. 接到 Claude Code：`claude mcp add home -- <venv 的 python 絕對路徑> <home_mcp.py 絕對路徑>`，再 `claude mcp list` 看到 Connected。
5. 在 Claude Code 問：「家裡的杜邦線在哪？5 V 接 220 Ω 的電流是多少？」看它呼叫哪些工具。
6. 新增一個工具 `add_item(name, place, qty)` 讓 AI 能幫你登記新東西；先想一下要擋什麼輸入。

**你應該看到／得到**：`test_client.py` 的輸出和書上一致；Claude Code 對話中出現工具呼叫的提示並要求你同意；新增的工具在 `claude mcp list` 重新連線後出現。

**觀察與記錄**：

| 我問的話 | AI 呼叫了哪些工具（順序） | 參數 | 回答對嗎 |
|---|---|---|---|
| | | | |
| | | | |
| | | | |

### 活動 13-2：寫一個控制 ESP32 燈的 MCP

**材料／工具**：活動 13-1 的環境、`pip install requests`；《動手玩電》第 16 章做好的 ESP32 網頁伺服器（有 `/on`、`/off` 路徑），**沒有實機時用本章的 `fake_esp32.py` 代替**。

**步驟**：

1. 把 `esp32_mcp.py`、`fake_esp32.py`、`test_esp32.py` 放進資料夾。
2. 開一個終端機跑 `python fake_esp32.py`（假 ESP32，聽 8080 埠）。
3. 另一個終端機跑 `python test_esp32.py`，看到 `light_on → LED ON`、溫濕度、`light_off → LED OFF`。
4. 有實機：把 ESP32 的 IP 填進環境變數 `ESP32_URL=http://192.168.x.x`，重跑第 3 步，LED 應該真的亮滅。
5. 接到 Claude Code：`claude mcp add esp32 -e ESP32_URL=http://192.168.x.x -- <python> <esp32_mcp.py>`。
6. 在對話裡說「把燈打開」「現在幾度」「關燈」。
7. 把 ESP32 關機（或把 `ESP32_URL` 改成不存在的 IP），再問一次，看 AI 怎麼處理「連不到」。

**你應該看到／得到**：假 ESP32 時三個工具都回傳固定值；實機時 LED 真的動、溫濕度是真的數字；關機後工具回傳「連不到 ESP32……」的文字，AI 會告訴你裝置離線而不是當掉。

**觀察與記錄**：

| 情況 | 我說的話 | 工具回傳 | AI 的回答 | 燈的狀態 |
|---|---|---|---|---|
| 假 ESP32 | 把燈打開 | | | （無） |
| 實機 | 把燈打開 | | | |
| 實機 | 現在幾度 | | | |
| 關機 | 把燈打開 | | | |

## 程式與執行

### 環境

```bash
python -m venv venv
source venv/bin/activate
pip install mcp requests anthropic
```

作者驗證時 `mcp` 是 2.3.0（本章程式都用 2.x 寫法）、`anthropic` 1.13.0。

### home_mcp.py：家庭資料伺服器

```python
# home_mcp.py：家庭資料 MCP 伺服器（查 SQLite、讀感測器、算東西）
import sys, json, sqlite3
from pathlib import Path

from mcp.server.mcpserver import MCPServer               # mcp 2.x（1.x 叫 FastMCP，見版本提醒）
from mcp.server.mcpserver.exceptions import ToolError    # 丟這個例外，錯誤訊息才會傳回 client

DB = Path(__file__).with_name("home.db")           # 資料庫放在程式旁邊
SENSOR = Path(__file__).with_name("sensor.json")   # 感測器最新讀值（由另一支程式寫入）

def init_db():
    # 第一次執行時建表、塞幾筆範例資料
    con = sqlite3.connect(DB)
    con.execute("CREATE TABLE IF NOT EXISTS items (name TEXT, place TEXT, qty INTEGER)")
    if con.execute("SELECT COUNT(*) FROM items").fetchone()[0] == 0:
        con.executemany("INSERT INTO items VALUES (?,?,?)", [
            ("AA 電池", "客廳抽屜", 8), ("三用電錶", "書房書架", 1),
            ("杜邦線", "工具箱", 40), ("ESP32", "書房書架", 2), ("麵包板", "工具箱", 3)])
        con.commit()
    con.close()

mcp = MCPServer("home", instructions="查家裡的物品、感測器讀值與簡單計算。")

@mcp.tool()
def find_item(keyword: str) -> str:
    """用關鍵字查家裡的物品放在哪裡、有幾個。"""
    if len(keyword) > 50:                              # 驗證輸入：太長直接拒絕
        raise ToolError("關鍵字太長（上限 50 字）")        # 用 ToolError，client 會收到這句話
    con = sqlite3.connect(DB)
    # 用參數化查詢（?），絕對不要把字串拼進 SQL，否則會被 SQL injection
    rows = con.execute("SELECT name, place, qty FROM items WHERE name LIKE ?",
                       (f"%{keyword}%",)).fetchall()
    con.close()
    if not rows:
        return f"找不到含「{keyword}」的物品"
    return "\n".join(f"{n}：在{p}，共 {q} 個" for n, p, q in rows)

@mcp.tool()
def read_sensor() -> dict:
    """讀最新的溫濕度（來自 sensor.json）。"""
    if not SENSOR.exists():
        return {"error": "還沒有感測器資料"}
    return json.loads(SENSOR.read_text(encoding="utf-8"))

@mcp.tool()
def ohm(voltage: float, resistance: float) -> str:
    """用歐姆定律算電流：I = V / R（伏特、歐姆）。"""
    if resistance <= 0:
        raise ToolError("電阻必須大於 0")
    return f"{voltage / resistance * 1000:.1f} mA"

@mcp.resource("home://items")
def all_items() -> str:
    """整張物品表，當作背景資料給 AI 讀。"""
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT name, place, qty FROM items").fetchall()
    con.close()
    return "\n".join(f"{n},{p},{q}" for n, p, q in rows)

@mcp.prompt()
def weekly_check() -> str:
    """產生一段「每週檢查庫存」的提示詞。"""
    return "請讀 home://items，列出數量少於 3 的物品，並建議要不要補貨。"

if __name__ == "__main__":
    init_db()
    if "--http" in sys.argv:
        mcp.run(transport="streamable-http")           # 網址是 http://127.0.0.1:8000/mcp
    else:
        mcp.run()                                      # 預設 stdio：由 Claude 啟動這支程式
```

`sensor.json` 先手動放一份（第 15 章專題會用 ESP32 真的寫它）：

```json
{"temperature": 27.5, "humidity": 63, "updated": "2026-10-14 15:40"}
```

### test_client.py：自己當 client（stdio）

```python
# test_client.py：用 mcp 的 client 透過 stdio 啟動 home_mcp.py，實際呼叫每個工具
import asyncio, sys
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():
    # 告訴 client 怎麼啟動 server：用同一個 Python 跑 home_mcp.py
    params = StdioServerParameters(command=sys.executable, args=["home_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()                # 握手：交換版本與能力
            print("伺服器：", init.server_info.name)          # 2.x 的屬性都是 snake_case
            tools = await session.list_tools()
            print("工具：", [t.name for t in tools.tools])
            print("ohm 的參數格式：", tools.tools[2].input_schema["properties"])

            r = await session.call_tool("find_item", {"keyword": "電池"})
            print("find_item →", r.content[0].text)
            r = await session.call_tool("ohm", {"voltage": 5, "resistance": 220})
            print("ohm →", r.content[0].text)
            r = await session.call_tool("read_sensor", {})
            print("read_sensor →", r.content[0].text)
            r = await session.call_tool("ohm", {"voltage": 5, "resistance": 0})   # 故意給錯的輸入
            print("ohm(錯誤) → is_error =", r.is_error, "|", r.content[0].text)

            res = await session.read_resource("home://items")   # 讀 resource
            print("resource 前兩行：", res.contents[0].text.splitlines()[:2])
            p = await session.get_prompt("weekly_check")        # 取 prompt
            print("prompt →", p.messages[0].content.text)

asyncio.run(main())
```

真實輸出：

```
伺服器： home
工具： ['find_item', 'read_sensor', 'ohm']
ohm 的參數格式： {'voltage': {'title': 'Voltage', 'type': 'number'}, 'resistance': {'title': 'Resistance', 'type': 'number'}}
find_item → AA 電池：在客廳抽屜，共 8 個
ohm → 22.7 mA
read_sensor → {
  "temperature": 27.5,
  "humidity": 63,
  "updated": "2026-10-14 15:40"
}
ohm(錯誤) → is_error = True | Error executing tool ohm: 電阻必須大於 0
resource 前兩行： ['AA 電池,客廳抽屜,8', '三用電錶,書房書架,1']
prompt → 請讀 home://items，列出數量少於 3 的物品，並建議要不要補貨。
```

注意「ohm 的參數格式」那行：你只寫了 `voltage: float`，SDK 就產生了 JSON Schema，這就是 AI 看到的參數說明。最後一個錯誤案例顯示 `ToolError` 的訊息完整傳到了 client。
工具： ['find_item', 'read_sensor', 'ohm']
find_item → AA 電池：在客廳抽屜，共 8 個
ohm → 22.7 mA
read_sensor → {
  "temperature": 27.5,
  "humidity": 63,
  "updated": "2026-10-14 15:40"
}
resource 前兩行： ['AA 電池,客廳抽屜,8', '三用電錶,書房書架,1']
prompt → 請讀 home://items，列出數量少於 3 的物品，並建議要不要補貨。
```

### test_client_http.py：用 HTTP 連

先在一個終端機啟動 `python home_mcp.py --http`，它會印出 uvicorn 在 `http://127.0.0.1:8000` 的訊息。另一個終端機：

```python
# test_client_http.py：連到用 --http 啟動的 home_mcp.py（streamable HTTP 傳輸）
import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():
    async with streamable_http_client("http://127.0.0.1:8000/mcp") as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            print("HTTP 連線成功，工具：", [t.name for t in tools.tools])
            r = await session.call_tool("find_item", {"keyword": "ESP32"})
            print("find_item →", r.content[0].text)

asyncio.run(main())
```

真實輸出：

```
伺服器： home
工具： ['find_item', 'read_sensor', 'ohm']
ohm 的參數格式： {'voltage': {'title': 'Voltage', 'type': 'number'}, 'resistance': {'title': 'Resistance', 'type': 'number'}}
find_item → AA 電池：在客廳抽屜，共 8 個
ohm → 22.7 mA
read_sensor → {
  "temperature": 27.5,
  "humidity": 63,
  "updated": "2026-10-14 15:40"
}
ohm(錯誤) → is_error = True | Error executing tool ohm: 電阻必須大於 0
resource 前兩行： ['AA 電池,客廳抽屜,8', '三用電錶,書房書架,1']
prompt → 請讀 home://items，列出數量少於 3 的物品，並建議要不要補貨。
```

注意「ohm 的參數格式」那行：你只寫了 `voltage: float`，SDK 就產生了 JSON Schema，這就是 AI 看到的參數說明。最後一個錯誤案例顯示 `ToolError` 的訊息完整傳到了 client。
HTTP 連線成功，工具： ['find_item', 'read_sensor', 'ohm']
find_item → ESP32：在書房書架，共 2 個
```

兩種傳輸的 client 程式只差「怎麼拿到 read／write 兩條串流」那一行，後面的 `ClientSession` 完全一樣。

### 接到 Claude Code

```bash
# stdio：用「--」隔開，後面是啟動伺服器的完整指令（路徑用絕對路徑）
claude mcp add home -- /Users/me/home-mcp/venv/bin/python /Users/me/home-mcp/home_mcp.py

# 需要環境變數時用 -e（子程序不會繼承你的 shell 環境變數）
claude mcp add esp32 -e ESP32_URL=http://192.168.1.57 -- /Users/me/home-mcp/venv/bin/python /Users/me/home-mcp/esp32_mcp.py

# HTTP 模式的伺服器
claude mcp add --transport http home-http http://127.0.0.1:8000/mcp

# 查看、移除
claude mcp list
claude mcp get home
claude mcp remove home
```

`-s` 決定設定存在哪：`-s local`（預設）只在你這台電腦的這個專案；`-s user` 你這台電腦的所有專案都能用；`-s project` 寫進專案的 `.mcp.json`（可以進 git、同學拿到就能用）。以上格式以 Claude Code 2.1.299 的 `claude mcp add --help` 為準，新版若有變動以 `--help` 為主。接好之後在 Claude Code 對話裡問「家裡的 AA 電池在哪」，它會先徵求同意再呼叫 `find_item`。

### 接到 Claude Desktop

編輯設定檔（macOS 在 `~/Library/Application Support/Claude/claude_desktop_config.json`，Windows 在 `%APPDATA%\Claude\claude_desktop_config.json`），加一段：

```json
{
  "mcpServers": {
    "home": {
      "command": "/Users/me/home-mcp/venv/bin/python",
      "args": ["/Users/me/home-mcp/home_mcp.py"]
    },
    "esp32": {
      "command": "/Users/me/home-mcp/venv/bin/python",
      "args": ["/Users/me/home-mcp/esp32_mcp.py"],
      "env": {"ESP32_URL": "http://192.168.1.57"}
    }
  }
}
```

存檔後完全關閉再打開 Claude Desktop，對話框旁會出現工具圖示。`command` 一定要是 venv 裡 python 的絕對路徑，否則它會用系統 Python、找不到 `mcp` 套件。

### fake_esp32.py：沒有實機時的替身

```python
# fake_esp32.py：假的 ESP32，用 Python 內建 http.server 模仿《動手玩電》第 16 章的網頁伺服器
# 沒有實機時用它測試 esp32_mcp.py；有實機就不需要這支程式
from http.server import BaseHTTPRequestHandler, HTTPServer

state = {"led": "off"}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/on":
            state["led"] = "on"; body = "LED ON"            # 和實機一樣：/on 開燈
        elif self.path == "/off":
            state["led"] = "off"; body = "LED OFF"
        else:                                                # 根路徑：模仿 16-4 的溫濕度網頁
            body = "<h1>教室溫濕度</h1><p style='font-size:3em'>27.5 &deg;C</p><p style='font-size:3em'>63 %</p>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))
    def log_message(self, *a):                              # 安靜一點，不印每個請求
        pass

print("假 ESP32 在 http://127.0.0.1:8080")
HTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
```

### esp32_mcp.py：控制燈與讀溫濕度

```python
# esp32_mcp.py：控制 ESP32 燈的 MCP 伺服器——透過 HTTP 呼叫《動手玩電》第 16 章的網頁伺服器
import os, re, requests
from mcp.server.mcpserver import MCPServer               # mcp 2.x（1.x 叫 FastMCP）
from mcp.server.mcpserver.exceptions import ToolError    # 丟這個例外，錯誤訊息才會傳回 client

# ESP32 的 IP 從環境變數讀；沒設就用假 ESP32（fake_esp32.py）的位址
ESP32 = os.environ.get("ESP32_URL", "http://127.0.0.1:8080")
mcp = MCPServer("esp32", instructions="控制客廳的 ESP32 LED，並讀取溫濕度。")

def _get(path: str) -> str:
    # 所有請求都走這裡：只允許固定路徑、設 3 秒逾時，失敗回傳文字而不是當掉
    try:
        r = requests.get(ESP32 + path, timeout=3)
        r.raise_for_status()
        return r.text
    except requests.RequestException as e:
        return f"連不到 ESP32（{ESP32}）：{e}"

@mcp.tool()
def light_on() -> str:
    """打開 ESP32 上的 LED。"""
    return _get("/on")

@mcp.tool()
def light_off() -> str:
    """關掉 ESP32 上的 LED。"""
    return _get("/off")

@mcp.tool()
def read_weather() -> dict:
    """讀 ESP32 氣象站網頁上的溫度與濕度。"""
    html = _get("/")
    # 從網頁文字裡用正規表示式把「27.5 °C」和「63 %」抓出來
    t = re.search(r"([\d.]+)\s*&deg;C", html)
    h = re.search(r"(\d+)\s*%", html)
    if not (t and h):
        return {"error": "網頁裡找不到溫濕度", "raw": html[:100]}
    return {"temperature": float(t.group(1)), "humidity": int(h.group(1))}

if __name__ == "__main__":
    mcp.run()
```

注意工具沒有「任意網址」參數——AI 只能開、關、讀，不能叫 ESP32 做別的。這就是最小權限。

### test_esp32.py

```python
# test_esp32.py：透過 MCP client 呼叫 esp32_mcp.py 的三個工具
import asyncio, os, sys
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():
    # stdio 啟動的 server 不會自動繼承環境變數，要用 env 明確傳進去
    params = StdioServerParameters(command=sys.executable, args=["esp32_mcp.py"],
                                   env={"ESP32_URL": os.environ.get("ESP32_URL", "http://127.0.0.1:8080")})
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as s:
            await s.initialize()
            for name in ("light_on", "read_weather", "light_off"):
                r = await s.call_tool(name, {})
                print(f"{name} →", r.content[0].text)

asyncio.run(main())
```

對假 ESP32 的真實輸出（`python fake_esp32.py` 先跑著）：

```
light_on → LED ON
read_weather → {
  "temperature": 27.5,
  "humidity": 63
}
light_off → LED OFF
```

對一個不存在的位址（`ESP32_URL=http://10.255.255.1 python test_esp32.py`）的真實輸出，等了 3 秒後：

```
light_on → 連不到 ESP32（http://10.255.255.1）：HTTPConnectionPool(host='10.255.255.1', port=80): Max retries exceeded with url: /on (Caused by ConnectTimeoutError(... 'Connection to 10.255.255.1 timed out. (connect timeout=3)'))
```

程式沒有當掉，而是把錯誤當成文字回傳，AI 就能告訴使用者「裝置離線」。**實機**：把 `ESP32_URL` 換成序列埠監控視窗印出的 IP，LED 會真的亮滅；作者寫作時沒有接實機，這部分請你自己驗證。

### api_mcp.py：API 端用 mcp_servers（需要公網 URL 與金鑰）

```python
# api_mcp.py：在 API 端用 mcp_servers + mcp_toolset，讓 Claude 直接連「遠端」的 MCP 伺服器
# 注意：API 端只能連「網路上拿得到的 URL」，不能連你電腦上的 127.0.0.1（Anthropic 的伺服器連不進你家）
import anthropic

client = anthropic.Anthropic()                      # 金鑰從環境變數 ANTHROPIC_API_KEY 讀

response = client.beta.messages.create(
    model="claude-opus-5-5",
    max_tokens=1024,
    betas=["mcp-client-2025-11-20"],                # MCP connector 目前是 beta 功能
    # 兩個參數要一起給：mcp_servers 說「伺服器在哪」，tools 裡的 mcp_toolset 說「用它的工具」
    mcp_servers=[{"type": "url", "url": "https://你的網域/mcp", "name": "home"}],
    tools=[{"type": "mcp_toolset", "mcp_server_name": "home"}],
    messages=[{"role": "user", "content": "家裡的 AA 電池放在哪裡？"}],
)
for block in response.content:
    if block.type == "text":
        print(block.text)
```

作者本機沒有公網伺服器也沒有設 API 金鑰，用假金鑰執行確認程式能送出請求（收到 `AuthenticationError: 401 invalid x-api-key`，表示請求格式正確、只是金鑰不對）。**預期輸出**（有金鑰、伺服器在公網時）：

```
家裡的 AA 電池在客廳抽屜，共 8 個。
```

### local_mcp_agent.py：在本機把 MCP 工具接給 Claude

```python
# local_mcp_agent.py：在自己電腦上把「本機 MCP 伺服器的工具」接給 Claude 用（tool_runner + async_mcp_tool）
import asyncio, sys
from anthropic import AsyncAnthropic
from anthropic.lib.tools.mcp import async_mcp_tool         # 需要 pip install "anthropic[mcp]"
from mcp import ClientSession
from mcp.client.stdio import stdio_client, StdioServerParameters

async def main():
    client = AsyncAnthropic()
    params = StdioServerParameters(command=sys.executable, args=["home_mcp.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            # 把每個 MCP 工具包成 Claude 能呼叫的工具；tool_runner 會自動跑「呼叫 → 執行 → 回傳」迴圈
            runner = client.beta.messages.tool_runner(
                model="claude-opus-5-5",
                max_tokens=4096,
                tools=[async_mcp_tool(t, session) for t in tools],
                messages=[{"role": "user", "content": "5 V 接 220 Ω 的電阻會有多少電流？另外家裡的杜邦線在哪？"}],
            )
            async for message in runner:               # 每一輪的回覆都會印出來
                for block in message.content:
                    if block.type == "text":
                        print(block.text)
                    elif block.type == "tool_use":
                        print(f"[呼叫工具 {block.name} {block.input}]")

asyncio.run(main())
```

同樣用假金鑰確認：伺服器成功啟動、工具清單成功轉換、請求送出後收到 401。**預期輸出**（有金鑰時）：

```
[呼叫工具 ohm {'voltage': 5, 'resistance': 220}]
[呼叫工具 find_item {'keyword': '杜邦線'}]
5 V 接 220 Ω 的電流約 22.7 mA。杜邦線在工具箱，共 40 條。
```

這個寫法是第 15 章專題二的基礎：同一支程式裡，MCP 工具在你家執行，Claude 只負責決定「叫哪個工具」。

## 常見錯誤與迷思

- **`ModuleNotFoundError: No module named 'mcp.server.fastmcp'` → 你裝到 mcp 2.x 但程式是 1.x 寫法 → 改成 `from mcp.server.mcpserver import MCPServer`，或 `pip install "mcp<2"` 留在舊版。**
- **`AttributeError: 'CallToolResult' object has no attribute 'isError'` → 2.x 屬性改成 snake_case → 用 `is_error`、`input_schema`、`server_info`。**
- **工具裡丟了例外，AI 只看到「Error executing tool」沒有原因 → 一般例外的訊息會被吃掉 → 改丟 `ToolError("原因")`。**
- **接到 Claude Code 後顯示 Failed to connect → 幾乎都是路徑 → `command` 要用 venv 裡 python 的絕對路徑；用 `claude mcp get home` 看它實際執行的指令，自己在終端機貼一次看會不會錯。**
- **工具在 test_client 能跑、接給 AI 就讀不到環境變數 → stdio 子程序不繼承環境 → `claude mcp add` 用 `-e`，Desktop 設定檔用 `"env"`。**
- **在 server 裡用 `print()` 除錯，結果整個連線壞掉 → stdio 模式下 stdout 是傳輸通道 → 除錯訊息改印到 stderr（`print(..., file=sys.stderr)`）或用 logging。**
- **把 HTTP 伺服器 host 改成 0.0.0.0 讓手機也能連 → 區網裡任何裝置都能叫你的工具 → 至少加 token 驗證；控制實體裝置的伺服器尤其不要這樣開。**
- **API 端 `mcp_servers` 填 `http://127.0.0.1:8000/mcp` → Anthropic 的伺服器連不到你的電腦 → 改用 `local_mcp_agent.py` 的做法，或把伺服器部署到公網並加驗證。**
- **以為 docstring 隨便寫沒關係 → AI 靠它決定要不要用這個工具 → 寫清楚「做什麼、參數單位、什麼時候用」，和第 3 章 Skill 的 description 一樣重要。**

## 想一想

1. `find_item` 用 `WHERE name LIKE ?` 加參數，如果改成 `f"WHERE name LIKE '%{keyword}%'"` 字串拼接，AI（或被注入的資料）送來 `' OR 1=1 --` 會發生什麼？

<details><summary>參考答案</summary>

SQL 變成 `WHERE name LIKE '%' OR 1=1 --%'`，`OR 1=1` 永遠為真，會把整張表吐出來；更惡意的輸入可以接 `; DROP TABLE items` 刪表。參數化查詢把輸入當成「值」而不是「SQL 的一部分」，就不會被改寫。

</details>

2. 為什麼 `esp32_mcp.py` 不提供一個 `fetch(path)` 工具讓 AI 自己決定要打哪個路徑，而是寫死 `light_on`、`light_off`、`read_weather` 三個？

<details><summary>參考答案</summary>

最小權限。有了 `fetch(path)`，AI（或 prompt injection）可以打任何路徑，包括你以後加的 `/reset`、`/update` 之類的危險路徑，甚至改 `ESP32` 變數指向別台機器。三個固定工具讓 AI 只能做這三件事，出錯的範圍也只有這三件事。

</details>

3. stdio 和 HTTP 各舉一個「非它不可」的情境。

<details><summary>參考答案</summary>

stdio：伺服器要讀你電腦上的私人檔案（例如家用 SQLite），而且只給你自己的 Claude Code 用——不用開埠、不用驗證、關掉 Claude Code 伺服器就跟著關。HTTP：伺服器跑在樹莓派上（感測器接在那裡），你在筆電上的 Claude Desktop 和手機上的另一個 client 都要連它——stdio 做不到跨機器。

</details>

4. `test_esp32.py` 對不存在的 IP 等了 3 秒才回應。如果 AI 一次呼叫 `light_on`、`read_weather`、`light_off` 三個工具，使用者要等多久？怎麼改善？

<details><summary>參考答案</summary>

最壞 9 秒（三次各逾時 3 秒），如果 client 是一個一個叫的話。改善：(1) 逾時縮到 1 秒；(2) 在 `_get` 裡記住「上次連不到的時間」，30 秒內直接回傳「裝置離線」不再重試；(3) 工具說明裡寫「若回傳離線，不要重複嘗試」，讓 AI 不要連叫三次。

</details>

5. 你想加一個 `delete_item(name)` 工具。列出三個你會加的保護措施。

<details><summary>參考答案</summary>

(1) 只允許刪「完全相符」的名稱，不用 LIKE，避免一次刪一堆；(2) 要求第二個參數 `confirm: str` 必須等於物品名稱（AI 得先問使用者確認），或改成「標記為刪除」而非真的刪；(3) 每次刪除寫一行日誌（時間、名稱），並且回傳「已刪除 X」讓使用者看得到。更保守的做法：根本不提供，刪除讓人自己做。

</details>

6. 開放挑戰：把 `home_mcp.py` 用 `--http` 跑在樹莓派上，想讓家裡區網的 Claude Desktop 連進來。設計一個最簡單的驗證：client 要帶什麼、server 怎麼檢查、token 放哪裡。查一下 `claude mcp add --transport http` 的 `--header` 選項怎麼配合。

<details><summary>參考答案</summary>

最簡單：server 啟動時從環境變數讀一個長隨機字串 `MCP_TOKEN`，用 MCPServer 的中介層（middleware）或 `custom_route` 前的檢查，要求每個請求的 `Authorization: Bearer <token>` 標頭相符，不符回 401。client 端 `claude mcp add --transport http home http://樹莓派IP:8000/mcp --header "Authorization: Bearer <token>"`。token 放環境變數或只有你能讀的檔案，不進 git。再加兩道：server 只聽區網介面、不要在路由器上開埠轉發。要開到網際網路時，才需要 HTTPS 和正式的 OAuth。

</details>

## 本章小結

- 一個 MCP 伺服器 = `MCPServer` 物件 + 幾個加了 `@mcp.tool()` 的函式；docstring 是給 AI 的說明、型別提示是參數格式。
- `mcp` 2.x 把 `FastMCP` 改名 `MCPServer`、屬性改 snake_case；工具錯誤丟 `ToolError` 訊息才會傳回。1.x 寫法等價，`pip install "mcp<2"` 可保留。
- stdio：AI 啟動子程序、只有本機能用、不繼承環境變數。HTTP：伺服器自己跑、可跨機器、預設只聽 127.0.0.1、要開出去就要驗證。
- 接 Claude Code 用 `claude mcp add name -- <python> <server.py>`（`-e` 傳環境變數、`--transport http` 接網址）；接 Claude Desktop 編輯 `claude_desktop_config.json`。
- API 端 `mcp_servers` + `mcp_toolset` 只能連公網 URL；本機工具要給 API 用，改用 `anthropic.lib.tools.mcp` 在自己程式裡轉接。
- 先用 `test_client.py` 跑通每個工具，再接 AI；stdio 模式除錯訊息印到 stderr。
- 安全四件事：參數化查詢與輸入驗證、工具只做一件事、不開公網、危險動作要確認。
- 控制實體裝置（ESP32）就是多一層 `requests.get`，連不到要回傳文字而不是當掉。

## 名詞表

| 中文 | 英文 | 一句話解釋 |
|---|---|---|
| MCP 伺服器 | MCP Server | 把工具、資源、提示提供給 AI 的程式。 |
| MCP 客戶端 | MCP Client | 連到伺服器、呼叫工具的那一方（Claude Code、Desktop 或你的程式）。 |
| MCPServer／FastMCP | MCPServer / FastMCP | 官方 Python SDK 的高階伺服器類別，2.x 與 1.x 的名稱。 |
| 工具錯誤 | ToolError | 2.x 裡工具用來回報錯誤的例外，訊息會原樣傳給 client。 |
| 工具 | Tool | AI 可以呼叫的函式，有名稱、說明、參數格式。 |
| 資源 | Resource | 用 URI 標示的唯讀資料，例如 home://items。 |
| 提示 | Prompt | 伺服器提供的提示詞範本。 |
| 標準輸入輸出傳輸 | stdio transport | 用子程序的 stdin／stdout 傳 JSON 的傳輸方式。 |
| 串流 HTTP 傳輸 | Streamable HTTP transport | 用 HTTP 請求與 SSE 回應的傳輸方式，網址結尾是 /mcp。 |
| 握手 | initialize | client 與 server 連線後交換版本與能力的第一步。 |
| JSON Schema | JSON Schema | 描述參數格式的標準，由型別提示自動產生。 |
| 參數化查詢 | Parameterized Query | SQL 用 ? 佔位、資料另外傳，防止 SQL injection。 |
| SQL 注入 | SQL Injection | 把惡意字串拼進 SQL 讓資料庫做不該做的事。 |
| 最小權限 | Least Privilege | 工具只給完成任務所需的最少能力。 |
| MCP Inspector | MCP Inspector | 官方的圖形化除錯工具，可手動呼叫工具。 |
| MCP connector | MCP connector | API 端用 mcp_servers 讓 Anthropic 伺服器去連你的 MCP 伺服器。 |
| mcp_toolset | mcp_toolset | tools 參數裡的項目，指定要用哪個 mcp_servers 的工具。 |
| 逾時 | Timeout | 等待回應的最長時間，超過就放棄。 |
| 環境變數 | Environment Variable | 程式外部設定的鍵值，用來傳 IP、金鑰等。 |
