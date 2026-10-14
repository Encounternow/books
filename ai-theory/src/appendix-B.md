# 附錄 B　Colab 操作與程式索引

全書的程式都在 Google Colab 上跑。這份附錄分三部分：Colab 的基本操作、每一章的程式在做什麼與需要哪些套件、以及你最可能遇到的錯誤訊息和解法。

## B.1　Colab 基本操作

**它是什麼**：Google 提供的免費線上 Python 環境，在瀏覽器裡寫程式、按一下就跑，不用在自己的電腦安裝任何東西。需要一個 Google 帳號。

### 開始

1. 打開 https://colab.research.google.com ，用 Google 帳號登入。
2. 點「新增筆記本」。畫面會出現一個空的「儲存格（Cell）」。
3. 筆記本會自動存到你的 Google 雲端硬碟的「Colab Notebooks」資料夾。改名：點左上角的檔名。

### 儲存格

- 一個筆記本由很多儲存格組成，每格可以是**程式**或**文字**（Markdown）。
- **執行一格**：點進去，按 `Shift + Enter`（或左邊的 ▶ 按鈕）。輸出會出現在那一格下面。
- **新增一格**：滑鼠移到儲存格上下邊緣，點「+ 程式碼」或「+ 文字」。
- **順序很重要**：變數是上一格定義的，就要先跑上一格。書裡每章的程式都設計成「全部貼進一格、跑一次」，最不容易出錯。
- **全部重跑**：選單「執行階段 → 全部執行」。

### 執行階段（Runtime）

- 第一次執行會花幾秒「連線」。畫面右上角會顯示 RAM 和磁碟。
- **閒置約 90 分鐘或總共約 12 小時**會自動斷線，變數全部消失，重新「全部執行」即可。程式碼不會不見。
- **重新啟動**：「執行階段 → 重新啟動工作階段」。變數清空、套件還在。當你覺得「怪怪的」（例如改了程式但結果沒變）先做這個。
- **GPU**：「執行階段 → 變更執行階段類型 → 硬體加速器 → GPU」。本書只有第 11 章選配的小型語言模型和第 8 章的 PyTorch 版本需要；其餘用 CPU 就夠。免費版 GPU 有用量限制。

### 套件

- Colab 預裝 numpy、matplotlib、scikit-learn（sklearn）、pandas、PyTorch、torchvision 等，本書的程式幾乎都不用額外安裝。
- 要裝別的套件，在儲存格裡打 `!pip install 套件名`（前面有驚嘆號），執行完再 `import`。重新啟動工作階段後要重裝。

### 檔案

- 左側邊欄的「檔案」圖示可以看到暫存空間。**斷線後會清空**。
- 上傳：點「檔案 → 上傳」，或在程式裡 `from google.colab import files; files.upload()`。
- 掛載雲端硬碟（要長期保存檔案時）：`from google.colab import drive; drive.mount('/content/drive')`，依指示授權。

### 幾個好用的習慣

- 每格程式最上面用註解寫它在做什麼。
- 改數字做實驗前，先複製一份筆記本（「檔案 → 在雲端硬碟中儲存複本」），原版留著。
- 跑太久想停：點儲存格左邊的 ■。
- 看一個變數的內容：單獨一格打變數名，執行。
- 看一個函式怎麼用：`help(np.argsort)`。

## B.2　全書程式索引

每章「用工具看看」的程式。「套件」欄只列 `import` 進來的；全部 Colab 預裝。

| 章 | 程式做什麼 | 套件 | 執行時間 | 可以改什麼來做實驗 |
|---|---|---|---|---|
| 1 | 用「平均」當最簡單的預測器，算誤差 | numpy | 1 秒 | 換資料、看誤差怎麼變 |
| 2 | sklearn 的 KNN 與決策樹各約 10 行，分類小資料集 | numpy、sklearn | 2 秒 | k 的大小、樹的深度 |
| 3 | numpy 算最佳直線（最小平方），印斜率與截距 | numpy | 1 秒 | 加一個離群值看直線怎麼歪 |
| 4 | 向量加法、內積、矩陣乘法；把一張小圖當矩陣顯示 | numpy、matplotlib | 2 秒 | 把矩陣換成旋轉、鏡射 |
| 5 | 用梯度下降找到第 3 章的直線，印每一步的損失 | numpy | 2 秒 | 學習率（太大會發散） |
| 6 | numpy 感知器學 AND、OR，試 XOR 失敗 | numpy | 1 秒 | 初始權重、學習率、改成 XOR |
| 7 | 從零寫兩層網路學 XOR，畫損失下降曲線 | numpy、matplotlib | 5 秒 | 隱藏層大小、epoch 數 |
| 8 | 訓練 MNIST 手寫數字到 95% 以上，顯示認錯的圖 | numpy 或 PyTorch、torchvision、matplotlib | CPU 約 2–5 分鐘 | epoch、batch、隱藏層；加 GPU 看速度 |
| 9 | numpy 對照片做 3×3 卷積（邊緣偵測） | numpy、matplotlib | 3 秒 | 換濾鏡（模糊、銳利） |
| 10 | 用小型詞向量或共現矩陣算詞的相似度 | numpy | 5 秒 | 換詞、換文字 |
| 11 | 字元級 n-gram 文字產生器；（選配）呼叫小型開源語言模型 | random、collections；選配 transformers、torch | 1 秒；選配需 GPU 約 3 分鐘 | n、溫度、種子 |
| 12 | 迷你獎勵模型：從 12 組偏好學出 3 個權重 | numpy | 1 秒 | 調換偏好、改學習率 |
| 13 | 一層分類器認 8×8 數字；分類別評估；製造對抗樣本 | numpy、sklearn | 5 秒 | 雜訊大小 eps、訓練次數 |
| 14-1 | KNN 推薦：找最像的同學、推薦他們喜歡的東西 | numpy | 1 秒 | k、特徵、自己的資料 |
| 14-2 | 兩層網路從零訓練 8×8 數字；印圖、用 # 畫圖給它猜 | numpy、sklearn | 15 秒 | 隱藏層、epoch、drawing |
| 14-3 | 字元 n-gram 寫故事，比較 n = 1、2、3 | random、collections | 1 秒 | n、種子、換文字 |

