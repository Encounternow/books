# 第 3 章　Skill

## 本章目標

學完這一章，你會：

- 用一句話說出 Skill 是什麼：給 AI 的操作手冊，需要時才翻開。
- 寫出一個合格的 `SKILL.md`：frontmatter 的 `name` 與 `description`、正文的步驟、附檔怎麼放。
- 在 Claude Code 裡用 `/名稱` 手動觸發，也讓它依描述自動觸發。
- 判斷一個 Skill 為什麼不可靠（觸發描述太模糊、正文太長、規則互相矛盾），並修好它。
- 分清楚 Claude Code 的 Skill 和 Claude API 的 Agent Skills 是兩件事。

## 開場：每次都要重講一遍

小安用 Claude Code 幫她寫實驗報告已經三次了。每次她都要重打同一段話：「報告要有目的、器材、步驟、數據表、討論、結論六段；數據要算平均到小數第一位；不要幫我編數據；全部用繁體中文。」第四次她想：「這段話能不能存起來，以後說『寫實驗報告』它就自己照做？」

她試過把這段放在 `CLAUDE.md`（第 5 章會講，那是專案的「常駐說明」）。可是這樣每次對話都會讀到這段，就算她只是想問一個 Python 語法。而且她還有「整理筆記」、「檢查 Arduino 程式」等好幾套規則，全塞進去會變成一本厚厚的手冊，AI 反而抓不到重點。

她要的是**按需要翻開的手冊**：平常收在抽屜裡，只佔一行目錄；說到「實驗報告」時才整本拿出來照做。這就是 Skill。

## 核心概念

### Skill 是什麼：給 AI 的操作手冊

**Skill（技能）**是一個資料夾，裡面有一份 `SKILL.md`，寫著「什麼時候用、怎麼做、要注意什麼」。AI 平常只看到每個 Skill 的名字和一句描述（像目錄），等到任務符合描述時，才把整份手冊讀進來照著做。

拿餐廳打比方：第 1 章的 system prompt 像是員工的基本守則（永遠有效），Skill 像是「處理客訴的 SOP」、「辦生日派對的流程」，平常掛在牆上只看標題，遇到了才拿下來翻。

| | system prompt / CLAUDE.md | Skill |
|---|---|---|
| 什麼時候讀 | 每次對話都讀 | 符合描述時才讀 |
| 適合放什麼 | 短、通用的規則（語言、語氣、專案背景） | 長、特定任務的步驟與範本 |
| 佔多少上下文 | 全文 | 平常只佔一行描述 |
| 數量 | 一份 | 可以很多份 |

Skill 有兩種，本書以第一種為主：

1. **Claude Code 的 Skill**：資料夾放在專案的 `.claude/skills/<名稱>/`，用 `/<名稱>` 呼叫，或讓 Claude Code 依描述自動觸發。給人在終端機用。
2. **Claude API 的 Agent Skills**：透過 `client.skills` 上傳或使用 Anthropic 內建的 Skill（例如做簡報、做試算表），在 API 呼叫裡搭配程式執行沙盒使用。給程式用。本章最後一節帶過。

### SKILL.md 的格式

一個最小的 Skill 長這樣：

```
.claude/
└── skills/
    └── lab-report/
        ├── SKILL.md           ← 必要，檔名大小寫固定
        └── templates/
            └── report.md      ← 選用的附檔
```

`SKILL.md` 分兩部分。開頭兩個 `---` 之間叫 **frontmatter（前置資料）**，是給程式讀的設定；後面是給 AI 讀的正文。

```
---
name: lab-report
description: 把實驗的原始數據與觀察整理成一份完整的實驗報告（Markdown）。當使用者提到「寫實驗報告」「整理實驗數據」時使用。
---

# 寫實驗報告
（正文：什麼時候用、步驟、規則）
```

frontmatter 兩個必要欄位：

