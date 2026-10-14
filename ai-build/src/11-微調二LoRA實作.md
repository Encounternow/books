# 第 11 章　微調二LoRA實作

## 本章目標

- 學完你會說出全參數微調為什麼貴，以及 LoRA 怎麼用「只訓練一小塊補丁」把成本降到百分之一。
- 學完你會解釋 rank 與 alpha 兩個數字的意思，知道調大調小會怎樣。
- 學完你會用 transformers、peft、datasets 三個套件，在 Colab 免費 GPU（或自己電腦的 CPU）上微調一個幾百 MB 的小模型，讓它學會固定格式回覆。
- 學完你會比較微調前後的輸出，分得出「格式學會了」和「知識學會了」是兩回事。
- 學完你會把補丁合併回原模型，並知道怎麼轉成 GGUF 交給 Ollama 用。

## 開場：換輪胎，不用換整台車

第 10 章你整理了一份「用我的語氣回覆」的資料集，這章要真的把它教給模型。

想像模型是一台車，幾億個參數是車上的每一顆螺絲。「全參數微調」等於為了讓車子跑得順一點，把每顆螺絲都拆下來重新鎖一次：要很大的車庫（記憶體）、很多工具（GPU）、很久的時間。對一台 70 億顆螺絲的車，個人根本做不到。

LoRA 的想法是：車子本來就跑得不錯，我只是想讓它「習慣走我家附近的路」。那不用動螺絲，加裝一組小補丁就好——補丁很小、拆裝方便、換一組補丁就換一種習慣。本章要做的事就是：拿一個 5 億參數的小模型（約 1 GB），貼上一組 440 萬參數的補丁（17 MB），訓練 60 步，讓它從「想到什麼寫什麼」變成每次都用「【結論】【理由】【提醒】」三行回答。

整個過程作者在自己的筆電 CPU 上跑完只花了 104 秒；在 Colab GPU 上會更快。你不需要有顯示卡也能完成本章。

## 核心概念

### 全參數微調為什麼貴

一個參數在訓練時佔的記憶體不只它自己。以常見的設定算：

| 項目 | 每個參數要幾個數字 | 說明 |
|---|---|---|
| 權重本身 | 1 | 模型的數字 |
| 梯度 | 1 | 這一步要往哪裡調 |
| 優化器狀態（AdamW） | 2 | 記住前幾步的平均方向與大小 |
| 合計 | 4 | 每個參數約 4 個 32 位元數字 = 16 位元組 |

5 億參數 × 16 位元組 = 8 GB，再加上中間計算用的空間，Colab 免費 GPU（約 15 GB）剛好塞得下但很勉強。70 億參數 × 16 = 112 GB，一張消費級顯示卡裝不下。這還只是記憶體，時間也是照參數量算。

### LoRA：只訓練一小塊補丁

LoRA（Low-Rank Adaptation，低秩適應）的做法是：原本的權重矩陣 W **一個數字都不動**，旁邊加一條小路：

```
            輸入 x
              │
      ┌───────┴────────┐
      ▼                ▼
   原本的 W          補丁 A（小）
  （凍結，不訓練）        │
      │                ▼
      │             補丁 B（小）
      │                │
      └───────┬────────┘
              ▼
       輸出 = W·x + B·A·x
```

W 是 896 × 896 的大矩陣（Qwen 0.5B 的一層），有 802,816 個數字。補丁 A 是 8 × 896、B 是 896 × 8，兩個加起來只有 14,336 個數字，是 W 的 1.8%。訓練時只調 A 和 B，W 原封不動。

為什麼這樣做得到？因為「讓模型換個習慣」需要的改動通常很小、很有規律，用兩個小矩陣相乘就能表達。這個「小」就是數學上的「低秩（Low Rank）」。

好處一次列出來：

- **記憶體**：只有補丁需要梯度和優化器狀態，大矩陣只要存一份。
- **檔案**：補丁存起來只有幾 MB 到幾十 MB，原模型共用，可以存很多組補丁換著用。
- **安全**：原模型沒被動過，補丁拿掉就回到原樣。

### rank 與 alpha

LoRA 有兩個數字一定會看到：