### 第 11 章選配：呼叫小型開源語言模型

需要 GPU。先裝套件（Colab 通常已預裝 transformers，沒有就裝）：

```python
!pip install -q transformers torch
```

再用 Hugging Face 的 `pipeline` 載入一個支援中文的小型開源模型產生文字。模型名稱會隨時間更新，請到 https://huggingface.co/models 搜尋「chinese text-generation」挑一個幾億參數以內的；第一次執行會下載模型檔（幾百 MB 到幾 GB），需要幾分鐘。基本用法是：

```python
from transformers import pipeline
gen = pipeline("text-generation", model="（模型名稱）")
print(gen("從前從前，山腳下有一隻小狐狸，", max_new_tokens=60, do_sample=True, temperature=0.8)[0]["generated_text"])
```

參數 `temperature` 就是第 11 章的溫度，`do_sample=True` 表示用取樣而不是永遠挑最大機率的字。

## B.3　常見錯誤訊息

錯誤訊息都在輸出的**最後一行**，先看那一行。

| 錯誤訊息 | 意思 | 怎麼修 |
|---|---|---|
| `NameError: name 'np' is not defined` | 用了一個還沒定義的名字 | 最常見是上面那格 `import numpy as np` 沒跑；按「全部執行」。 |
| `ModuleNotFoundError: No module named 'xxx'` | 套件沒裝 | `!pip install xxx`，裝完再跑。確認拼法（sklearn 的安裝名是 `scikit-learn`）。 |
| `SyntaxError: invalid syntax` | 程式寫法有誤 | 看箭頭指的那一行：括號沒關、少冒號、中文的逗號或引號（，「」）混進程式裡。 |
| `IndentationError: unexpected indent` | 縮排不對 | Python 用縮排分段落。`for`、`if`、`def` 下面要縮 4 格，而且整段要一致；貼程式時前面多了空格也會這樣。 |
| `ValueError: shapes (3,2) and (3,2) not aligned` | 矩陣乘法的形狀對不上 | 左邊的欄數要等於右邊的列數。印 `A.shape`、`B.shape` 檢查，可能要轉置 `A.T`。 |
| `ValueError: operands could not be broadcast together` | 兩個陣列形狀不同不能相加減 | 印出 `.shape`。常見是一個是 (64,) 一個是 (8, 8)，用 `.reshape(64)` 統一。 |
| `IndexError: index 360 is out of bounds for axis 0 with size 360` | 編號超過範圍 | 索引從 0 開始，360 張圖的最大編號是 359。 |
| `KeyError: '小美'` | 字典裡沒有這個鍵 | 名字打錯或沒加進字典；注意全形半形、空格。 |
| `TypeError: unsupported operand type(s) for +: 'int' and 'str'` | 數字和文字不能直接加 | 用 `int()` 或 `str()` 轉換，或用 f-string：`f"共 {n} 張"`。 |
| `TypeError: 'int' object is not subscriptable` | 對一個數字用了 `[ ]` | 你以為是清單的東西其實是數字；往上找這個變數是在哪裡被覆蓋的。 |
| `ZeroDivisionError: division by zero` | 除以 0 | 分母可能是空清單的長度或全 0 的陣列；分母加一個很小的數（如 `+ 1e-9`）。 |
| `FileNotFoundError: [Errno 2] No such file or directory` | 找不到檔案 | 斷線後暫存檔會清空，重新上傳；路徑要完全一樣。 |
| `RuntimeError: CUDA out of memory` | GPU 記憶體不夠 | 把 batch 改小、模型改小，或「重新啟動工作階段」釋放記憶體。 |
| 輸出是 `nan` 或 `inf` | 數字爆掉 | 學習率太大（第 5 章）；或 `log(0)`，在機率上加 `1e-9`。 |
| 損失一直不降 | 不一定是錯誤 | 學習率太小、權重初始化全 0（第 6 章）、或資料沒有縮到 0 到 1。 |
| 執行很久沒反應 | 迴圈太大或卡住 | 按儲存格左邊 ■ 停止；先把 epoch 改小試跑。 |
| 「無法連線到 GPU 後端」 | 免費 GPU 用量到了 | 換回 CPU（「變更執行階段類型 → None」），本書大多數程式 CPU 都能跑。 |
| 改了程式，結果沒變 | 跑的是舊變數 | 「重新啟動工作階段」後全部執行。 |

### 找錯誤的三步驟

1. **看最後一行**：錯誤類型與訊息。
2. **看箭頭那一行**：訊息上方會有 `----> 12   x = a @ b` 之類的標示，那是出錯的行。
3. **印出來看**：在出錯那行前面加 `print(a.shape, b.shape)` 或 `print(type(x))`，大部分問題一印就明白。

還是不行，把整段錯誤訊息（不只最後一行）貼給聊天 AI 問，通常能得到有用的方向——但記得第 13 章：它的解釋也可能是幻覺，改完要自己跑過確認。