| 欄位 | 規則 | 作用 |
|---|---|---|
| `name` | 小寫英文、數字、連字號，**要跟資料夾同名** | 決定 `/name` 這個指令叫什麼 |
| `description` | 一到三句，寫「做什麼」加「什麼時候用」 | **自動觸發的唯一依據**；AI 平常只看得到這行 |

官方文件還有其他選填欄位（例如限制這個 Skill 能用哪些工具），本書只用這兩個就夠了。

正文沒有硬性格式，但好用的 Skill 通常有四段：**什麼時候用**（含什麼時候不要用）、**步驟**（編號，動詞開頭）、**規則**（不要做什麼）、**附檔**（範本、範例、檢查表，用相對路徑指過去，例如 `templates/report.md`）。AI 會在需要時自己去讀附檔，所以 `SKILL.md` 本身保持短。

### 放哪裡、怎麼觸發

Skill 資料夾有兩個地方可以放：

- **專案層** `.claude/skills/`：跟專案一起進 git，同一個專案的人都能用。
- **個人層** `~/.claude/skills/`：你自己所有專案都能用，例如「我的 commit 訊息格式」。

在專案資料夾啟動 `claude` 後，有兩種觸發方式：

1. **手動**：輸入 `/lab-report` 加上你的話，例如 `/lab-report 這是我的電阻實驗數據：……`。
2. **自動**：直接說「幫我把這些數據寫成實驗報告」，Claude Code 看到你的話符合 `description`，就會自己載入這個 Skill。

兩種都要 `description` 寫得好才靠得住。你可以用 `claude --help` 看到幾個相關選項：`--disable-slash-commands` 會關掉所有 Skill，`--safe-mode` 會把 CLAUDE.md、Skill、外掛全部停用，用來排查「是不是哪個 Skill 害的」。

### 怎麼讓 Skill 可靠

寫 Skill 最常見的失敗不是「AI 做錯」，而是「AI 根本沒用它」或「用了但沒照做」。四個原則：

**1. description 寫觸發情境，不要只寫功能。** 「實驗報告產生器」太模糊；「當使用者提到『寫實驗報告』『整理實驗數據』『把量測結果寫成報告』時使用」才有用。把使用者**會怎麼說**寫進去。

**2. 寫出「什麼時候不要用」。** 「若只是問單一數據的意思，不要用這個 Skill」能避免它過度觸發。

**3. 短。** `SKILL.md` 超過一兩百行，AI 會漏看中間的規則。範本、長範例、對照表放附檔，正文只留步驟和規則。

**4. 規則要可檢查、不互相矛盾。** 「平均保留到小數第 1 位」可檢查；「數據要漂亮」不行。寫完自己讀一遍，想像你是第一次看到的新員工，照著做得出來嗎？

一個檢查用的小表：

```
[ ] name 跟資料夾同名、全小寫
[ ] description 有「做什麼」+「當……時使用」
[ ] 有寫什麼時候不要用
[ ] 步驟有編號、每步一個動作
[ ] 正文不超過 150 行，長的東西在附檔
[ ] 規則每條都能用「有／沒有做到」判斷
```

### API 端的 Agent Skills（一節帶過）

Claude API 也有 Skill，但用法不同：它是給**程式呼叫時**掛上的能力包，裡面可以有腳本與資源，模型在 Anthropic 的沙盒裡執行程式來使用它。Anthropic 內建了幾個（例如做 `.pptx` 簡報、`.xlsx` 試算表），你也能用 `client.skills.create()` 上傳自己的。用法是在 `client.beta.messages.create()` 裡加 `container={"skills": [...]}`，並開啟 `code_execution` 工具：

