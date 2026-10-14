# 第 9 章　本地模型與 Ollama

## 本章目標

學完這一章，你會：

- 說出什麼時候該用本地模型、什麼時候該用雲端的 Claude，以及各自的代價。
- 在自己的電腦上裝好 Ollama、拉下一個小模型、在終端機跟它對話。
- 看懂模型名稱後面的「4b」「Q4_K_M」是什麼意思，並用一條算式估算模型要吃多少記憶體。
- 用 `ollama` Python 套件呼叫本地模型，包含一般回答、串流輸出和嵌入。
- 把第 8 章的 RAG 整條管線換成「嵌入也本地、生成也本地」，資料完全不出門。
- 設計一張比較表，用同一組問題衡量三個不同大小的模型的品質與速度。

## 開場：沒有網路的那個下午

颱風天，小宇家停電又停網。他本來打算用第 8 章做好的「問我的筆記」機器人查「颱風來的時候盆栽要怎麼辦」，結果 `rag_claude.py` 一執行就噴錯：連不上網路。

他突然意識到一件事：他家的筆記明明都在自己電腦裡，向量資料庫也在自己電腦裡，檢索的部分完全不需要網路——唯一要出門的是最後一步「生成」，因為模型在雲端。

那模型可不可以也在自己的電腦裡？可以。這幾年開源的語言模型越做越小、越做越好，幾十億參數的模型壓縮之後只有兩三 GB，一台普通筆電就跑得動。差別是：它比 Claude 笨一些、慢一些，但它免費、不用網路、而且你問它的每一個字都不會離開你的電腦。

這一章就是把「模型」搬回自己家。工具叫 Ollama，它把「下載模型、載入記憶體、提供一個可以呼叫的服務」全部包成兩三條指令。裝好之後，第 8 章那支程式只要改一行，就從雲端切換成本地。

## 核心概念

### 為什麼要本地模型

| 理由 | 說明 | 什麼情境特別重要 |
|---|---|---|
| 隱私 | 資料不離開電腦 | 病歷、日記、公司內部文件、別人託付給你的資料 |
| 離線 | 沒網路也能用 | 外出、網路不穩、颱風天 |
| 免費 | 跑一萬次和跑一次都不用錢 | 大量批次處理、反覆測試提示、學生練習 |
| 可控 | 模型版本不會被別人更新、不會突然改行為 | 需要結果穩定重現的實驗 |
| 可改 | 可以微調成自己的模型（第 10、11 章） | 想要特定語氣或格式 |

代價也要說清楚：

| 代價 | 說明 |
|---|---|
| 品質 | 筆電跑得動的模型（1 到 8B）明顯比 Claude 弱，複雜推理、長文件理解、少見語言都差一截 |
| 速度 | 沒有獨立顯示卡時，每秒幾個到十幾個 token，長回答要等 |
| 硬體 | 要有足夠的記憶體；想跑大一點的模型要有顯示卡 |
| 維護 | 要自己下載、更新、處理錯誤 |

所以合理的用法通常不是「全部本地」或「全部雲端」，而是看任務：簡單、大量、私密的交給本地；困難、重要、需要高品質的交給 Claude。本章最後有一張決策表。

### Ollama 是什麼、怎麼裝

Ollama 是一個管理和執行本地語言模型的工具。它做三件事：

1. **模型庫**：`ollama pull 名字` 就能從官方模型庫下載模型，不用自己找檔案。
2. **執行引擎**：載入模型到記憶體，自動用你的顯示卡（有的話）或 CPU 跑。
3. **服務**：在背景開一個網路服務（預設 `http://localhost:11434`），你的 Python 程式、第 8 章的 RAG、甚至其他 App 都透過它呼叫模型。

安裝方式（依官方網站 https://ollama.com/download ）：

| 系統 | 方法 |
|---|---|
| macOS | 下載 .dmg 安裝，或 `brew install ollama` |
| Windows | 下載安裝程式執行 |
| Linux | `curl -fsSL https://ollama.com/install.sh \| sh` |

裝好後在終端機確認：

```bash
ollama --version
```

**預期輸出**（作者的機器未安裝 Ollama，以下為依官方文件撰寫的預期結果，版本號會隨時間不同）：

```
ollama version is 0.x.y
```

macOS 和 Windows 的安裝程式會順便把 Ollama 設成背景服務，開機自動啟動。如果你發現服務沒在跑（Python 程式噴 `Failed to connect to Ollama`），可以手動開一個終端機視窗執行 `ollama serve`，讓它一直開著。

### 拉模型與跑模型

