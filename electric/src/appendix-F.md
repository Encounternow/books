# 附錄 F　中英名詞對照表

全書出現過的名詞都在這裡，依主題分成六組。每一條有中文、英文和一句話說明。說明是「幫你想起來」用的，不是完整定義；完整的解釋請回對應章節看。

查的方法：先想這個詞是「講電的基本性質」「某個零件」「訊號或儀器」「數位或 Arduino」「通訊或 Wi-Fi」還是「程式裡的東西」，再到那一組找。

---

## F.1　電學基礎

| 中文 | 英文 | 簡短說明 |
|---|---|---|
| 電荷 | Charge | 電的「最小單位」，正負兩種，同性相斥、異性相吸。 |
| 電流 | Current (I) | 電荷流動的量，單位安培（A）。像水管裡每秒流過多少水。 |
| 電壓 | Voltage (V) | 推動電流的「壓力」，單位伏特（V）。像水塔的高度。 |
| 電阻 | Resistance (R) | 阻擋電流的程度，單位歐姆（Ω）。像水管變細。 |
| 安培 | Ampere (A) | 電流的單位。本書常用毫安培（mA）。 |
| 伏特 | Volt (V) | 電壓的單位。 |
| 歐姆 | Ohm (Ω) | 電阻的單位。 |
| 瓦特 | Watt (W) | 功率的單位。1/4 W 電阻最多只能散 0.25 W 的熱。 |
| 歐姆定律 | Ohm's Law | V = I × R。電壓、電流、電阻三者的關係。 |
| 功率 | Power (P) | 每秒消耗的能量，P = V × I。 |
| 導體 | Conductor | 電流容易通過的材料：銅、鋁、鐵。 |
| 絕緣體 | Insulator | 電流幾乎不通過的材料：塑膠、橡膠、空氣。 |
| 閉合迴路 | Closed Circuit | 電流從電源正極出發、繞一圈回到負極的完整路徑。斷一處就不通。 |
| 開路 | Open Circuit | 迴路斷掉，沒有電流。 |
| 短路 | Short Circuit | 電源正負極被幾乎沒電阻的東西直接接通，電流超大、會發熱甚至起火。 |
| 接地／地 | Ground (GND) | 電路裡約定的「0 V 基準點」。所有電壓都是相對它量的。 |
| 直流 | Direct Current (DC) | 電流方向固定不變。電池、USB 都是直流。 |
| 交流 | Alternating Current (AC) | 電流方向來回交替。家用插座是交流，本書不碰。 |
| 串聯 | Series | 元件一個接一個排成一條線，電流處處相同。 |
| 並聯 | Parallel | 元件並排接在同兩點之間，電壓處處相同。 |
| 分壓器 | Voltage Divider | 兩顆串聯電阻，從中間取出比較低的電壓。 |
| 分流 | Current Division | 並聯時電流依電阻大小分配，電阻小的分到多。 |
| 克希荷夫電流定律 | Kirchhoff's Current Law (KCL) | 流進一個接點的電流 = 流出的電流。 |
| 克希荷夫電壓定律 | Kirchhoff's Voltage Law (KVL) | 繞迴路一圈，所有電壓升和電壓降加起來是 0。 |
| 內阻 | Internal Resistance | 電池內部自己的電阻，電流越大、輸出電壓掉越多。 |
| 空載電壓 | Open-Circuit Voltage | 電池沒接負載時量到的電壓。 |
| 負載 | Load | 吃電的東西：LED、馬達、Arduino。 |
| 電池容量 | Battery Capacity (mAh) | 毫安培小時。1000 mAh 可以供 100 mA 十小時（理想值）。 |
| 穩壓器 | Voltage Regulator | 把輸入電壓變成固定輸出電壓的晶片，Arduino 板上就有一顆 5 V 的。 |
| 磁場 | Magnetic Field | 磁鐵或通電導線周圍的「力的範圍」。 |
| 電磁感應 | Electromagnetic Induction | 磁場變化讓線圈產生電壓。發電機的原理。 |
| 反電動勢 | Back EMF | 線圈的電流突然被切斷時，它自己產生的反向高電壓尖波。 |
| 時間常數 | Time Constant (τ) | RC 電路充放電的「快慢指標」，τ = R × C，5τ 當作充飽。 |