```python
"""API 端的 Agent Skills：列出可用的 Skill，再在一次呼叫裡掛上 pptx Skill 請模型做簡報。"""
import anthropic

client = anthropic.Anthropic()

# 1. 列出帳號裡可用的 Skill（Anthropic 內建的 + 你自己上傳的）
for skill in client.skills.list():
    print("可用 Skill：", skill.id)

# 2. 在 container.skills 掛上想用的 Skill，並開啟 code_execution 讓它在沙盒裡跑
response = client.beta.messages.create(
    model="claude-opus-5-5",
    max_tokens=16000,
    betas=["code-execution-2025-08-25"],
    container={"skills": [{"type": "anthropic", "skill_id": "pptx", "version": "latest"}]},
    tools=[{"type": "code_execution_20260521", "name": "code_execution"}],
    messages=[{"role": "user", "content": "做一份 3 頁的簡報，介紹台灣夜市的歷史。"}],
)

# 回覆裡的文字說明直接印；產生的檔案會以 file_id 形式出現，要再用 Files API 下載
for block in response.content:
    if block.type == "text":
        print(block.text)
```

預期輸出：先列出 `pptx`、`xlsx`、`docx` 等內建 Skill 的 id，然後是模型的說明文字，例如「已產生 3 頁簡報……」。產生的檔案要用 Files API 下載，本書不深入；第 5 章會解釋為什麼程式端通常用 MCP 或自己的工具而不是 Agent Skills。

兩種 Skill 的核心想法一樣：**把一套做法寫成檔案，需要時才載入**。差別只在誰載入：Claude Code 自己讀本機資料夾，API 則在雲端沙盒載入。

## 動手做

### 活動 3-1：寫一個「實驗報告」Skill 並在 Claude Code 觸發

**材料／工具**：裝好並登入的 Claude Code、一個專案資料夾（例如 `~/lab`）、一組你自己量過的數據（沒有的話用下面的電阻數據）。

**步驟**：

1. 建立資料夾：`mkdir -p ~/lab/.claude/skills/lab-report/templates`，然後 `cd ~/lab`。
2. 建立 `.claude/skills/lab-report/SKILL.md`，內容如下：

```
---
name: lab-report
description: 把實驗的原始數據與觀察整理成一份完整的實驗報告（Markdown）。當使用者提到「寫實驗報告」「整理實驗數據」「幫我把量測結果寫成報告」時使用。
---

# 寫實驗報告

## 什麼時候用
使用者給你一組量測數據（表格、CSV 或口述）並想要一份報告時。若只是問單一數據的意思，不要用這個 Skill。

## 步驟
1. 先讀 `templates/report.md`，報告一律照這個骨架。
2. 把使用者給的數據整理成 Markdown 表格；欄位要有單位。若數據少於 3 筆，先問使用者是否還有更多資料。
3. 算出每組的平均值；平均值保留到小數第 1 位，並在表格下方寫出算式（例如 `(12.1+12.3+12.2)/3 = 12.2`）。
4. 「結果與討論」要對照使用者的預期（或教科書的理論值），指出差異可能的來源：量測工具、環境、操作。
5. 「結論」最多三句，不要加入數據以外的推測。
6. 報告存成 `report.md` 放在目前資料夾，然後用一句話告訴使用者檔案在哪。

## 規則
- 全文繁體中文，科學名詞第一次出現附英文。
- 不要幫使用者編造沒給的數據；缺的欄位寫「未量測」。
- 不要改使用者的原始數字。
```

3. 建立附檔 `.claude/skills/lab-report/templates/report.md`：

```
# 實驗報告：（實驗名稱）

- 日期：
- 實驗者：

## 一、目的
（一句話）

## 二、器材與材料
- 

## 三、步驟
1. 

## 四、數據與計算
| 組別 | 量測 1 | 量測 2 | 量測 3 | 平均 |
|---|---|---|---|---|

## 五、結果與討論

## 六、結論
```

4. 在 `~/lab` 啟動 `claude`。**手動觸發**：輸入

   `/lab-report 歐姆定律實驗。電阻 100Ω，電壓 3V 時電流量到 29.8、30.1、30.0 mA；電壓 6V 時 59.5、60.2、60.1 mA。理論值 30 與 60 mA。`