- **rank（r）**：補丁的「厚度」。r = 8 表示 A 是 8 列、B 是 8 欄。r 越大補丁越能表達複雜的改動，但參數越多、也越容易背資料。常用 4 到 64，小資料用小的。
- **alpha（α）**：補丁的「音量」。補丁的輸出會乘上 α ÷ r 再加回去。α = 16、r = 8 就是乘 2。一般習慣 α 設成 r 的 1 到 2 倍，先別動它，調 r 和學習率比較有感。

算一個例子：本章用 r = 8、α = 16，對 Qwen2.5-0.5B 所有線性層都貼補丁，補丁總共 4,399,104 個參數，佔全部 498,431,872 的 0.88%。訓練時真的只調這 0.88%。

### 學習率、步數、批次怎麼選

除了 r 和 alpha，還有三個數字每次訓練都要決定。先給一組「小資料、小模型」的安全起點，再說調整的方向：

| 設定 | 本章的值 | 調大會怎樣 | 調小會怎樣 |
|---|---|---|---|
| 學習率 learning_rate | 2e-4 | loss 上下亂跳、甚至變成 nan | loss 掉得很慢，步數要多很多 |
| 步數 max_steps | 60 | 更容易背起來，對新問題照抄舊答案 | 格式還沒學穩 |
| 批次 batch_size | 4 | 每步看更多筆、較穩，但記憶體吃更多 | 記憶體省，但 loss 比較抖 |

一個實用的判斷法：看 loss 曲線。前幾步從 2.5 快速掉到 1 以下是正常；掉到 0.1 附近開始平，就差不多了；如果你看到它掉到 0.01 還在跑，通常已經在背資料，可以把步數砍一半。LoRA 的學習率可以比全參數微調大十倍（全參數常用 1e-5 到 5e-5），因為補丁本來就小、一開始是零，大步走也不會把原模型弄壞。

還有一個常被忽略的數字是 `max_length`。本章設 128 個 token，三行格式的回答約 50 到 70 個 token，夠用；若你的資料是長篇回覆，要把它調大，否則回答會被截掉，模型就學到「講到一半就停」。

### 本章的訓練資料

第 10 章講過資料品質比數量重要，本章用 16 筆就夠讓模型學會一種格式。每筆是「問題 → 三行固定格式的回答」：

```
問：LED 接反會亮嗎？
答：【結論】不會亮。
【理由】LED 是二極體，只允許單方向電流。
【提醒】長腳接正極。<eos>
```

最後那個 `<eos>`（end of sequence，結束符號）非常重要：模型是靠它學會「講完三行就停」。作者第一次跑時漏了它，微調後的模型三行講完還會一直冒出「。」「【提醒】……」停不下來；加上去之後就乾淨了。這種小細節在書上一句話，自己踩到要花半小時。

### 訓練流程五步

```
1. 載入       AutoTokenizer / AutoModelForCausalLM.from_pretrained(模型名)
     ▼
2. 貼補丁     LoraConfig(r, alpha, target_modules) → get_peft_model(model, cfg)
     ▼
3. 整理資料   Dataset.from_list → tokenizer → input_ids / labels
     ▼
4. 訓練       TrainingArguments(max_steps, lr, batch) → Trainer(...).train()
     ▼
5. 存檔       model.save_pretrained("lora-out")   ← 只存補丁
```

`labels` 和 `input_ids` 一樣，表示「學著預測下一個 token」，和第 12 章從零訓練的目標完全相同；padding 的位置設成 −100 表示「這幾格不算分」。

### 評估：格式 vs 知識

微調後一定要比較前後。本章的經驗很有代表性：

- **格式**：16 筆、60 步，模型 100% 學會三行格式，連沒看過的問題也照格式答。
- **知識**：問訓練資料裡有的「麵包為什麼發霉」，答得和資料一樣；問沒有的「鐵為什麼生鏽」，格式對、內容亂講（「因為鐵是導體」）。

這印證第 10 章的決策表：**微調教的是「怎麼說」，不是「知道什麼」**。要它知道新東西，用第 8 章的 RAG 把資料餵進提示；要它用固定風格說話，用微調。兩個常常一起用。

### 合併與匯出，轉 GGUF 給 Ollama

補丁訓練好有兩種用法：