---

## F.2　元件

| 中文 | 英文 | 簡短說明 |
|---|---|---|
| 電阻（元件） | Resistor | 固定阻值的零件，用色環標示阻值。 |
| 色碼 | Color Code | 電阻身上的色環，用顏色表示數字。 |
| 可變電阻／電位器 | Potentiometer | 轉旋鈕可以改阻值的三腳元件，常當分壓器用。 |
| 光敏電阻 | Light-Dependent Resistor (LDR) | 越亮阻值越低的電阻，做夜燈用。 |
| 電容（元件） | Capacitor | 儲存電荷的零件，像小水桶，單位法拉（F）。 |
| 法拉 | Farad (F) | 電容的單位。本書用微法（µF）和奈法（nF）。 |
| 電解電容 | Electrolytic Capacitor | 容量大的圓柱形電容，**有極性**，接反會爆。 |
| 陶瓷電容 | Ceramic Capacitor | 小容量、沒極性的扁平電容，常用 100 nF（104）。 |
| 極性 | Polarity | 元件有分正負腳。LED、電解電容、二極體都有。 |
| 去耦電容 | Decoupling Capacitor | 並在晶片電源腳旁邊的電容，吸收電壓的小抖動。 |
| 電感（元件） | Inductor | 線圈，抗拒電流變化，單位亨利（H）。 |
| 亨利 | Henry (H) | 電感的單位。本書用微亨（µH）和毫亨（mH）。 |
| 線圈 | Coil | 把導線繞成圈，通電生磁、磁變生電。 |
| 電磁鐵 | Electromagnet | 線圈裡放鐵釘，通電就變磁鐵。 |
| 二極體 | Diode | 只讓電流往一個方向走的零件。 |
| 陽極 | Anode | 二極體／LED 的正極腳，電流從這裡進。 |
| 陰極 | Cathode | 二極體／LED 的負極腳，電流從這裡出。色環那一端。 |
| 順向偏壓 | Forward Bias | 二極體接「對」方向，會導通。 |
| 逆向偏壓 | Reverse Bias | 二極體接「反」方向，不導通。 |
| 順向電壓 | Forward Voltage (Vf) | 二極體導通時固定吃掉的電壓，1N4007 約 0.7 V、LED 1.8–3.4 V。 |
| 整流 | Rectification | 用二極體把交流變成只有一個方向的直流。 |
| 飛輪二極體 | Flyback Diode | 並在線圈兩端、吸收反電動勢尖波的二極體。 |
| 發光二極體 | Light-Emitting Diode (LED) | 會發光的二極體，一定要串限流電阻。 |
| 限流電阻 | Current-Limiting Resistor | 串在 LED 前面、防止電流過大的電阻。 |
| 七段顯示器 | Seven-Segment Display | 七個 LED 排成「8」字，顯示數字。 |
| 電晶體 | Transistor | 用小電流控制大電流的三腳元件，當開關用。 |
| NPN 電晶體 | NPN Transistor | 本書用的 2N2222，基極給正電流就導通。 |
| 基極 | Base (B) | 電晶體的控制腳。 |
| 集極 | Collector (C) | 電晶體接負載的腳。 |
| 射極 | Emitter (E) | 電晶體接 GND 的腳。 |
| 放大倍數 | Current Gain (β / hFE) | 集極電流可以是基極電流的幾倍，2N2222 約 100。 |
| 飽和 | Saturation | 電晶體完全導通的狀態，像水閥全開。 |
| 截止 | Cut-off | 電晶體完全不導通的狀態，像水閥全關。 |
| 金氧半場效電晶體 | MOSFET | 用電壓控制的開關，本書用 IRLZ44N，幾乎不吃控制電流。 |
| 閘極 | Gate (G) | MOSFET 的控制腳。 |
| 汲極 | Drain (D) | MOSFET 接負載的腳。 |
| 源極 | Source (S) | MOSFET 接 GND 的腳。 |
| 邏輯準位 MOSFET | Logic-Level MOSFET | 5 V 或 3.3 V 就能推到全開的 MOSFET，型號裡有 L。 |
| 達靈頓 | Darlington | 兩顆電晶體串起來，放大倍數相乘。 |
| 繼電器 | Relay | 用線圈吸動金屬片的機械開關，可以用小電壓切換另一個電路。 |
| 直流馬達 | DC Motor | 通電就轉的馬達，調電壓或 PWM 調速。 |
| 伺服馬達 | Servo Motor | 可以指定角度的馬達，靠 1–2 ms 的脈波控制。 |
| 蜂鳴器 | Buzzer | 發聲元件。無源（Passive）要給頻率才會響，有源（Active）通電就響。 |
| 按鈕開關 | Push Button / Tactile Switch | 按下才導通的開關。 |
| 溫濕度感測器 | Temperature & Humidity Sensor (DHT11) | 一條線回傳溫度與濕度的感測器。 |
| 感測器 | Sensor | 把光、溫度、聲音等變成電壓或數位訊號的元件。 |
| 麵包板 | Breadboard | 不用焊接就能插元件的板子，每五孔一排相通。 |
| 杜邦線 | Jumper Wire (Dupont Wire) | 兩端有針（公）或孔（母）的連接線。 |
| 電池扣 | Battery Snap | 接 9 V 電池用的卡扣，附兩條線。 |
| 有機發光二極體顯示器 | OLED Display | 自己會發光的小螢幕，本書用 0.96 吋 SSD1306。 |