5. 看它做了什麼：應該先讀範本、列表格、算平均（29.97 → 30.0、59.93 → 59.9）、寫討論、存成 `report.md`。打開 `report.md` 檢查六段是否齊全、平均是否正確。
6. **自動觸發**：開新對話（或輸入 `/clear`），這次不打 `/lab-report`，直接說「幫我把這些量測結果寫成報告：……（同樣的數據）」。觀察它有沒有自己載入 Skill（輸出格式應該跟第 5 步一樣）。
7. 對照測試：問「30 mA 是多少安培？」，確認它**沒有**啟動 Skill 去寫整份報告。
8. 挑戰：把 description 改成只有「實驗報告」四個字，重做第 6 步，看自動觸發是否變得不穩。改回來。

**你應該看到**：第 5 步產生的 `report.md` 大致如下（預期輸出，文字會不同）：

```
# 實驗報告：歐姆定律

- 日期：2026-10-14
- 實驗者：未量測

## 四、數據與計算
| 組別 | 量測 1 (mA) | 量測 2 (mA) | 量測 3 (mA) | 平均 (mA) |
|---|---|---|---|---|
| 3V | 29.8 | 30.1 | 30.0 | 30.0 |
| 6V | 59.5 | 60.2 | 60.1 | 59.9 |

(29.8+30.1+30.0)/3 = 30.0；(59.5+60.2+60.1)/3 = 59.9

## 五、結果與討論
兩組平均與理論值 30、60 mA 的差距都在 0.2 mA 以內……
```

注意「實驗者」寫了「未量測」而不是亂編名字，這是規則第二條在起作用。

**觀察與記錄**：

| 測試 | 有載入 Skill 嗎 | 六段齊全嗎 | 平均算對嗎 | 有編造數據嗎 |
|---|---|---|---|---|
| /lab-report 手動 | | | | |
| 自動觸發 | | | | |
| 「30 mA 是多少安培」 | | | | |
| description 改短後 | | | | |

### 活動 3-2：為家裡的筆記規則寫一個 Skill

**材料／工具**：同上。這個 Skill 放在**個人層** `~/.claude/skills/`，所有專案都能用。

**步驟**：

1. `mkdir -p ~/.claude/skills/home-notes`，建立 `SKILL.md`（注意：這個檔案裡面自己也有一段 ``` 程式區塊，照抄即可）：

````
---
name: home-notes
description: 依照我們家的筆記規則，在 notes/ 資料夾新增或整理一篇筆記。當使用者說「記一下」「幫我做筆記」「整理成筆記」時使用。
---

# 家裡的筆記規則

## 檔案位置與命名
- 所有筆記放在 `notes/`，檔名格式 `YYYY-MM-DD-主題.md`，主題用中文、不含空白，例如 `2026-10-14-電阻實驗.md`。
- 同一天同主題已有檔案時，附加在原檔案最後，不要開新檔。

## 每篇筆記的固定格式
```
# 主題

- 日期：YYYY-MM-DD
- 標籤：#標籤1 #標籤2（1 到 3 個，從下面的清單挑）

## 重點
- （3 到 5 條，每條一行）