Ollama 的模型名稱格式是 `家族:標籤`，標籤通常寫參數量，例如 `qwen3:4b` 是 Qwen3 家族的 40 億參數版本。本書示範用的小模型「例如」有這些（模型庫更新很快，實際名稱請以 https://ollama.com/library 為準）：

| 例如 | 參數量 | 下載大小約 | 適合 |
|---|---|---|---|
| `qwen3:0.6b` | 6 億 | 0.5 GB | 最小的，任何電腦都能跑，看懂簡單指令 |
| `qwen3:1.7b` | 17 億 | 1.4 GB | 8 GB 記憶體的筆電可跑 |
| `qwen3:4b` | 40 億 | 2.6 GB | 中文不錯、本書 RAG 的主要示範 |
| `gemma3:4b` | 40 億 | 3.3 GB | 另一個家族，可以互相比較 |
| `llama3.2:3b` | 30 億 | 2.0 GB | 英文強、中文普通 |
| `nomic-embed-text` | 1.4 億 | 0.3 GB | 嵌入模型，不是聊天用的 |

拉一個模型：

```bash
ollama pull qwen3:4b
```

**預期輸出**：

```
pulling manifest
pulling 163553aea1b1... 100% ▕████████████████▏ 2.5 GB
pulling ae370d884f10... 100% ▕████████████████▏ 1.7 KB
pulling d18a5cc71b84... 100% ▕████████████████▏  11 KB
pulling cff3f395ef37... 100% ▕████████████████▏  120 B
pulling 05a61d37b084... 100% ▕████████████████▏  487 B
verifying sha256 digest
writing manifest
success
```

那些十六進位的字串是模型各個部件的雜湊值，每個模型都不一樣，不用管它。拉完之後直接聊：

```bash
ollama run qwen3:4b
```

**預期輸出**（進入互動模式，`>>>` 後面打字，`/bye` 離開）：

```
>>> 用一句話解釋什麼是歐姆定律
歐姆定律說明電壓、電流與電阻的關係：電壓等於電流乘以電阻（V = I × R）。

>>> /bye
```

其他常用指令：

| 指令 | 做什麼 |
|---|---|
| `ollama list` | 列出已下載的模型與大小 |
| `ollama ps` | 看現在哪些模型載入在記憶體裡 |
| `ollama show qwen3:4b` | 看模型的參數量、量化等級、上下文長度 |
| `ollama rm qwen3:1.7b` | 刪掉一個模型釋放硬碟 |
| `ollama serve` | 手動啟動服務（通常已在背景） |

`ollama list` 的**預期輸出**：

```
NAME                ID              SIZE      MODIFIED
qwen3:4b            a1b2c3d4e5f6    2.6 GB    3 minutes ago
qwen3:1.7b          b2c3d4e5f6a1    1.4 GB    10 minutes ago
qwen3:0.6b          c3d4e5f6a1b2    523 MB    12 minutes ago
nomic-embed-text    d4e5f6a1b2c3    274 MB    15 minutes ago
```

模型檔案存在家目錄的 `.ollama/models/` 裡（Windows 是 `C:\Users\你的名字\.ollama\models\`）。

### 模型檔案：GGUF 與量化

你會發現 `qwen3:4b` 有 40 億個參數，但只有 2.6 GB。算一下：如果每個參數用 16 位元（2 個位元組）存，40 億 × 2 = 80 億位元組 = 8 GB 才對。怎麼縮成 2.6 GB？

答案是量化（Quantization）：把每個參數從 16 位元壓到 4 位元左右。想像你有一張很精細的照片，每個像素用 65,536 種顏色表示；量化就像改成只用 16 種顏色——檔案小四倍，遠看幾乎一樣，近看有一點粗糙。模型也是這樣：Q4 量化之後，回答品質只掉一點點，但記憶體需求少四分之三，速度也變快。

量化等級常見的寫法：

| 寫法 | 每個參數約幾位元 | 品質 | 什麼時候用 |
|---|---|---|---|
| FP16 / BF16 | 16 | 原始品質 | 有大顯示卡、要做微調 |
| Q8_0 | 8 | 幾乎無損 | 記憶體夠、想要最接近原版 |
| Q5_K_M | 5.5 | 很好 | 折衷 |
| Q4_K_M | 4.5 | 好，最常用 | Ollama 大多數模型的預設 |
| Q3 / Q2 | 3 / 2 | 明顯變笨 | 只為了塞進很小的機器 |

Ollama 用的檔案格式叫 GGUF，是專為「在一般電腦用 CPU 或顯示卡跑量化模型」設計的格式，一個檔案就包含權重和必要的設定。第 11 章微調完的模型要給 Ollama 用，就要轉成 GGUF。

估算記憶體的算式很簡單：

```
記憶體（GB）≈ 參數量（十億）× 每個參數的位元數 ÷ 8
```

例如 4B 模型 Q4（約 4.5 位元）：4 × 4.5 ÷ 8 = 2.25 GB。實際執行還要加上「上下文」（你送進去的文字和它的中間計算）大約再多 0.5 到 2 GB。用程式算一張表（`memory_estimate.py`，這支純 Python，作者實際執行）：

```python
def memory_gb(params_billion, bits):
    """估算模型權重要佔多少記憶體：參數量 × 每個參數的位元數 ÷ 8 ÷ 10 億"""
    bytes_per_param = bits / 8
    return params_billion * 1e9 * bytes_per_param / 1e9