---

## F.3　訊號與儀器

| 中文 | 英文 | 簡短說明 |
|---|---|---|
| 訊號 | Signal | 隨時間變化、帶有資訊的電壓。 |
| 波形 | Waveform | 訊號畫在「電壓 vs 時間」圖上的形狀。 |
| 正弦波 | Sine Wave | 最平滑的波，像海浪。 |
| 方波 | Square Wave | 只有高低兩種電壓、方方正正的波。 |
| 脈波 | Pulse | 短暫跳高又回來的一個訊號。 |
| 頻率 | Frequency (f) | 每秒幾個週期，單位赫茲（Hz）。f = 1 ÷ T。 |
| 週期 | Period (T) | 一個完整的波要多久，單位秒。 |
| 赫茲 | Hertz (Hz) | 頻率的單位，每秒一次。 |
| 振幅 | Amplitude | 波從中心到最高點的高度。 |
| 峰對峰電壓 | Peak-to-Peak Voltage (Vpp) | 波最高點到最低點的差。 |
| 平均電壓 | Average Voltage | 一段時間內電壓的平均值，PWM 濾波後就是這個。 |
| 占空比 | Duty Cycle | 一個週期內 HIGH 占的百分比。 |
| 脈寬調變 | Pulse-Width Modulation (PWM) | 用改變占空比的方波來「假裝」不同電壓。 |
| 上升緣 | Rising Edge | 訊號從低變高的瞬間。 |
| 下降緣 | Falling Edge | 訊號從高變低的瞬間。 |
| 濾波 | Filtering | 把訊號裡不要的頻率去掉。 |
| 低通濾波器 | Low-Pass Filter | 讓慢的變化通過、擋掉快的變化。RC 一顆電阻一顆電容就能做。 |
| 雜訊 | Noise | 訊號上不想要的亂七八糟小抖動。 |
| 尖波 | Spike | 很短、很高的一個突波，例如反電動勢。 |
| 彈跳 | Bounce | 按鈕按下時金屬片反覆跳動，造成好幾次高低變化。 |
| 去抖動 | Debounce | 用延遲、電容或程式把彈跳濾掉。 |
| 示波器 | Oscilloscope | 把電壓隨時間的變化畫出來的儀器。 |
| 探棒 | Probe | 示波器的測試線，有勾子和鱷魚夾。 |
| 衰減比 | Attenuation (1×/10×) | 探棒把訊號縮小的倍數，10× 比較不干擾電路。 |
| 探棒補償 | Probe Compensation | 調探棒上的小螺絲，讓方波的角變直角。 |
| 接地夾 | Ground Clip | 探棒上的黑色鱷魚夾，一定接電路 GND。 |
| 通道 | Channel (CH) | 示波器或邏輯分析儀的一個輸入。 |
| 每格電壓 | Volts per Division (V/div) | 示波器畫面垂直一格代表幾 V。 |
| 每格時間 | Seconds per Division (s/div) | 示波器畫面水平一格代表多少時間。 |
| 耦合 | Coupling (DC/AC) | DC 看完整電壓；AC 把直流去掉只看變化。 |
| 觸發 | Trigger | 告訴示波器「從訊號的哪一點開始畫」，波形才會停住。 |
| 觸發準位 | Trigger Level | 觸發用的電壓門檻。 |
| 自動模式 | Auto Mode | 沒觸發到也一直畫。 |
| 一般模式 | Normal Mode | 沒觸發到就等。 |
| 單次觸發 | Single | 觸發一次就停住畫面，看一次性事件。 |
| 自動設定 | Auto Set / Autoscale | 示波器自己猜一組設定。 |
| 游標 | Cursor | 畫面上可以移動的量測線，量時間差或電壓差。 |
| 自動量測 | Measure | 示波器自動算 Vpp、頻率、占空比等數值。 |
| 捲動模式 | Roll Mode | 畫面像紙帶一樣慢慢捲，看很慢的訊號。 |
| 三用電表 | Multimeter | 量電壓、電流、電阻的手持儀器。 |
| 通斷檔 | Continuity | 三用電表的蜂鳴功能，兩點相通會叫。 |
| 邏輯分析儀 | Logic Analyzer | 同時記錄多條線 0/1 變化的儀器，可以解碼通訊。 |
| 取樣率 | Sample Rate | 每秒記錄幾次，至少要是訊號頻率的 4 倍。 |
| 取樣數 | Sample Count | 總共記錄幾個點，決定錄多久。 |
| 協定解碼器 | Protocol Decoder | PulseView 裡把 0/1 翻譯成字元或位址的功能。 |
| 序列繪圖器 | Serial Plotter | Arduino IDE 裡把序列埠的數字畫成曲線的工具。 |