1. **原模型 + 補丁分開載入**（`PeftModel.from_pretrained`）：檔案小、可換補丁，適合自己用。
2. **合併**（`merge_and_unload()`）：把 B·A 加回 W，輸出一個普通的 transformers 模型資料夾（本章合併後 1.9 GB），任何能載入 Hugging Face 模型的工具都能用。

要給 Ollama 用，還要多一步：轉成 GGUF 格式（第 9 章講過，Ollama 和 llama.cpp 用的單檔格式，可以順便量化）。概念與指令如下，本章不實跑（需要另外下載 llama.cpp）：

```bash
# 1. 取得 llama.cpp 的轉換工具（需要 git；在 Colab 也可以做）
git clone https://github.com/ggml-org/llama.cpp
pip install -r llama.cpp/requirements.txt

# 2. 把合併後的模型資料夾轉成 GGUF，順便量化成 Q8_0（約縮小一半）
python llama.cpp/convert_hf_to_gguf.py merged-qwen --outfile my-qwen.gguf --outtype q8_0

# 3. 寫一個 Modelfile 告訴 Ollama 用這個檔
echo 'FROM ./my-qwen.gguf' > Modelfile
ollama create my-qwen -f Modelfile

# 4. 用
ollama run my-qwen
```

轉換工具的參數名稱會隨版本變，跑之前用 `python convert_hf_to_gguf.py --help` 看一眼。

## 動手做

### 活動 11-1：微調一個小模型學會固定格式回覆

**材料／工具**：Google Colab（執行階段 → 變更執行階段類型 → GPU），或自己電腦（CPU 也行，約 2 分鐘）；本章的 `lora_train.py`。

**步驟**：

1. Colab 新筆記本，第一格 `!pip install -q transformers peft datasets accelerate`。
2. 把 `lora_train.py` 整段貼進第二格，執行。第一次會下載模型（約 1 GB），之後會印出 `trainable params`、六行 loss、`LoRA 補丁已存到 lora-out`。
3. 看 loss：從 2.5 左右掉到 0.1 以下代表模型學會了這 16 筆。
4. 左側檔案面板打開 `lora-out`，看補丁檔 `adapter_model.safetensors` 有多大。
5. 把 `pairs` 換成你第 10 章整理的資料（至少 16 筆，格式一致），重跑一次。

**你應該看到／得到**：補丁約 17 MB；loss 曲線一路往下；換成自己的資料後 loss 起點和終點可能不同，但趨勢一樣。

**觀察與記錄**：

| | trainable 參數 | 佔比 | 第一次 loss | 最後 loss | 訓練秒數 | 補丁大小 |
|---|---|---|---|---|---|---|
| 書上資料 | | | | | | |
| 我的資料 | | | | | | |

### 活動 11-2：比較微調前後的輸出

**材料／工具**：活動 11-1 的補丁、本章的 `lora_compare.py`。

**步驟**：

1. 執行 `lora_compare.py`，預設問「為什麼鐵會生鏽？」（訓練資料裡沒有）。
2. 看「微調前」：原模型自由發揮，通常是一段文章。看「微調後」：三行格式。
3. 換三個問題：一個訓練資料裡有的、一個相關但沒有的、一個完全無關的（例如「推薦一部電影」）。
4. 每個問題替「格式對不對」和「內容對不對」各打分。
5. 把 `MAX_STEPS` 改成 10 再訓練一次，重做第 3 步；再改成 200 做一次。

**你應該看到／得到**：格式幾乎一定對；內容只有訓練資料裡有的才對；步數 10 時格式可能還沒學穩，200 時格式更固定但內容不會變好（甚至更常照抄訓練資料）。

**觀察與記錄**：

| 問題 | 在訓練資料裡？ | 微調前（格式／內容） | 微調後（格式／內容） |
|---|---|---|---|
| 為什麼鐵會生鏽？ | 否 | | |
| 麵包為什麼會發霉？ | 是 | | |
| | | | |
| 推薦一部電影 | 否 | | |

## 程式與執行

### 環境

```bash
python -m venv venv
source venv/bin/activate
pip install torch transformers peft datasets accelerate
```

三支程式都用環境變數 `MODEL` 決定模型、`OUT_DIR` 決定補丁位置，不用改程式就能在「極小模型本機 smoke test」和「正式模型」之間切換。