# 常見的大小與量化等級（FP16 是沒量化、Q8 是 8 位元、Q4 是 4 位元）
sizes = [0.5, 1.5, 4, 8, 14, 32, 70]
print("| 參數量（B） | FP16（16 位元） | Q8（8 位元） | Q4（約 4.5 位元） |")
print("|---|---|---|---|")
for b in sizes:
    # Q4 實際上每個參數約 4.5 位元（有些額外的縮放資訊）
    print(f"| {b} | {memory_gb(b, 16):.1f} GB | {memory_gb(b, 8):.1f} GB | {memory_gb(b, 4.5):.1f} GB |")
```

執行結果：

| 參數量（B） | FP16（16 位元） | Q8（8 位元） | Q4（約 4.5 位元） |
|---|---|---|---|
| 0.5 | 1.0 GB | 0.5 GB | 0.3 GB |
| 1.5 | 3.0 GB | 1.5 GB | 0.8 GB |
| 4 | 8.0 GB | 4.0 GB | 2.2 GB |
| 8 | 16.0 GB | 8.0 GB | 4.5 GB |
| 14 | 28.0 GB | 14.0 GB | 7.9 GB |
| 32 | 64.0 GB | 32.0 GB | 18.0 GB |
| 70 | 140.0 GB | 70.0 GB | 39.4 GB |

這張表解釋了為什麼大家在筆電上跑的都是 Q4：同樣 8 GB 記憶體，FP16 只能跑 4B 以下，Q4 可以跑到 8B 以上。

### 硬體需求表

把上面的算式套到常見電腦：

| 你的電腦 | 可用記憶體 | 建議模型大小（Q4） | 速度大概 |
|---|---|---|---|
| 8 GB 記憶體、無獨顯 | 約 4 GB 給模型 | 0.5B–3B | 慢，每秒 5–15 token |
| 16 GB 記憶體、無獨顯 | 約 8–10 GB | 4B–8B | 每秒 5–15 token |
| Apple M 系列 16 GB 以上 | 統一記憶體，GPU 共用 | 8B–14B | 快，每秒 20–60 token |
| 有 8 GB 顯示卡（NVIDIA） | 顯示卡記憶體 8 GB | 4B–8B 全進顯示卡 | 快，每秒 30–80 token |
| 有 24 GB 顯示卡 | 24 GB | 14B–32B | 很快 |
| Google Colab 免費 GPU（T4，16 GB） | 16 GB | 8B–14B | 快，但要裝 Ollama 或改用其他工具 |

記憶體不夠時 Ollama 會把一部分放到主記憶體、一部分放顯示卡，能跑但慢很多；完全不夠就會載入失敗。原則：**模型檔案大小 + 2 GB，不要超過你能給它的記憶體**。

「每秒幾個 token」是什麼感覺？一個中文字大約 1 到 2 個 token。每秒 10 token 大概是「比你朗讀稍慢」，每秒 30 token 是「比你看字快」。

### 用 Python 呼叫

裝 Python 套件：

```bash
pip install ollama
```

最基本的呼叫，和第 1 章呼叫 Claude 的結構幾乎一樣：一個 `messages` 列表、角色是 system／user／assistant（`ollama_hello.py`）：

```python
import ollama

# 把一段對話送給本機的 Ollama（預設連 http://localhost:11434）
# model 寫你已經 pull 下來的模型名稱
response = ollama.chat(
    model="qwen3:4b",
    messages=[
        {"role": "system", "content": "你是一個用繁體中文回答的助理，回答要簡短。"},
        {"role": "user", "content": "用一句話解釋什麼是歐姆定律。"},
    ],
)

