# 接線圖製作指南（給畫圖的作者）

每個有 `**接線**` ASCII 圖的實驗，都要補一張 Fritzing 風格的麵包板接線圖（SVG），**ASCII 圖保留不動**，SVG 插在 ASCII 程式碼區塊的正下方。

## 流程

1. 讀章節，找到 `### 實驗 N-K` 底下的 `**接線**` 段落與其文字說明（「Arduino D9 → 1kΩ → …」那些條列）。
2. 寫規格檔 `electric/diagrams/NN-K-slug.json`（NN 兩位數章號、K 實驗號、slug 英文小寫），格式見 `tools/bbdraw.py` 開頭的說明。範例：`electric/diagrams/01-2-first-led.json`、`electric/diagrams/09-2-transistor-motor.json`。
3. 執行 `tools/preview.sh electric/diagrams/NN-K-slug.json <你的預覽目錄>`，它會產生 `electric/src/images/NN-K-slug.svg` 並輸出一張 PNG 路徑。
4. **用 Read 工具打開那張 PNG 親眼檢查**：接線是否和文字一致、零件標籤有沒有互相重疊、探棒或標籤有沒有壓到零件、板外零件有沒有被裁掉。有問題就改規格重畫，直到乾淨為止。
5. 在章節 Markdown 裡，找到該實驗 `**接線**` 下的 ASCII 程式碼區塊，在它的結尾 ``` 之後空一行插入：

   ```
   ![麵包板接線圖：實驗 N-K 標題](images/NN-K-slug.svg)
   ```

   不要加其他說明文字，不要改 ASCII 圖或其他內容。

## 正確性規則（最重要）

- 接線必須和章節文字**完全一致**：腳位編號、電阻值、零件型號、極性。
- 極性：LED `pins` 第一個是長腳（+）；電解電容第一個是 +；二極體第一個是陽極、第二個是陰極（色環）；蜂鳴器第一個是 +。
- 2N2222 的 `pins` 順序是 E、B、C；IRLZ44N 是 G、D、S；可變電阻是 左、中（滑動端）、右；DHT11 是 +、out、−；OLED 是 GND、VCC、SCL、SDA；伺服馬達是 `servo:gnd` / `servo:vcc` / `servo:sig`。
- 板子腳位名稱：`uno:D9`、`uno:A0`、`uno:5V`、`uno:3.3V`、`uno:GND`（下排）、`uno:GND0`（上排 AREF 旁的 GND）、`uno:VIN`；ESP32 用 GPIO 數字 `esp:18`、`esp:34`，還有 `esp:3V3`、`esp:GND`、`esp:VIN`、`esp:TX0`、`esp:RX0`。
- 電源軌：板子的 5V/3V3 接 `T+n`（上方紅軌）、GND 接 `T-n`（上方藍軌）；需要第二組電源（電池盒）用下方 `B+n` / `B-n`。
- 文字裡有示波器探棒就加 `probes`（`tip` 是探棒接的孔、`gnd` 是接地夾接的 GND 軌孔）；有三用電表就加 `{"type":"meter","mode":"V"或"A"或"Ω","display":"預期讀值"}` 並用 `meter:red` / `meter:black` 接線；有邏輯分析儀就加 `logic` 並用 `logic:CH0`、`logic:GND` 接線。
- 純軟體或純儀器操作的實驗（例如安裝 IDE、探棒補償）**不用畫**。只有電池 + 三用電表的實驗可以畫：電池與電表都是板外零件，`wires` 可以直接 `["bat:+", "meter:red", "red"]`，並加 `"breadboard": false` 不畫麵包板。
- 三用電表要放在 `parts` 裡（`{"type":"meter","mode":"V","display":"3.28"}`），再用 `meter:red` / `meter:black` 接線。按鈕可用 `"label": "按鈕 1"` 自訂標籤。

## 版面規則（讓圖好看）

- 三腳與四腳零件（電晶體、MOSFET、可變電阻、DHT11、OLED、按鈕）放在 **e 列（上半）或 f 列（下半）**，本體會自動朝中央溝畫，不會壓到孔。
- 兩腳零件（電阻、LED、電容、二極體、電感、LDR、蜂鳴器）可以直放（同一行不同列，例如 c5→c8）或橫放（同一列不同行）。兩腳之間至少隔 2 孔（電阻 3–4 孔最好看）。
- 零件之間至少隔 2 行，標籤才不會疊在一起。整張圖用到的行數儘量集中在 1–25 行。
- 杜邦線顏色慣例：5V/電源紅、GND 黑、訊號橘/黃/綠/藍、I2C SDA 藍 SCL 黃。
- 同一個實驗如果文字有「步驟二再加上 XX」的變化，只畫**最終完整版**；文字有兩個明顯不同的電路（例如「A 部分」「B 部分」），各畫一張，檔名加 `a`、`b`。
- `notes` 放 1–3 條最關鍵的提醒（極性、哪隻腳接哪裡），不要超過 3 條。

## 不要做的事

- 不要修改 `tools/bbdraw.py`。缺功能就用現有零件近似並在最後回報。
- 不要改 ASCII 圖、程式碼、或任何章節文字。
- 不要畫沒有在文字裡出現的接線。