### lora_train.py

```python
# lora_train.py：用 LoRA 微調一個小模型，學會「固定格式回覆」
import os, torch
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model

# 模型名稱用環境變數決定：Colab 用小型開源模型，本機 smoke test 用極小的 tiny-gpt2
MODEL = os.environ.get("MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
MAX_STEPS = int(os.environ.get("MAX_STEPS", "60"))
OUT_DIR = os.environ.get("OUT_DIR", "lora-out")

# 訓練資料：每一筆都是「問題 → 固定格式的回答」
# 格式規則：第一行【結論】、第二行【理由】、第三行【提醒】
pairs = [
    ("冰塊放在桌上會怎樣？", "【結論】會慢慢融化成水。\n【理由】室溫比 0°C 高，熱量流進冰塊。\n【提醒】桌面記得擦乾。"),
    ("LED 接反會亮嗎？", "【結論】不會亮。\n【理由】LED 是二極體，只允許單方向電流。\n【提醒】長腳接正極。"),
    ("為什麼天空是藍色的？", "【結論】因為空氣散射藍光比較多。\n【理由】波長短的光被散射得更厲害。\n【提醒】傍晚偏紅是同一個道理。"),
    ("電池串聯電壓會變嗎？", "【結論】會變大，兩顆 1.5 V 串聯成 3 V。\n【理由】串聯時電壓相加。\n【提醒】正負極要頭尾相接。"),
    ("水燒開是幾度？", "【結論】在平地大約 100°C。\n【理由】這是一大氣壓下水的沸點。\n【提醒】高山上會低一些。"),
    ("麵包放久為什麼會發霉？", "【結論】因為黴菌孢子在上面長大了。\n【理由】麵包有水分和養分，適合黴菌。\n【提醒】發霉的麵包整個丟掉。"),
    ("Python 的 list 和 tuple 差在哪？", "【結論】list 可以改，tuple 不能改。\n【理由】tuple 建立後內容固定。\n【提醒】不會改的資料用 tuple 比較安全。"),
    ("磁鐵為什麼會吸鐵？", "【結論】因為鐵被磁化後和磁鐵互相吸引。\n【理由】鐵裡的小磁區會排整齊。\n【提醒】磁鐵不要靠近信用卡。"),
    ("跑步後為什麼會喘？", "【結論】因為身體需要更多氧氣。\n【理由】肌肉運動消耗氧氣、產生二氧化碳。\n【提醒】運動後慢慢走幾分鐘再停。"),
    ("電阻越大電流越小嗎？", "【結論】電壓固定時，是的。\n【理由】歐姆定律 I = V ÷ R。\n【提醒】電壓改變時要重算。"),
    ("月亮為什麼有圓缺？", "【結論】因為我們看到的被太陽照亮的部分不同。\n【理由】月亮繞地球轉，角度一直變。\n【提醒】月蝕是另一回事。"),
    ("為什麼要存檔？", "【結論】因為沒存檔，關機內容就不見了。\n【理由】記憶體的資料斷電會消失。\n【提醒】養成 Ctrl+S 的習慣。"),
    ("鹽水會導電嗎？", "【結論】會。\n【理由】鹽溶在水裡變成帶電的離子。\n【提醒】純水幾乎不導電。"),
    ("植物晚上也在呼吸嗎？", "【結論】是的，植物一直在呼吸。\n【理由】呼吸作用不需要光。\n【提醒】光合作用才需要光。"),
    ("USB 線插反會壞嗎？", "【結論】USB-C 沒有正反，不會壞。\n【理由】接頭上下對稱設計。\n【提醒】舊的 USB-A 有方向。"),
    ("為什麼要洗手？", "【結論】把手上的細菌和病毒洗掉。\n【理由】手會碰到很多東西再碰嘴巴眼睛。\n【提醒】要搓 20 秒以上。"),
]

tok = AutoTokenizer.from_pretrained(MODEL)
if tok.pad_token is None:
    tok.pad_token = tok.eos_token          # 有些模型沒有 pad token，借用 eos

def build_text(q, a):
    # 把問答拼成模型要學的一整段文字；結尾加上 eos（結束符號），模型才學得會「講完就停」
    return f"問：{q}\n答：{a}{tok.eos_token}"

ds = Dataset.from_list([{"text": build_text(q, a)} for q, a in pairs])

model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.float32)

# LoRA 設定：r 是補丁的「厚度」，alpha 是補丁的「音量」
# target_modules 指定補丁貼在哪些層；"all-linear" 是最省事的寫法
lora_cfg = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05,
                      target_modules="all-linear", task_type="CAUSAL_LM")
model = get_peft_model(model, lora_cfg)
model.print_trainable_parameters()        # 印出「只訓練了多少比例的參數」

def tokenize(batch):
    # 轉成 token id；labels 等於 input_ids，表示「學著預測下一個字」
    enc = tok(batch["text"], truncation=True, max_length=128, padding="max_length")
    # padding 的位置設成 -100，表示「這些不用算損失」；注意 pad 和 eos 可能是同一個 id，所以用 attention_mask 判斷
    enc["labels"] = [[t if m == 1 else -100 for t, m in zip(ids, mask)]
                     for ids, mask in zip(enc["input_ids"], enc["attention_mask"])]
    return enc

tokenized = ds.map(tokenize, batched=True, remove_columns=["text"])

args = TrainingArguments(
    output_dir=OUT_DIR, max_steps=MAX_STEPS, per_device_train_batch_size=4,
    learning_rate=2e-4, logging_steps=max(1, MAX_STEPS // 6), save_strategy="no", report_to="none",
    use_cpu=not torch.cuda.is_available(),  # Colab 有 GPU 就用 GPU
)
trainer = Trainer(model=model, args=args, train_dataset=tokenized)
trainer.train()

model.save_pretrained(OUT_DIR)            # 只存 LoRA 補丁（幾 MB），不存整個模型
tok.save_pretrained(OUT_DIR)
print("LoRA 補丁已存到", OUT_DIR)
```