# 回傳物件的 .message.content 就是模型的回答
print(response.message.content)
# 這幾個欄位可以用來算速度（單位是奈秒，除以 1e9 變成秒）
print("輸出 token 數：", response.eval_count)
print("生成花費秒數：", round(response.eval_duration / 1e9, 2))
```

**預期輸出**：

```
歐姆定律說明電壓等於電流乘以電阻，寫成 V = I × R。
輸出 token 數： 28
生成花費秒數： 1.85
```

串流輸出，加 `stream=True` 就會一段一段回來（`ollama_stream.py`）：

```python
import ollama

# stream=True 時，回傳的是一個「一小段一小段」的迭代器
stream = ollama.chat(
    model="qwen3:4b",
    messages=[{"role": "user", "content": "寫一首關於電阻的四行小詩。"}],
    stream=True,
)

# 每收到一小段就馬上印出來，不換行，看起來像打字機
for chunk in stream:
    print(chunk.message.content, end="", flush=True)
print()
```

**預期輸出**（會一個字一個字出現）：

```
小小電阻一身黑，
色環四圈記數值，
電流經過它會熱，
守住電路不出事。
```

嵌入（第 7 章用 sentence-transformers 做的事，Ollama 也能做，`ollama_embed.py`）：

```python
import ollama

# 用 Ollama 的嵌入模型把兩句話變向量（要先 ollama pull nomic-embed-text）
r = ollama.embed(
    model="nomic-embed-text",
    input=["今天天氣很好", "The weather is nice today"],
)

# r.embeddings 是「每句一個向量」的列表
print("向量數：", len(r.embeddings))
print("每個向量的長度：", len(r.embeddings[0]))
print("第一個向量的前 5 個數字：", [round(x, 4) for x in r.embeddings[0][:5]])
```

**預期輸出**：

```
向量數： 2
每個向量的長度： 768
第一個向量的前 5 個數字： [0.0123, -0.0456, 0.0789, 0.0012, -0.0345]
```

注意 `nomic-embed-text` 輸出 768 維，第 7 章的 MiniLM 是 384 維，兩者不能混用（第 7 章講過：存和查要同一個模型）。

另外，Ollama 也提供一個「OpenAI 相容」的端點 `http://localhost:11434/v1`。有些第三方工具只會講 OpenAI 的格式，把它們的網址指到這裡就能接上本地模型。本書自己的程式一律用 `ollama` 套件，這個端點只在這裡提一下。

### 本地模型 vs Claude：怎麼選

| 情境 | 建議 | 理由 |
|---|---|---|
| 個人筆記問答（第 8 章） | 本地 | 資料私密、問題簡單、免費 |
| 要處理幾千篇文章做分類、摘要 | 本地 | 量大，雲端費用會累積 |
| 寫程式、除錯、複雜推理 | Claude | 本地小模型常常答錯或繞圈 |
| 需要讀很長的文件（幾萬字） | Claude | 本地模型的上下文通常較短，而且長了就慢 |
| 給別人用的產品、要穩定品質 | Claude | 品質與穩定度差距大 |
| 練習提示工程、反覆試 100 次 | 本地 | 免費試錯 |
| 沒網路 | 本地 | 沒得選 |
| 資料絕對不能外流 | 本地 | 沒得選 |

一個很實用的組合：**用本地模型做「粗活」，把需要判斷的部分交給 Claude。** 例如先用本地模型把 1,000 封郵件分成「要回／不用回」，再把 50 封要回的交給 Claude 寫草稿。

## 動手做

### 活動 9-1：比較三個不同大小的模型

這個活動的結果要你自己填，因為每台電腦的速度不同、每個模型版本的回答也不同。作者提供程式和表格。

**材料／工具**

- 裝好的 Ollama，拉三個同家族不同大小的模型，例如 `qwen3:0.6b`、`qwen3:1.7b`、`qwen3:4b`（總共約 4.5 GB）
- `compare_models.py`

**步驟**

1. 拉模型：

```bash
ollama pull qwen3:0.6b
ollama pull qwen3:1.7b
ollama pull qwen3:4b
```

2. 寫 `compare_models.py`。它對三個模型各問同樣五題，記錄回答、秒數和每秒 token 數：