---

## F.4　數位與微控制器

| 中文 | 英文 | 簡短說明 |
|---|---|---|
| 數位 | Digital | 只有 0 和 1 兩種狀態。 |
| 類比 | Analog | 連續變化的量，任何電壓都可以。 |
| 高電位／低電位 | HIGH / LOW | 數位的 1 和 0。UNO 是 5 V／0 V，ESP32 是 3.3 V／0 V。 |
| 電壓門檻 | Threshold | 高於多少算 1、低於多少算 0 的分界線。 |
| 位元 | Bit | 一個 0 或 1。 |
| 位元組 | Byte | 8 個位元，可以表示 0–255。 |
| 二進位 | Binary | 只用 0 和 1 的計數方式。 |
| 十六進位 | Hexadecimal | 用 0–9 和 A–F 計數，0x3C 這種寫法。 |
| 邏輯閘 | Logic Gate | 做 AND、OR、NOT 等判斷的基本電路。 |
| 真值表 | Truth Table | 把所有輸入組合和對應輸出列成的表。 |
| 及閘 | AND Gate | 全部輸入都是 1 才輸出 1。 |
| 或閘 | OR Gate | 任何一個輸入是 1 就輸出 1。 |
| 反閘 | NOT Gate | 把 1 變 0、0 變 1。 |
| 互斥或閘 | XOR Gate | 兩個輸入不一樣才輸出 1。 |
| 上拉電阻 | Pull-up Resistor | 把腳位平常拉到 HIGH 的電阻，按鈕按下才變 LOW。 |
| 下拉電阻 | Pull-down Resistor | 把腳位平常拉到 LOW 的電阻。 |
| 浮接 | Floating | 腳位沒接任何東西，讀值會亂跳。 |
| 微控制器 | Microcontroller (MCU) | 一顆有 CPU、記憶體、腳位的小電腦晶片。 |
| Arduino UNO | Arduino UNO | 本書用的 5 V 開發板，晶片是 ATmega328P。 |
| ESP32 | ESP32 | 本書用的 3.3 V 開發板，內建 Wi-Fi 和藍牙。 |
| 開發板 | Development Board | 把微控制器、USB、穩壓器做在一起方便使用的板子。 |
| 腳位 | Pin | 微控制器伸出來可以接線的接點。 |
| 通用輸入輸出 | GPIO | 可以設定成輸入或輸出的腳位。 |
| 數位輸出 | Digital Output | 腳位輸出 HIGH 或 LOW。 |
| 數位輸入 | Digital Input | 腳位讀取 HIGH 或 LOW。 |
| 類比輸入 | Analog Input | 腳位讀取電壓並換成數字。 |
| 類比數位轉換器 | Analog-to-Digital Converter (ADC) | 把電壓變成數字的電路，UNO 10 位元、ESP32 12 位元。 |
| 解析度 | Resolution | ADC 能分成幾格：10 位元 = 1024 格。 |
| 參考電壓 | Reference Voltage | ADC 把哪個電壓當成最大值：UNO 5 V、ESP32 3.3 V。 |
| 中斷 | Interrupt | 腳位一變化就立刻跳去執行某段程式。 |
| 重置 | Reset | 讓微控制器重新開機。 |
| 燒錄／上傳 | Upload / Flash | 把程式寫進微控制器。 |
| 燒錄模式 | Bootloader Mode | ESP32 等待接收程式的狀態，按 BOOT 鍵進入。 |
| 開機按鈕 | BOOT Button | ESP32 上進燒錄模式用的按鈕（接 GPIO 0）。 |
| 啟用腳 | EN (Enable) | ESP32 的重置腳，按下就重開。 |
| 欠壓偵測 | Brownout Detector | ESP32 偵測到電壓不夠就自動重開機的保護機制。 |
| 深度睡眠 | Deep Sleep | ESP32 幾乎全部關掉省電，時間到再醒來。 |
| 板上 LED | Onboard LED | 焊在開發板上的 LED：UNO 是 D13，ESP32 是 GPIO 2。 |
| 驅動程式 | Driver | 讓電腦認得 USB 裝置的軟體，CH340、CP2102 常要另外裝。 |
| 函式庫 | Library | 別人寫好的程式包，例如 Servo、DHT、Adafruit_SSD1306。 |
| 整合開發環境 | IDE | 寫程式、編譯、上傳一站搞定的軟體，Arduino IDE。 |