### lora_compare.py

```python
# lora_compare.py：比較「原模型」與「貼上 LoRA 補丁」後的回答
import os, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

MODEL = os.environ.get("MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
LORA_DIR = os.environ.get("OUT_DIR", "lora-out")
question = os.environ.get("Q", "為什麼鐵會生鏽？")

tok = AutoTokenizer.from_pretrained(MODEL)
base = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.float32)

def ask(m, label):
    # 用和訓練時一樣的格式提問，固定亂數種子讓結果可重現
    torch.manual_seed(0)
    prompt = f"問：{question}\n答："
    ids = tok(prompt, return_tensors="pt")
    out = m.generate(**ids, max_new_tokens=60, do_sample=False,
                     pad_token_id=tok.eos_token_id)
    print(f"--- {label} ---")
    print(tok.decode(out[0][ids["input_ids"].shape[1]:], skip_special_tokens=True))

ask(base, "微調前")
# 把補丁貼回原模型：同一個 base 物件，外面多包一層 LoRA
tuned = PeftModel.from_pretrained(base, LORA_DIR)
ask(tuned, "微調後")
```

### lora_merge.py

```python
# lora_merge.py：把 LoRA 補丁「燙」進原模型，輸出一個普通的完整模型
import os, torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

MODEL = os.environ.get("MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
LORA_DIR = os.environ.get("OUT_DIR", "lora-out")
MERGED = os.environ.get("MERGED", "merged-model")

base = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.float32)
tuned = PeftModel.from_pretrained(base, LORA_DIR)
merged = tuned.merge_and_unload()        # 把 B×A 加回原本的權重矩陣，去掉補丁結構
merged.save_pretrained(MERGED)           # 存成一般的 transformers 模型資料夾
AutoTokenizer.from_pretrained(MODEL).save_pretrained(MERGED)
print("合併完成，存到", MERGED)
print("資料夾內容：", sorted(os.listdir(MERGED)))
```

### 本機 smoke test（極小模型，只確認程式能跑）

先用 `sshleifer/tiny-gpt2`（一個只有 10 萬參數、純粹拿來測試的模型）跑 30 步，確認三支程式都沒寫錯。**這個模型什麼都學不會，輸出是亂的，這是正常的**：