```python
import time
import ollama

# 三個不同大小的模型（請改成你自己 pull 下來的名稱）
MODELS = ["qwen3:0.6b", "qwen3:1.7b", "qwen3:4b"]

# 同一組問題，從簡單到難
QUESTIONS = [
    "台灣最高的山是哪一座？",
    "用一句話解釋什麼是餘弦相似度。",
    "一個 1000 瓦的電器開 8 小時，用了幾度電？請列出算式。",
    "把這句話翻成英文：冷氣濾網每兩個月要洗一次。",
    "寫一個 Python 函式，輸入攝氏溫度，回傳華氏溫度。",
]

for model in MODELS:
    print(f"\n========== {model} ==========")
    for q in QUESTIONS:
        t0 = time.time()
        r = ollama.chat(model=model, messages=[{"role": "user", "content": q}])
        elapsed = time.time() - t0
        # tokens/秒 = 輸出 token 數 ÷ 生成秒數
        tps = r.eval_count / (r.eval_duration / 1e9)
        print(f"\n問：{q}")
        print(f"答：{r.message.content.strip()[:150]}")
        print(f"（{elapsed:.1f} 秒，{r.eval_count} tokens，{tps:.1f} tokens/秒）")
```

3. 執行 `python compare_models.py`。第一次問每個模型時會多花幾秒載入模型，那是正常的。
4. 對每一題的回答打分：3 分（正確且清楚）、2 分（大致對）、1 分（有錯）、0 分（完全錯或答非所問）。
5. 填表。

**你應該看到／得到**

**預期輸出**（節錄一題，實際內容會不同）：

```
========== qwen3:0.6b ==========

問：一個 1000 瓦的電器開 8 小時，用了幾度電？請列出算式。
答：1000 瓦 × 8 小時 = 8000 瓦小時 = 8 度電。
（1.2 秒，35 tokens，41.3 tokens/秒）

========== qwen3:4b ==========

問：一個 1000 瓦的電器開 8 小時，用了幾度電？請列出算式。
答：一度電是 1 千瓦小時（kWh）。算式：1000 W × 8 h = 8000 Wh = 8 kWh，所以用了 8 度電。
（3.8 秒，52 tokens，18.7 tokens/秒）
```

一般會看到的趨勢：模型越大，回答越完整、越少犯錯，但每秒 token 數越低。0.6B 常常在「翻譯」和「寫程式」兩題出錯或格式亂掉；4B 五題大多能過。中間那個 1.7B 常常是「筆電上最划算」的選擇。

**觀察與記錄**

品質分數（0–3 分）：

| 問題 | 0.6b | 1.7b | 4b |
|---|---|---|---|
| 台灣最高的山 | | | |
| 解釋餘弦相似度 | | | |
| 8 小時幾度電 | | | |
| 翻譯成英文 | | | |
| 攝氏轉華氏函式 | | | |
| **總分（滿分 15）** | | | |

速度：

| 模型 | 檔案大小 | 平均 tokens/秒 | 五題總秒數 | 第一次載入秒數 |
|---|---|---|---|---|
| 0.6b | | | | |
| 1.7b | | | | |
| 4b | | | | |

最後寫一句結論：「在我的電腦上，________ 是品質和速度最平衡的，因為 ________。」

### 活動 9-2：全本地 RAG

第 8 章的 RAG 有兩個地方用到模型：嵌入（sentence-transformers，已經是本地）和生成（Ollama 或 Claude）。這個活動把嵌入也換成 Ollama 的模型，整條管線都走 Ollama，程式更單純，而且資料從頭到尾不出門。

**材料／工具**

- 第 8 章的 `ch08/docs/` 與 `ch08/chunk.py`
- 已拉好 `nomic-embed-text` 與一個聊天模型（例如 `qwen3:4b`）
- 新檔案 `ch09/rag_all_local.py`

**步驟**

1. 拉嵌入模型：`ollama pull nomic-embed-text`。
2. 寫 `rag_all_local.py`。它借用第 8 章的切塊函式，但嵌入改用 `ollama.embed`，生成用 `ollama.chat`：