---

## F.5　通訊與無線

| 中文 | 英文 | 簡短說明 |
|---|---|---|
| 通訊協定 | Communication Protocol | 兩顆晶片講話的「規則」，誰先講、多快講、怎麼算一個字。 |
| 序列通訊 | Serial Communication | 一次送一個位元，排隊送。 |
| 並列通訊 | Parallel Communication | 多條線同時送很多位元。 |
| 通用非同步收發器 | UART | 兩條線（TX、RX）的序列通訊，Serial.println 用的就是它。 |
| 傳送／接收 | TX / RX | 送出資料的腳／接收資料的腳。A 的 TX 接 B 的 RX。 |
| 鮑率 | Baud Rate | 每秒幾個位元，兩邊要一樣，本書用 9600 或 115200。 |
| 起始位元 | Start Bit | UART 每個字元前面的一個 LOW，告訴對方「要開始了」。 |
| 停止位元 | Stop Bit | UART 每個字元後面的一個 HIGH，告訴對方「講完了」。 |
| 8N1 | 8N1 | 8 個資料位元、無同位元、1 個停止位元，UART 最常見設定。 |
| 序列埠 | Serial Port (COM Port) | 電腦和 Arduino 講話的那條通道。 |
| 序列埠監控視窗 | Serial Monitor | Arduino IDE 裡顯示 Serial.println 內容的視窗。 |
| 積體電路匯流排 | I2C (Inter-Integrated Circuit) | 兩條線（SDA、SCL）可以接很多裝置的通訊，靠位址認人。 |
| 資料線 | SDA (Serial Data) | I2C 的資料線。UNO 是 A4，ESP32 是 GPIO 21。 |
| 時脈線 | SCL (Serial Clock) | I2C 的時脈線。UNO 是 A5，ESP32 是 GPIO 22。 |
| 位址 | Address | I2C 裝置的「門牌號碼」，OLED 是 0x3C。 |
| 主機／從機 | Master / Slave (Controller / Peripheral) | I2C 裡發號施令的那顆／聽命的那顆。 |
| 應答 | ACK (Acknowledge) | I2C 從機收到資料後回的一個「收到」位元。 |
| 序列周邊介面 | SPI | 四條線的高速通訊，本書只簡介。 |
| 時脈 | Clock | 用來同步「現在讀第幾個位元」的規律方波。 |
| 無線網路 | Wi-Fi | ESP32 內建的無線網路，只支援 2.4 GHz。 |
| 網路名稱 | SSID | Wi-Fi 的名字。 |
| 網際網路協定位址 | IP Address | 裝置在網路上的號碼，例如 192.168.1.50。 |
| 網頁伺服器 | Web Server | 等別人用瀏覽器來敲門、然後回傳網頁的程式。 |
| 超文字傳輸協定 | HTTP | 瀏覽器和伺服器講話的規則。 |
| 超文字標記語言 | HTML | 寫網頁內容的語言。 |
| 用戶端 | Client | 主動發出請求的一方，例如手機瀏覽器。 |
| 存取點 | Access Point (AP) | 讓別人連上的 Wi-Fi 熱點，ESP32 自己也能當。 |
| 訊息佇列遙測傳輸 | MQTT | 物聯網常用的「發布／訂閱」通訊方式，本書只簡介。 |
| 藍牙 | Bluetooth | ESP32 內建的短距離無線通訊，本書只提到。 |
| 物聯網 | Internet of Things (IoT) | 讓感測器、燈、風扇都連上網路的概念。 |