```bash
MODEL=sshleifer/tiny-gpt2 MAX_STEPS=30 OUT_DIR=lora-tiny python lora_train.py
MODEL=sshleifer/tiny-gpt2 OUT_DIR=lora-tiny python lora_compare.py
MODEL=sshleifer/tiny-gpt2 OUT_DIR=lora-tiny MERGED=merged-tiny python lora_merge.py
```

```
trainable params: 512 || all params: 103,226 || trainable%: 0.4960
{'loss': '10.73', 'grad_norm': '0.008991', 'learning_rate': '0.0001733', 'epoch': '1.25'}
{'loss': '10.73', ...（六行都一樣，因為這個模型太小、學不動）
{'train_runtime': '1.053', ...}
LoRA 補丁已存到 lora-tiny
--- 微調前 ---
 stairs stairs stairs stairs stairs ...
--- 微調後 ---
 stairs stairs stairs stairs stairs ...
合併完成，存到 merged-tiny
資料夾內容： ['config.json', 'generation_config.json', 'model.safetensors', 'tokenizer.json', 'tokenizer_config.json']
```

三支程式 10 秒內跑完、沒有錯誤訊息，就可以換正式模型。

### 正式模型：Qwen2.5-0.5B-Instruct（作者本機 CPU 實跑；Colab GPU 輸出相同、只是更快）

```bash
python lora_train.py          # 預設就是 Qwen2.5-0.5B-Instruct、60 步、存到 lora-out
```

```
trainable params: 4,399,104 || all params: 498,431,872 || trainable%: 0.8826
{'loss': '2.494', 'grad_norm': '3.085', 'learning_rate': '0.00017', 'epoch': '2.5'}
{'loss': '1.217', 'grad_norm': '3.362', 'learning_rate': '0.0001367', 'epoch': '5'}
{'loss': '0.5528', 'grad_norm': '2.955', 'learning_rate': '0.0001033', 'epoch': '7.5'}
{'loss': '0.2272', 'grad_norm': '1.42', 'learning_rate': '7e-05', 'epoch': '10'}
{'loss': '0.1158', 'grad_norm': '1.619', 'learning_rate': '3.667e-05', 'epoch': '12.5'}
{'loss': '0.08761', 'grad_norm': '1.39', 'learning_rate': '3.333e-06', 'epoch': '15'}
{'train_runtime': '103.8', 'train_samples_per_second': '2.313', 'train_steps_per_second': '0.578', 'train_loss': '0.7825', 'epoch': '15'}
LoRA 補丁已存到 lora-out
```

補丁 `adapter_model.safetensors` 實測 17.6 MB（整個資料夾含 tokenizer 28 MB）。注意 `epoch: 15`：16 筆資料、每批 4 筆，60 步等於把資料看了 15 遍。

```bash
python lora_compare.py                                # 問訓練資料裡沒有的問題
```

```
--- 微調前 ---
因為鐵在氧化時，會產生一種叫做「鉻」的元素。當鐵與氧反應時，會生成一種叫做「鐵銫」的化合物。這種化合物會吸收光線，形成一種叫做「鉻」的元素。鉻是黑色的，所以
--- 微調後 ---
【結論】因為铁是導體。
【理由】電壓一致的兩點間电压降大，導體斷開。
【提醒】高壓電切斷。
```

```bash
Q="為什麼要戴安全帽？" python lora_compare.py
```

```
--- 微調前 ---
安全帽是防止頭部受到外力傷害的裝備，可以保護頭部免受碰撞、砸擊等外力傷害。在工作或場所中，佩戴安全帽可以有效避免頭部受到物理損傷和人身安全事故。

請問如何正確佩戴安全
--- 微調後 ---
【結論】因為撞到你會疼。
【理由】頭部有許多小血管。
【提醒】是兩 halves 關。
```

讀這兩組輸出：

- **格式**：微調後 100% 三行、講完就停。微調前則是長篇大論，甚至自己開始問下一題（「請問如何正確佩戴安全」）。
- **內容**：鐵生鏽那題微調後完全亂講。原因很簡單——16 筆資料裡沒有生鏽，模型只學到「怎麼排版」。安全帽那題結論勉強對、理由亂、提醒出現簡體字和英文，說明 0.5B 的模型本來中文就不穩，微調沒辦法補足。
- **本機 vs Colab**：這組數字是作者在 Apple Silicon 筆電 CPU 跑的；Colab T4 GPU 跑同一支程式，loss 數值幾乎相同（亂數種子一樣），訓練時間從 104 秒縮到約 15 秒。