```python
import chromadb
import ollama
import sys
sys.path.insert(0, "../ch08")          # 借用第 8 章的切塊函式
from chunk import split_text, load_docs

EMBED_MODEL = "nomic-embed-text"   # 嵌入用的本地模型
CHAT_MODEL = "qwen3:4b"            # 生成用的本地模型

def embed(texts):
    """用 Ollama 的嵌入模型把一批文字變向量"""
    return ollama.embed(model=EMBED_MODEL, input=texts).embeddings

# 1. 建索引：切塊 → 用 Ollama 嵌入 → 存進 chromadb
client = chromadb.PersistentClient(path="rag_local_db")
try:
    client.delete_collection("docs")
except Exception:
    pass
col = client.create_collection("docs", metadata={"hnsw:space": "cosine"})
ids, texts = [], []
for name, text in load_docs("../ch08/docs"):
    for i, c in enumerate(split_text(text)):
        ids.append(f"{name}#{i}")
        texts.append(c)
col.add(ids=ids, documents=texts, embeddings=embed(texts))
print(f"索引完成：{len(texts)} 塊")

# 2. 問答：問題嵌入 → 找 3 塊 → 組提示 → 本地模型生成
def ask(question):
    q_vec = embed([question])[0]
    r = col.query(query_embeddings=[q_vec], n_results=3)
    context = "\n\n".join(f"[{i+1}] {d}" for i, d in enumerate(r["documents"][0]))
    prompt = f"只根據下面資料回答，沒有就說「資料裡沒有提到」。\n\n{context}\n\n問題：{question}"
    resp = ollama.chat(model=CHAT_MODEL, messages=[{"role": "user", "content": prompt}])
    print(f"\n問：{question}\n答：{resp.message.content.strip()}")

ask("颱風來的時候盆栽要怎麼辦？")
ask("社團的 LED 弄丟一顆要賠多少錢？")
```

3. 執行 `python rag_all_local.py`。
4. 把網路關掉，再執行一次。它應該還是能跑。

**你應該看到／得到**

**預期輸出**：

```
索引完成：15 塊

問：颱風來的時候盆栽要怎麼辦？
答：颱風警報發布後，要把四盆全部搬進客廳靠牆的地方，小番茄的支架要先拆掉；風停後再搬回去，
先放在陰涼處一天再曬太陽 [1]。

問：社團的 LED 弄丟一顆要賠多少錢？
答：LED 一顆 2 元 [1]。
```

這個版本和第 8 章的差異：嵌入模型從 384 維的 MiniLM 換成 768 維的 nomic-embed-text，資料庫也換了一個資料夾（`rag_local_db`），所以和第 8 章的 `rag_db` 不會打架。你可以把第 8 章的 `rag_eval.py` 搬過來改一改，比較兩個嵌入模型的 Hit@3 哪個高。

**觀察與記錄**

| 項目 | 第 8 章（MiniLM + Claude） | 全本地（nomic + qwen3:4b） |
|---|---|---|
| 建索引秒數 | | |
| 一題回答秒數 | | |
| 答案品質（0–3） | | |
| 需要網路 | 是 | 否 |
| 費用 | | 0 |

## 程式與執行

**1. 安裝與確認**

```bash
# 裝好 Ollama 之後
ollama --version
ollama pull qwen3:4b
ollama pull nomic-embed-text
ollama list

# Python 套件（沿用前兩章的 venv）
pip install ollama
```

作者驗證時的 Python 套件版本：ollama 0.6.3、chromadb 1.5.9、Python 3.13.7。作者的機器未安裝 Ollama 本體，本章所有 `ollama ...` 指令與需要連線到 Ollama 服務的程式輸出都標為「預期輸出」，依官方文件（ https://github.com/ollama/ollama 與 https://github.com/ollama/ollama-python ）撰寫；每支 Python 程式都通過語法檢查，`ollama.chat`、`ollama.embed`、`ollama.list` 的函式簽名與回傳物件欄位（`message.content`、`eval_count`、`eval_duration`、`embeddings`）都已對照套件原始碼確認。`memory_estimate.py` 是純 Python，有實際執行。

**2. 服務有沒有在跑**

打開瀏覽器到 `http://localhost:11434`，看到 `Ollama is running` 就是正常。或在終端機：

```bash
curl http://localhost:11434
```

沒有回應就執行 `ollama serve`（這個視窗要一直開著），或重新啟動 Ollama 應用程式。

**3. 看模型的細節**

```bash
ollama show qwen3:4b
```

**預期輸出**（節錄）：

```
  Model
    architecture        qwen3
    parameters          4.0B
    context length      40960
    embedding length    2560
    quantization        Q4_K_M
```

`quantization Q4_K_M` 就是本章講的 4 位元量化；`context length` 是它一次能看的最大 token 數。

**4. 看誰在吃記憶體**

```bash
ollama ps
```

**預期輸出**：

```
NAME        ID              SIZE      PROCESSOR    UNTIL
qwen3:4b    a1b2c3d4e5f6    3.4 GB    100% GPU     4 minutes from now
```

`SIZE` 比檔案大（3.4 GB 對 2.6 GB），多出來的就是上下文的記憶體；`PROCESSOR` 顯示是用 GPU 還是 CPU；`UNTIL` 表示閒置多久後會自動卸載。

**5. 在 Colab 上跑 Ollama**