---

## F.6　程式

| 中文 | 英文 | 簡短說明 |
|---|---|---|
| 程式碼 | Code / Sketch | Arduino 把一個程式叫做 sketch。 |
| 初始設定 | setup() | 開機只執行一次的區塊。 |
| 主迴圈 | loop() | setup() 結束後一直重複執行的區塊。 |
| 函式 | Function | 一段取了名字、可以重複呼叫的程式。 |
| 變數 | Variable | 存數值的「盒子」，要先宣告型別。 |
| 常數 | Constant (const) | 宣告後不能改的變數，腳位編號常用。 |
| 整數 | int | 整數型別，UNO 上範圍 −32768 到 32767。 |
| 浮點數 | float | 有小數的數字，例如 3.14。 |
| 布林 | bool | 只有 true／false 兩種值。 |
| 字串 | String | 一串文字。 |
| 註解 | Comment | 用 // 或 /* */ 寫給人看的說明，程式不執行。 |
| 條件判斷 | if / else | 「如果……就……否則……」。 |
| 迴圈 | for / while | 重複執行某段程式。 |
| 比較運算子 | Comparison Operator | ==、!=、<、>、<=、>=。注意 == 和 = 不一樣。 |
| 邏輯運算子 | Logical Operator | &&（且）、\|\|（或）、!（非）。 |
| 設定腳位模式 | pinMode() | 把腳位設成 INPUT、OUTPUT 或 INPUT_PULLUP。 |
| 數位寫入 | digitalWrite() | 讓腳位輸出 HIGH 或 LOW。 |
| 數位讀取 | digitalRead() | 讀腳位是 HIGH 還是 LOW。 |
| 類比讀取 | analogRead() | 讀 ADC 數值，UNO 0–1023、ESP32 0–4095。 |
| 類比寫入 | analogWrite() | UNO 輸出 PWM，0–255。 |
| 延遲 | delay() | 暫停幾毫秒。 |
| 毫秒計時 | millis() | 回傳開機到現在過了幾毫秒，不卡住程式的計時方法。 |
| 對應 | map() | 把一個範圍的數字換算成另一個範圍。 |
| 音調 | tone() | UNO 讓腳位輸出指定頻率的方波。 |
| LED 控制 | ledcWrite() / ledcAttach() | ESP32 輸出 PWM 的函式。 |
| 序列埠初始化 | Serial.begin() | 設定鮑率、打開序列埠。 |
| 序列埠輸出 | Serial.println() | 把文字或數字送到電腦。 |
| 引入 | #include | 把函式庫加進程式。 |
| 定義 | #define | 幫一個數字或文字取名字。 |
| 伺服函式庫 | Servo.h | 控制伺服馬達的函式庫，attach()、write()。 |
| 編譯 | Compile | 把人看的程式翻譯成晶片看的機器碼。 |
| 編譯錯誤 | Compile Error | 程式語法有問題，IDE 會指出哪一行。 |
| 無效數值 | nan (Not a Number) | 浮點數「算不出來」的標記，DHT11 讀失敗會回傳它。 |
| 除錯 | Debug | 找出並修正程式或電路的錯誤。 |