```bash
python lora_merge.py          # 合併成完整模型
```

```
合併完成，存到 merged-model
資料夾內容： ['chat_template.jinja', 'config.json', 'generation_config.json', 'model.safetensors', 'tokenizer.json', 'tokenizer_config.json']
```

合併後 `model.safetensors` 1.98 GB（float32）。對比補丁 17.6 MB，就知道為什麼平常只存補丁。

## 常見錯誤與迷思

- **微調後模型「知道」了新東西 → 錯 → 16 筆、60 步只夠學格式與語氣。要新知識用 RAG（第 8 章）或幾千筆高品質資料＋更多步數，而且仍然容易幻覺。**
- **loss 越低越好，多跑幾百步 → 不一定 → 小資料上 loss 掉到 0.01 通常是背起來了，模型會把任何問題都答成訓練資料裡最像的那一筆。本章 60 步、loss 0.09 就夠。**
- **r 越大越好 → 不對 → r = 64 的補丁在 16 筆資料上只會更快背熟。小資料用 4–8，幾千筆再考慮 16–32。**
- **微調後輸出停不下來、一直重複 → 幾乎都是訓練文字結尾沒加 eos → 加 `tok.eos_token`，並確認 labels 沒把它遮成 −100。**
- **`CUDA out of memory` → Colab 記憶體不夠 → 把 `per_device_train_batch_size` 降到 1、`max_length` 降到 64，或載入時用 `dtype=torch.bfloat16`。**
- **本機 smoke test 用 tiny-gpt2 輸出是 "stairs stairs" → 正常 → 那個模型只有 10 萬參數、隨機初始化，目的只是確認程式不會當掉。**
- **載入補丁時 `size mismatch` → 補丁和原模型對不上 → 訓練和載入要用同一個 `MODEL`；換了模型就要重新訓練補丁。**

## 想一想

1. Qwen2.5-0.5B 全部 498,431,872 個參數，若全參數微調，光權重、梯度、優化器狀態就要多少 GB？本章 LoRA 只訓練 4,399,104 個，同樣算法要多少？

<details><summary>參考答案</summary>

全參數：498,431,872 × 16 位元組 ≈ 7.97 GB。LoRA：補丁 4,399,104 × 16 ≈ 70 MB，加上原權重一份（498,431,872 × 4 ≈ 2 GB，只讀不調）≈ 2.07 GB。差不多省了四分之三，模型越大省越多。

</details>

2. 一個 1024 × 1024 的權重矩陣，r = 4 和 r = 16 的 LoRA 補丁各有幾個參數？各是原矩陣的百分之幾？

<details><summary>參考答案</summary>

原矩陣 1,048,576。r = 4：A 是 4×1024、B 是 1024×4，共 8,192 個，0.78%。r = 16：共 32,768 個，3.1%。r 乘 4 倍，補丁也乘 4 倍，但還是不到原矩陣的 5%。

</details>

3. 本章 16 筆資料、批次 4、60 步 = 15 個 epoch。如果你有 400 筆資料，想同樣看 3 遍，`MAX_STEPS` 要設多少？

<details><summary>參考答案</summary>

每個 epoch = 400 ÷ 4 = 100 步，3 遍 = 300 步。資料變多時 epoch 數可以少一點（3 遍通常夠），因為每一遍看到的東西更多樣。

</details>

4. 微調後問「為什麼鐵會生鏽」答成「因為鐵是導體」。從第 10 章的決策表看，這個問題應該用哪種方法解決？寫出具體做法。

<details><summary>參考答案</summary>

用 RAG 補知識：把一份正確的生鏽說明放進向量庫，提問時檢索出來放進提示，再要求模型用三行格式回答。微調負責格式、RAG 負責內容。也可以兩者疊加：用微調後的模型做 RAG 的生成端。

</details>

5. 你想讓模型同時會兩種格式：「三行格式」和「表格格式」。用 LoRA 有哪兩種做法？各有什麼優缺點？

<details><summary>參考答案</summary>