## 待辦
- [ ] （沒有就寫「無」）
```

## 可用標籤
#學校 #實驗 #程式 #家事 #採買 #健康

## 規則
- 使用者講的內容只「整理」不「擴寫」；不確定的地方用（？）標出來問使用者。
- 寫完後列出：檔案路徑、用了哪些標籤、有幾條待辦。
````

2. 在任何專案資料夾（例如 `~/lab`）啟動 `claude`，說：「記一下：今天跟媽媽討論週末採買，要買洗衣精、米、還有阿公的血壓藥，記得先問藥局有沒有貨。」
3. 檢查 `notes/` 裡是不是多了 `2026-10-14-週末採買.md`（日期是你執行的那天），標籤是不是從清單挑的（應該是 #採買 #家事 或加 #健康），待辦是不是有「問藥局有沒有貨」。
4. 再說一次「記一下：採買還要加牙膏」，確認它**附加**在同一個檔案而不是開新檔。
5. 故意講一句模糊的話：「記一下那個東西明天要用」，看它有沒有用（？）標出來問你，而不是自己編。
6. 挑戰：把你家真正的規則寫進去（例如誰負責什麼、固定的購物清單格式），用一週，每天記錄一次它有沒有照做。

**你應該看到**（預期輸出）：

```
已建立 notes/2026-10-14-週末採買.md
標籤：#採買 #家事 #健康
待辦：1 條（先問藥局阿公的血壓藥有沒有貨）
```

**觀察與記錄**：

| 日期 | 你說的話 | 檔名正確嗎 | 標籤來自清單嗎 | 附加 or 新檔 | 有亂擴寫嗎 |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |

## 程式與執行：Skill 格式檢查器

Skill 寫多了，常常忘記 name 跟資料夾對不上、description 漏寫觸發情境。這個小程式掃描專案的 `.claude/skills/`，把問題列出來。它不需要 API 金鑰，純粹讀檔案。

```python
"""檢查 .claude/skills/ 底下每個 Skill 的格式。用法：python check_skills.py 專案資料夾"""
import sys
from pathlib import Path

MAX_DESC = 1024  # description 太長會占掉上下文，也很難被正確觸發


def parse_frontmatter(text: str) -> dict | None:
    """讀出檔案開頭兩個 --- 之間的 key: value；格式不對就回 None。"""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    meta = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return meta
        if ":" in line:
            key, value = line.split(":", 1)
            meta[key.strip()] = value.strip()
    return None  # 沒找到結尾的 ---


def check(skill_dir: Path) -> list[str]:
    """回傳這個 Skill 的問題清單，空清單代表通過。"""
    problems = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return ["缺少 SKILL.md（注意大小寫）"]
    text = skill_md.read_text(encoding="utf-8")
    meta = parse_frontmatter(text)
    if meta is None:
        return ["frontmatter 格式錯誤：開頭要有 ---，結尾也要有 ---"]

    # name 必須存在，而且要跟資料夾同名，才能用 /名稱 呼叫
    if "name" not in meta:
        problems.append("frontmatter 缺 name")
    elif meta["name"] != skill_dir.name:
        problems.append(f"name「{meta['name']}」和資料夾名「{skill_dir.name}」不一致")

    # description 是觸發依據：要有、不能太長、最好寫出「什麼時候用」
    desc = meta.get("description", "")
    if not desc:
        problems.append("frontmatter 缺 description（這是自動觸發的依據）")
    elif len(desc) > MAX_DESC:
        problems.append(f"description 太長（{len(desc)} 字）")
    elif not any(k in desc for k in ("當", "時使用", "用於", "when", "Use when")):
        problems.append("description 沒寫觸發情境（建議加「當使用者……時使用」）")

    # 正文太長代表該拆成附檔
    body_lines = len(text.splitlines())
    if body_lines > 300:
        problems.append(f"正文 {body_lines} 行，建議拆成附檔，SKILL.md 只留步驟")
    return problems


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    skills_dir = root / ".claude" / "skills"
    if not skills_dir.is_dir():
        print(f"找不到 {skills_dir}")
        sys.exit(1)

    print(f"{'Skill':<14}{'狀態':<6}說明")
    all_ok = True
    for d in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        problems = check(d)
        status = "通過" if not problems else "有問題"
        all_ok = all_ok and not problems
        print(f"{d.name:<14}{status:<6}{'；'.join(problems) or '-'}")
    sys.exit(0 if all_ok else 2)


if __name__ == "__main__":
    main()