Colab 可以裝 Ollama（用 Linux 那行安裝指令，前面加 `!`），但服務要用 `!nohup ollama serve &` 放到背景。免費 GPU 跑 4B 到 8B 很順。不過每次重開 Colab 都要重裝重拉，比較適合做實驗，不適合當日常工具。

**6. 常見錯誤訊息**

| 訊息 | 原因 | 解法 |
|---|---|---|
| `Failed to connect to Ollama` | 服務沒在跑 | `ollama serve` 或重啟 App |
| `model 'xxx' not found` | 沒拉這個模型或名字打錯 | `ollama list` 看正確名字，`ollama pull` |
| 回答極慢、風扇狂轉 | 記憶體不夠，模型一半在硬碟換頁 | 換小一點的模型或更低的量化 |
| `out of memory` | 完全塞不下 | 同上 |

## 常見錯誤與迷思

- **「本地模型跟 Claude 差不多，只是免費。」** → 錯。筆電跑得動的 1 到 8B 模型和 Claude 之間有明顯差距，尤其在推理、程式、長文件。 → 正確理解：本地模型適合簡單、大量、私密的任務；重要的、困難的交給 Claude。活動 9-1 的表會讓你親眼看到差距。

- **「量化就是變笨，應該用 FP16。」** → Q4_K_M 的品質損失很小，大多數人感覺不出來，但記憶體省四分之三。 → 正確理解：先用 Q4，真的覺得品質不夠再升 Q8，升到 FP16 幾乎沒必要。

- **「參數量越大越好，硬塞 14B。」** → 塞不進記憶體時 Ollama 會用硬碟換頁，速度掉到每秒 1 個 token，比小模型差得多。 → 正確理解：模型檔案 + 2 GB 不能超過可用記憶體，在這個限制內選最大的。

- **「Ollama 的嵌入模型和 sentence-transformers 的向量可以混用。」** → 錯，維度都不一樣（768 對 384），空間也完全不同。 → 正確理解：一個資料庫只用一個嵌入模型，換模型就重建。

- **「本地模型不用管安全。」** → 提示注入對本地模型一樣有效，而且小模型更容易被騙。如果你把 Ollama 的服務開到網路上（改 `OLLAMA_HOST` 讓外面連得到），任何人都能用你的電腦跑模型。 → 正確理解：服務只留在 `localhost`，不要開到公網；RAG 的資料還是要框清楚。

- **「`ollama run` 離開之後模型就卸載了，下次要重新載入很慢。」** → 預設閒置 5 分鐘才卸載，Python 程式連續呼叫不會每次重載。 → 正確理解：第一次呼叫慢是載入，之後的呼叫就是純生成時間；要常駐可以用 `keep_alive` 參數。

## 想一想

1. 一個 8B 的模型用 Q4_K_M（約 4.5 位元）量化，光權重要多少 GB？加上約 1.5 GB 的上下文，8 GB 記憶體的筆電跑得動嗎？

<details><summary>參考答案</summary>

8 × 4.5 ÷ 8 = 4.5 GB，加 1.5 GB 約 6 GB。8 GB 記憶體的筆電理論上塞得下，但作業系統和其他程式也要用記憶體，實際上會很擠、可能換頁變慢。保險的選擇是 4B 以下，或把其他程式都關掉再試。

</details>

2. 為什麼同一台電腦上，0.6B 模型每秒能生成 40 個 token，4B 模型只有 18 個？

<details><summary>參考答案</summary>

生成每一個 token 都要把整個模型的參數「算一遍」，參數越多，每個 token 的計算量和記憶體讀取量越大。4B 是 0.6B 的六倍多，雖然不是嚴格成反比（有些固定開銷），但大致上模型越大每秒 token 數越低。這也是為什麼小模型在「量大但簡單」的任務上很划算。

</details>

3. 小宇想用本地模型把 2,000 篇新聞分成「科技／體育／其他」三類，再把「科技」類的 100 篇交給 Claude 寫摘要。請說明這個安排的好處，以及可能的風險。

<details><summary>參考答案</summary>

好處：分類是簡單任務，本地模型做得來且免費，2,000 篇用雲端會花錢；摘要需要品質，100 篇交給 Claude 費用可控。風險：本地小模型分類會有錯，可能漏掉幾篇科技新聞或混進別的；解法是先用第 6 章的方法建一個 50 篇的評估集，確認本地模型的分類準確率可以接受，再放大跑。

</details>

4. 活動 9-2 把嵌入模型從 MiniLM 換成 nomic-embed-text。如果你直接讓它讀第 8 章的 `rag_db` 資料夾而不重建，會發生什麼事？