做法一：兩組資料混在一起、問題裡標明要哪種格式（例如開頭加「[三行]」或「[表格]」），訓練一組補丁。優點是一個模型搞定，缺點是資料要平衡、模型要學會看標記。做法二：訓練兩組補丁，用的時候依需求載入其中一組。優點是各自乾淨、互不干擾，缺點是切換要重新載入補丁。LoRA 的補丁很小，做法二很常見。

</details>

6. 開放挑戰：把合併後的模型轉成 GGUF、匯入 Ollama，然後用第 8 章的 RAG 程式把生成端換成它。測 10 個問題，記錄「格式正確率」和「內容正確率」，和原本的 Ollama 模型比較。你預期哪個數字會變好、哪個不會？

<details><summary>參考答案</summary>

格式正確率會明顯變好（微調的目的）；內容正確率主要取決於檢索有沒有找對資料，微調不會讓它變好，甚至可能稍差（小模型微調後有時更固執）。若內容正確率掉很多，表示微調步數太多或資料太單一，模型學會「照格式亂講」而不看檢索到的內容；解法是在訓練資料裡也放幾筆「附參考資料的問答」，教它看資料答。

</details>

## 本章小結

- 全參數微調每個參數約要 16 位元組的記憶體（權重、梯度、兩個優化器狀態），5 億參數就 8 GB。
- LoRA 凍結原權重 W，在旁邊加 B·A 兩個小矩陣，只訓練它們；本章補丁佔 0.88% 的參數、17.6 MB。
- r 是補丁厚度（小資料用 4–8），alpha 是音量（設成 r 的 1–2 倍），學習率 2e-4 是常見起點。
- 訓練文字結尾一定要加 eos，模型才會學到「講完就停」。
- 16 筆資料、60 步、CPU 104 秒，模型就 100% 學會三行格式；但內容沒有學到，微調教「怎麼說」不教「知道什麼」。
- 評估一定做前後對照，分開記錄格式與內容。
- 補丁可以分開載入或 `merge_and_unload()` 合併；要給 Ollama 用，再用 llama.cpp 的工具轉 GGUF 並寫 Modelfile。
- 本機先用 tiny-gpt2 跑 smoke test 確認程式沒錯，再換正式模型，省下等待和除錯時間。

## 名詞表

| 中文 | 英文 | 一句話解釋 |
|---|---|---|
| 全參數微調 | Full Fine-tuning | 模型所有參數都拿來訓練，記憶體與時間都最貴。 |
| 低秩適應 | LoRA, Low-Rank Adaptation | 凍結原權重，只訓練旁邊兩個小矩陣的微調法。 |
| 秩 | Rank, r | LoRA 補丁的厚度，決定補丁參數量與表達力。 |
| alpha | LoRA alpha | 補丁輸出的縮放倍率（乘上 alpha ÷ r）。 |
| 目標模組 | target_modules | 要貼補丁的層；"all-linear" 表示所有線性層。 |
| 凍結 | Freeze | 參數不參與訓練，不算梯度。 |
| 優化器狀態 | Optimizer State | AdamW 為每個參數多記的兩個數字，佔訓練記憶體一半。 |
| 結束符號 | EOS, End of Sequence | 告訴模型「到此為止」的特殊 token。 |
| 填充 | Padding | 把長短不一的句子補到同樣長度，補的位置不算損失。 |
| 標籤 | Labels | 訓練時要預測的目標，語言模型就是「下一個 token」。 |
| 訓練步 | Step | 用一個批次更新一次參數。 |
| 週期 | Epoch | 把整份資料看過一遍。 |
| 合併 | merge_and_unload | 把補丁加回原權重，輸出普通模型。 |
| 補丁檔 | Adapter | LoRA 存出來的小檔案，載入原模型後疊上去用。 |
| GGUF | GGUF | llama.cpp 與 Ollama 用的單檔模型格式，可含量化。 |
| 量化 | Quantization | 把參數從 32 位元縮成 8 或 4 位元，檔案小、跑得快。 |
| Modelfile | Modelfile | 告訴 Ollama 用哪個 GGUF 檔與設定的文字檔。 |
| 煙霧測試 | Smoke Test | 用極小的設定先跑一遍確認程式不會當掉。 |