```

**怎麼跑**：存成 `check_skills.py`，在有 `.claude/skills/` 的專案執行 `python check_skills.py .`。

**輸出**（作者在含有 `lab-report` 與 `home-notes` 的專案實際執行）：

```
Skill         狀態    說明
home-notes    通過    -
lab-report    通過    -
```

故意做一個壞的：資料夾叫 `Bad-Name`，`SKILL.md` 裡 `name: badname` 且沒有 description，再跑一次：

```
Skill         狀態    說明
Bad-Name      有問題   name「badname」和資料夾名「Bad-Name」不一致；frontmatter 缺 description（這是自動觸發的依據）
```

程式結尾的 `sys.exit(2)` 讓它可以放進自動化流程：檢查沒過就不要 commit。這個程式本身也可以變成一個 Skill——「當使用者說『檢查 skill』時，執行 `python check_skills.py .` 並解釋結果」。

## 常見錯誤與迷思

- **「我放了 SKILL.md 但 `/名稱` 找不到」** → 路徑或檔名錯：要在 `.claude/skills/<名稱>/SKILL.md`，`SKILL.md` 大小寫固定，`name` 要跟資料夾同名；而且要在專案資料夾啟動 `claude`。 → 用本章的檢查器跑一次。
- **「description 寫得越長越詳細越好」** → description 是目錄，每次對話都會載入，太長反而稀釋重點、浪費上下文。 → 一到三句，寫「做什麼」+「當……時使用」，細節放正文。
- **「Skill 就是把一堆提示貼進去」** → 沒有步驟、沒有「不要做什麼」的 Skill 跟隨口講沒兩樣。 → 編號步驟、可檢查的規則、不該用的情境。
- **「它用了 Skill 但沒照第 7 條做」** → 正文太長，中間的規則被漏看；或規則互相矛盾。 → 砍短，長內容放附檔；矛盾的規則二選一。
- **「Skill 和 CLAUDE.md 一樣，放哪都行」** → CLAUDE.md 每次都讀，適合短的通用規則；Skill 需要時才讀，適合長的特定任務。 → 通用放 CLAUDE.md，任務放 Skill。
- **「Claude Code 的 Skill 可以直接拿到 API 用」** → 兩者格式思路相同但載入方式不同：API 端要用 `client.skills` 上傳並搭配程式執行沙盒。 → 分清楚你在哪個環境。
- **「Skill 裡叫它執行任何指令都沒關係」** → Skill 正文是指令，會被 AI 照做；寫了「刪掉所有舊檔」它真的會做。 → 破壞性動作寫「先列出來問使用者確認」。

## 想一想

1. 用自己的話說：為什麼「把規則放在 Skill」比「每次對話都重講」或「全塞進 CLAUDE.md」好？

<details><summary>參考答案</summary>

重講每次都要打字且容易漏；全塞進 CLAUDE.md 會讓每次對話都載入所有規則，佔上下文又讓 AI 抓不到重點。Skill 平常只佔一行描述，符合任務時才載入整份，兼顧「不用重講」和「不浪費」。

</details>

2. 下面兩個 description，哪個比較容易被正確觸發？為什麼？
   A：`實驗報告工具`
   B：`把量測數據整理成實驗報告。當使用者提到「寫實驗報告」「整理實驗數據」時使用；只問單一數據的意思時不用。`

<details><summary>參考答案</summary>

B。它寫了使用者會怎麼說（觸發詞）、也寫了什麼時候不要用。A 只有名詞，AI 很難判斷「幫我看這組數據」算不算要用它。

</details>

3. 你的 `SKILL.md` 有 400 行，包含三個完整的報告範例。AI 常常漏掉第 12 條規則。該怎麼改？

<details><summary>參考答案</summary>

把三個範例搬到 `examples/` 附檔，正文只留步驟與規則並在步驟裡寫「需要時參考 examples/」。正文縮到一百行內，規則集中在一段，AI 就不容易漏看。

</details>

4. `lab-report` 的規則說「不要編造沒給的數據」。如果使用者只給了兩筆量測，Skill 的步驟 2 會怎麼做？為什麼這樣設計？

<details><summary>參考答案</summary>

步驟 2 說「若數據少於 3 筆，先問使用者是否還有更多資料」，所以它會先問而不是補一筆假的。這樣設計是因為實驗報告裡假數據比缺數據嚴重得多；寧可多問一句。

</details>

5. 活動 3-2 的 Skill 放在 `~/.claude/skills/`，而 3-1 放在專案的 `.claude/skills/`。什麼情況下該選哪一個？

<details><summary>參考答案</summary>

跟特定專案綁在一起、要跟同組的人共享的（實驗報告格式、這個專案的程式風格）放專案層並進 git；跟你個人習慣有關、每個專案都要用的（筆記規則、commit 訊息格式）放個人層。

</details>

6. 開放挑戰：設計一個「檢查 Arduino 程式」的 Skill。想一想 description 要寫哪些觸發詞、步驟裡要檢查哪五件事（例如 `pinMode` 有沒有設、`delay` 會不會卡住、變數型別會不會溢位）、哪些該放附檔。寫出來後用本章的檢查器跑一次。

<details><summary>參考答案</summary>

參考設計：`name: arduino-check`；description「檢查 Arduino（.ino）程式的常見錯誤並給修改建議。當使用者說『幫我看 Arduino 程式』『這段 .ino 哪裡有問題』『為什麼燈不亮』時使用。」步驟：(1) 讀整個檔案；(2) 檢查 setup 裡每個用到的腳位都有 pinMode；(3) 找出 loop 裡超過 1000 ms 的 delay 並建議用 millis；(4) 檢查 int 存毫秒會不會溢位（建議 unsigned long）；(5) 檢查 Serial.begin 有沒有呼叫；(6) 用表格列出「行號、問題、建議」，不要直接改檔案，除非使用者說要。附檔：`checklist.md`（完整檢查清單）、`examples/blink-bad.ino` 與 `blink-good.ino`。可以連結《動手玩電》的對應章節。

</details>

## 本章小結

- Skill 是給 AI 的操作手冊：平常只載入一行描述，任務符合時才讀整份。
- Claude Code 的 Skill 放在 `.claude/skills/<name>/SKILL.md`（專案層）或 `~/.claude/skills/`（個人層）。
- frontmatter 必要欄位：`name`（跟資料夾同名）、`description`（自動觸發的唯一依據）。
- 正文寫四段：什麼時候用（含不要用）、編號步驟、規則、附檔；保持短，長內容放附檔。
- 觸發方式：手動 `/name`，或依 description 自動；description 要寫使用者會怎麼說。
- 可靠的關鍵：觸發情境明確、正文短、規則可檢查且不矛盾、破壞性動作先確認。
- API 端的 Agent Skills 是另一套：`client.skills` + `container={"skills": [...]}` + 程式執行沙盒。
- 用本章的 `check_skills.py` 在 commit 前檢查格式。

## 名詞表

| 中文 | 英文 | 一句話解釋 |
|---|---|---|
| 技能 | Skill | 給 AI 的操作手冊資料夾，需要時才載入 |
| 前置資料 | frontmatter | `SKILL.md` 開頭兩個 `---` 之間的設定，含 name 與 description |
| 觸發描述 | description | 一到三句說明做什麼、什麼時候用；自動觸發的依據 |
| 斜線指令 | slash command | 在 Claude Code 輸入 `/名稱` 手動啟動一個 Skill |
| 自動觸發 | auto-invocation | AI 依描述判斷任務符合，自己載入 Skill |
| 附檔 | supporting files | Skill 資料夾裡的範本、範例、檢查表，用相對路徑引用 |
| 專案層 / 個人層 | project / personal | `.claude/skills/` 只對該專案有效；`~/.claude/skills/` 對所有專案有效 |
| 專案說明檔 | CLAUDE.md | 每次對話都載入的專案常駐說明（第 5 章） |
| 代理技能 | Agent Skills | Claude API 端的 Skill，透過 `client.skills` 與程式執行沙盒使用 |
| 程式執行 | code execution | API 提供的雲端沙盒，模型可在裡面跑程式與使用 Agent Skills |