<details><summary>參考答案</summary>

查詢時會出錯或得到亂七八糟的結果。`rag_db` 裡存的是 384 維的向量，而 nomic-embed-text 算出來的問題向量是 768 維，chromadb 會因為維度不符直接報錯；就算維度剛好一樣，兩個模型的向量空間也完全不同，算出來的相似度沒有意義。換嵌入模型一定要重建索引。

</details>

5. （挑戰）修改 `compare_models.py`，讓它把每題的回答、秒數、tokens/秒自動寫進一個 CSV 檔，再用試算表畫一張「模型大小 vs 平均 tokens/秒」的長條圖。你預期是什麼形狀？

<details><summary>參考答案</summary>

用 Python 內建的 `csv` 模組，`csv.writer` 每題寫一列：模型、問題、回答前 50 字、秒數、tokens/秒。長條圖預期是「越大越矮」：0.6b 最高、4b 最矮。如果你的電腦有獨立顯示卡，三根柱子的差距會比純 CPU 小，因為 GPU 的記憶體頻寬高，大模型的負擔相對沒那麼重。

</details>

6. （挑戰）本章說「資料不出門」是本地模型的優點。請舉出三種「即使用本地模型，資料還是可能外流」的情況，並各給一個防法。

<details><summary>參考答案</summary>

(1) Ollama 服務被設定成監聽所有網路介面（`OLLAMA_HOST=0.0.0.0`），區域網路或公網的人都能連進來用、甚至看到你送的內容——防法：只留 `localhost`，或加防火牆。(2) 你的 Python 程式除了呼叫 Ollama，還有別的地方會上網（例如把對話記錄傳到某個分析服務、或用了會回報的套件）——防法：審視程式裡所有的網路呼叫，必要時斷網測試。(3) 模型本身是從不可信來源下載的，可能帶有惡意的設定或程式——防法：只從官方模型庫或信得過的來源拉模型。另外，RAG 的文件裡若有提示注入，雖然不會「外流」，但可能讓模型輸出不該輸出的內容給使用者看，這也要防。

</details>

## 本章小結

- 本地模型的三大理由：隱私、離線、免費；代價是品質、速度、硬體。
- Ollama 把「下載、執行、提供服務」包成幾條指令：`pull`、`run`、`list`、`ps`、`show`、`rm`。
- 模型名稱的「4b」是參數量；量化把每個參數從 16 位元壓到 4 到 8 位元，Q4_K_M 是最常用的折衷。
- 記憶體估算：參數量（B）× 位元數 ÷ 8，再加 1 到 2 GB 上下文；不要超過可用記憶體。
- Python 用 `ollama.chat`（可 `stream=True`）和 `ollama.embed`，結構和第 1 章呼叫 Claude 幾乎一樣。
- 第 8 章的 RAG 換成全本地只要把嵌入和生成兩處改成 Ollama，資料從頭到尾不出門。
- 選擇原則：簡單、大量、私密 → 本地；困難、重要、長文件 → Claude；常常是兩者搭配。
- 服務只開在 localhost，不要暴露到公網。

## 名詞表

| 中文 | 英文 | 一句話解釋 |
|---|---|---|
| 本地模型 | Local Model | 在自己電腦上執行的語言模型，不經過雲端 |
| Ollama | Ollama | 管理與執行本地模型的工具，提供模型庫與本機服務 |
| 參數量 | Parameter Count | 模型裡可學習的數字個數，常用 B（十億）為單位 |
| 量化 | Quantization | 把參數從 16 位元壓到更少位元以省記憶體、加速 |
| GGUF | GGUF | 專為一般電腦執行量化模型設計的模型檔案格式 |
| Q4_K_M | Q4_K_M | 約 4.5 位元的常用量化等級 |
| 上下文長度 | Context Length | 模型一次能看的最大 token 數 |
| 每秒 token 數 | Tokens per Second | 衡量生成速度的單位 |
| 嵌入模型 | Embedding Model | 專門把文字變向量的模型，不是用來聊天的 |
| 統一記憶體 | Unified Memory | Apple M 系列晶片讓 CPU 與 GPU 共用的記憶體 |
| 換頁 | Swapping / Paging | 記憶體不夠時把資料暫放到硬碟，會非常慢 |
| OpenAI 相容端點 | OpenAI-compatible Endpoint | Ollama 提供的另一種呼叫格式，讓其他工具能接上 |
| 常駐 | Keep-alive | 讓模型在記憶體裡保留一段時間不卸載 |
