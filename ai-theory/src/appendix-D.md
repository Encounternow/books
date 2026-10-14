# 附錄 D　名詞對照表

全書出現過的名詞，按主題分組，每一條都是「中文｜英文｜一句話解釋」。想找某個詞，用瀏覽器的搜尋功能（Ctrl + F／⌘ + F）最快。

## D.1　機器學習基本概念（第 1 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 1 | 人工智慧 | Artificial Intelligence, AI | 讓電腦做出需要「智慧」的事（認圖、翻譯、下棋）的技術總稱。 |
| 2 | 機器學習 | Machine Learning | 不寫死規則，從例子裡學出規律的方法。 |
| 3 | 深度學習 | Deep Learning | 用多層神經網路做的機器學習。 |
| 4 | 規則式系統 | Rule-based System | 由人把判斷規則一條一條寫出來的程式。 |
| 5 | 監督式學習 | Supervised Learning | 例子附標準答案（標籤）的學習。 |
| 6 | 非監督式學習 | Unsupervised Learning | 例子沒有標籤，模型自己找結構（例如分群）。 |
| 7 | 強化學習 | Reinforcement Learning | 靠做了之後得到的獎勵或懲罰來學習。 |
| 8 | 訓練資料 | Training Data | 用來讓模型學習的例子。 |
| 9 | 特徵 | Feature | 描述一個例子的數字，例如身高、像素值。 |
| 10 | 標籤 | Label | 例子的正確答案，例如「這是貓」。 |
| 11 | 模型 | Model | 從輸入算出預測的那個函數，由參數決定。 |
| 12 | 參數 | Parameter | 模型裡可以被訓練調整的數字（權重、偏差）。 |
| 13 | 預測 | Prediction | 模型對一個輸入給出的答案。 |
| 14 | 訓練 | Training | 調整參數讓損失變小的過程。 |
| 15 | 推論 | Inference | 訓練完後，拿模型對新資料做預測。 |
| 16 | 分類 | Classification | 預測屬於哪一類（貓／狗、0 到 9）。 |
| 17 | 迴歸 | Regression | 預測一個數值（房價、溫度）。 |
| 18 | 分群 | Clustering | 把相似的例子自動分成幾堆，不用標籤。 |
| 19 | 獎勵 | Reward | 強化學習裡，做對了得到的分數。 |
| 20 | 超參數 | Hyperparameter | 訓練前由人決定的設定，例如 k、學習率、層數。 |

## D.2　最近鄰、決策樹與泛化（第 2 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 21 | k 最近鄰 | k-Nearest Neighbors, KNN | 找最像的 k 個例子，看它們多數是哪一類。 |
| 22 | 距離 | Distance | 兩個例子有多不像，用數字表示。 |
| 23 | 歐幾里得距離 | Euclidean Distance | 各特徵差的平方和再開根號。 |
| 24 | 曼哈頓距離 | Manhattan Distance | 各特徵差的絕對值相加。 |
| 25 | 決策樹 | Decision Tree | 一連串「是／否」問題組成的分類器。 |
| 26 | 節點 | Node | 決策樹上的一個問題。 |
| 27 | 葉節點 | Leaf | 決策樹最末端，給出答案的地方。 |
| 28 | 樹深度 | Depth | 從根到葉最多問幾個問題。 |
| 29 | 過度擬合／過擬合 | Overfitting | 模型背住訓練資料的細節，遇到新資料反而不準。 |
| 30 | 欠擬合 | Underfitting | 模型太簡單，連訓練資料都學不好。 |
| 31 | 泛化 | Generalization | 對沒見過的資料也能正確預測的能力。 |
| 32 | 標準化 | Standardization | 把每個特徵換成（值 − 平均）÷ 標準差，讓尺度一致。 |
| 33 | 正規化（縮放） | Normalization | 把特徵縮到固定範圍，例如 0 到 1。 |

## D.3　線性迴歸與損失（第 3 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 34 | 線性迴歸 | Linear Regression | 用一條直線（或平面）做預測。 |
| 35 | 斜率 | Slope | 直線 x 增加 1，y 增加多少。 |
| 36 | 截距 | Intercept | 直線在 x = 0 時的 y 值。 |
| 37 | 損失函數 | Loss Function | 衡量預測錯多少的函數。 |
| 38 | 誤差／殘差 | Error / Residual | 預測值減真實值。 |
| 39 | 均方誤差 | Mean Squared Error, MSE | 誤差平方的平均。 |
| 40 | 平均絕對誤差 | Mean Absolute Error, MAE | 誤差絕對值的平均。 |
| 41 | 最小平方法 | Least Squares | 找讓誤差平方和最小的直線。 |
| 42 | 離群值 | Outlier | 離其他資料很遠的點，會把直線拉歪。 |
| 43 | 最佳化 | Optimization | 找讓某個數（損失）最小或最大的參數。 |

## D.4　向量與矩陣（第 4 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 44 | 向量 | Vector | 一串排好順序的數字。 |
| 45 | 純量 | Scalar | 單獨一個數字。 |
| 46 | 維度 | Dimension | 向量裡有幾個數字。 |
| 47 | 向量長度／範數 | Norm | 向量的長度，平方和開根號。 |
| 48 | 內積／點積 | Dot Product | 對應位置相乘再相加。 |
| 49 | 餘弦相似度 | Cosine Similarity | 內積除以兩個長度，只看方向。 |
| 50 | 矩陣 | Matrix | 數字排成的表格。 |
| 51 | 矩陣乘法 | Matrix Multiplication | 列乘欄再相加，代表變換或一整層運算。 |
| 52 | 轉置 | Transpose | 把矩陣的列和欄對調。 |
| 53 | 單位矩陣 | Identity Matrix | 對角線是 1、其他是 0，乘了等於沒變。 |
| 54 | 線性變換 | Linear Transformation | 矩陣對向量做的拉伸、旋轉、鏡射。 |
| 55 | 張量 | Tensor | 向量、矩陣的推廣，可以有更多維；深度學習框架的基本資料型態。 |
| 56 | 形狀 | Shape | 陣列每一維有幾個數字，例如 (8, 8)。 |
| 57 | 像素 | Pixel | 圖片的最小格子，一個灰階值或 RGB 三個值。 |
| 58 | 灰階 | Grayscale | 只有亮暗沒有顏色的圖片。 |
| 59 | NumPy | NumPy | Python 做向量與矩陣運算的套件。 |

## D.5　梯度下降（第 5 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 60 | 梯度 | Gradient | 對每個參數的斜率排成的向量，指向上升最快的方向。 |
| 61 | 梯度下降 | Gradient Descent | 往梯度反方向走一小步，重複，讓損失變小。 |
| 62 | 學習率 | Learning Rate | 每一步走多大。 |
| 63 | 收斂 | Convergence | 損失不再明顯下降，參數穩定下來。 |
| 64 | 發散 | Divergence | 損失越來越大，通常是學習率太大。 |
| 65 | 局部最小值 | Local Minimum | 附近最低、但不是全域最低的點。 |
| 66 | 全域最小值 | Global Minimum | 整個損失曲面上真正最低的點。 |
| 67 | 隨機梯度下降 | Stochastic Gradient Descent, SGD | 每次只用一小批資料算梯度。 |
| 68 | 導數 | Derivative | 函數在某一點的斜率（《數學這樣想（進階）》）。 |
| 69 | 迭代 | Iteration | 重複做一次更新。 |

## D.6　神經元與神經網路（第 6、7 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 70 | 人工神經元 | Artificial Neuron | 加權相加、加偏差、過啟動函數的單元。 |
| 71 | 權重 | Weight | 每個輸入的重要程度。 |
| 72 | 偏差／偏置 | Bias | 加在加權總和上的常數，讓門檻可以移動。 |
| 73 | 感知器 | Perceptron | 最早的單一神經元模型，用階梯函數。 |
| 74 | 啟動函數 | Activation Function | 加權相加之後再過的非線性函數。 |
| 75 | 階梯函數 | Step Function | 大於門檻輸出 1，否則 0。 |
| 76 | sigmoid | Sigmoid | 把任何數壓到 0 到 1 的 S 形函數。 |
| 77 | ReLU | Rectified Linear Unit | 負數變 0、正數照舊。 |
| 78 | tanh | Hyperbolic Tangent | 把數壓到 −1 到 1 的 S 形函數。 |
| 79 | softmax | Softmax | 把一組分數變成加總為 1 的機率。 |
| 80 | 線性可分 | Linearly Separable | 能用一條直線（平面）分開兩類。 |
| 81 | XOR 問題 | XOR Problem | 單層感知器學不會的經典例子。 |
| 82 | 神經網路 | Neural Network | 很多神經元分層連起來的模型。 |
| 83 | 輸入層 | Input Layer | 接收特徵的第一層。 |
| 84 | 隱藏層 | Hidden Layer | 輸入與輸出之間的層。 |
| 85 | 輸出層 | Output Layer | 給出預測的最後一層。 |
| 86 | 全連接層 | Fully Connected Layer | 每個神經元接到上一層的所有神經元。 |
| 87 | 前向傳播 | Forward Propagation | 從輸入一層一層算到輸出。 |
| 88 | 反向傳播 | Backpropagation | 從損失往回算每個參數的梯度。 |
| 89 | 連鎖律 | Chain Rule | 反向傳播背後的數學：一層一層把斜率相乘。 |
| 90 | 梯度消失 | Vanishing Gradient | 深層網路前面幾層的梯度變得極小、學不動。 |
| 91 | 初始化 | Initialization | 訓練前給參數的起始值，通常是小的隨機數。 |

## D.7　訓練真的模型（第 8 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 92 | 資料集 | Dataset | 一整批用來訓練或測試的資料。 |
| 93 | MNIST | MNIST | 70,000 張 28×28 手寫數字的經典資料集。 |
| 94 | 訓練集 | Training Set | 用來調參數的資料。 |
| 95 | 驗證集 | Validation Set | 用來選超參數、看有沒有過擬合的資料。 |
| 96 | 測試集 | Test Set | 最後評估用，訓練時絕不能看。 |
| 97 | epoch | Epoch | 把全部訓練資料看過一遍。 |
| 98 | 批次 | Batch | 一次拿來算梯度的一小批資料。 |
| 99 | 批次大小 | Batch Size | 一批有幾筆。 |
| 100 | 準確率 | Accuracy | 答對的比例。 |
| 101 | 混淆矩陣 | Confusion Matrix | 表格記錄「真實 i 被猜成 j」各幾次。 |
| 102 | 正則化 | Regularization | 限制模型複雜度以減少過擬合的方法。 |
| 103 | Dropout | Dropout | 訓練時隨機關掉一些神經元的正則化方法。 |
| 104 | 早停 | Early Stopping | 驗證損失開始上升就停止訓練。 |
| 105 | 資料增強 | Data Augmentation | 平移、旋轉、加雜訊製造更多訓練資料。 |
| 106 | 損失曲線 | Loss Curve | 損失隨訓練進度變化的折線圖。 |
| 107 | one-hot 編碼 | One-hot Encoding | 用一個只有一格是 1 的向量表示類別。 |
| 108 | PyTorch | PyTorch | 常用的深度學習框架。 |
| 109 | GPU | Graphics Processing Unit | 擅長平行算矩陣的晶片，訓練大模型用它。 |

## D.8　看圖的 AI（第 9 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 110 | 卷積 | Convolution | 用小濾鏡掃過圖片，每個位置做一次內積。 |
| 111 | 濾鏡／卷積核 | Filter / Kernel | 卷積用的小矩陣（例如 3×3）。 |
| 112 | 邊緣偵測 | Edge Detection | 用濾鏡找出圖片裡亮暗變化的邊界。 |
| 113 | 特徵圖 | Feature Map | 卷積後得到的新圖，表示某種模式在哪裡出現。 |
| 114 | 池化 | Pooling | 把一小區域縮成一個值（取最大或平均），讓圖變小。 |
| 115 | 步幅 | Stride | 濾鏡每次移動幾格。 |
| 116 | 填補 | Padding | 圖片邊緣補 0，讓卷積後大小不變。 |
| 117 | 卷積神經網路 | Convolutional Neural Network, CNN | 由卷積層與池化層組成、專長處理圖片的網路。 |
| 118 | 遷移學習 | Transfer Learning | 拿別人在大資料上訓練好的模型，改一點用在自己的任務。 |
| 119 | 預訓練模型 | Pre-trained Model | 已經在大資料上訓練過、可以直接拿來用的模型。 |
| 120 | 通道 | Channel | 圖片的顏色層（RGB 三個）或特徵圖的層數。 |

## D.9　文字變數字（第 10 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 121 | token | Token | 模型處理文字的最小單位，可能是字、詞或詞的一部分。 |
| 122 | 斷詞／分詞 | Tokenization | 把文字切成 token 的過程。 |
| 123 | 詞彙表 | Vocabulary | 模型認得的所有 token 的清單。 |
| 124 | 詞向量／嵌入 | Word Embedding | 把每個詞表示成一個向量，相似的詞向量相近。 |
| 125 | 嵌入層 | Embedding Layer | 神經網路裡把 token 編號換成向量的那一層。 |
| 126 | 共現矩陣 | Co-occurrence Matrix | 記錄哪些詞常在附近一起出現的表。 |
| 127 | 語意相似度 | Semantic Similarity | 兩個詞或句子意思有多接近，用向量相似度估計。 |
| 128 | 相似度搜尋 | Similarity Search | 在一堆向量裡找和查詢最像的幾個。 |
| 129 | 向量資料庫 | Vector Database | 專門存向量、做相似度搜尋的資料庫。 |
| 130 | 詞袋 | Bag of Words | 只數每個詞出現幾次、不管順序的表示法。 |

## D.10　語言模型與 Transformer（第 11 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 131 | 語言模型 | Language Model | 預測下一個字（token）的模型。 |
| 132 | 大型語言模型 | Large Language Model, LLM | 參數極多、在海量文字上訓練的語言模型。 |
| 133 | n-gram | n-gram | 只看前 n 個字來預測下一個字的簡單語言模型。 |
| 134 | 上下文／前文 | Context | 模型在預測時看得到的前面文字。 |
| 135 | 上下文長度 | Context Length | 模型一次最多能看幾個 token。 |
| 136 | 注意力機制 | Attention | 每個字計算該參考其他字多少，用內積算權重。 |
| 137 | 自注意力 | Self-Attention | 一段文字裡的字互相看彼此。 |
| 138 | 查詢、鍵、值 | Query, Key, Value | 注意力裡三種向量：拿什麼去問、用什麼被找、找到後拿什麼。 |
| 139 | Transformer | Transformer | 以注意力為核心的網路結構，現代語言模型的基礎。 |
| 140 | 位置編碼 | Positional Encoding | 告訴模型每個字在第幾個位置的資訊。 |
| 141 | 溫度 | Temperature | 控制取樣隨機程度的參數，低保守、高隨機。 |
| 142 | 取樣 | Sampling | 依機率隨機挑下一個字，而不是永遠挑最大的。 |
| 143 | 貪婪解碼 | Greedy Decoding | 永遠挑機率最大的字。 |
| 144 | 困惑度 | Perplexity | 衡量語言模型預測得多準的數字，越低越好。 |
| 145 | 幻覺 | Hallucination | 模型流暢地說出不正確或不存在的內容。 |
| 146 | 參數量 | Parameter Count | 模型有幾個可訓練的數字，常以 B（十億）為單位。 |

## D.11　訓練聊天 AI（第 12 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 147 | 預訓練 | Pre-training | 用海量文字做「預測下一個字」的訓練。 |
| 148 | 基礎模型 | Base Model | 只做過預訓練、還不會聽指令的模型。 |
| 149 | 微調 | Fine-tuning | 預訓練後用少量特定資料再訓練。 |
| 150 | 指令微調 | Instruction Tuning | 用「問題→理想回答」教模型聽指令。 |
| 151 | 監督式微調 | Supervised Fine-tuning, SFT | 指令微調的另一個名字，強調有標準答案。 |
| 152 | 人類回饋強化學習 | Reinforcement Learning from Human Feedback, RLHF | 人替回答排序→訓練獎勵模型→引導聊天模型。 |
| 153 | 獎勵模型 | Reward Model | 輸入問題與回答，輸出「有多好」的分數。 |
| 154 | 偏好資料 | Preference Data | 「回答 A 比回答 B 好」這類人類標註。 |
| 155 | 標註者 | Annotator / Labeler | 替資料打標籤或排序的人。 |
| 156 | 迎合 | Sycophancy | 模型傾向同意使用者、討好分數的現象。 |
| 157 | 提示詞 | Prompt | 使用者給模型的前文。 |
| 158 | 系統提示 | System Prompt | 服務商放在對話最前面、使用者看不到的指示。 |
| 159 | 少樣本提示 | Few-shot Prompting | 在提示詞裡先給幾個範例。 |
| 160 | 零樣本提示 | Zero-shot Prompting | 不給範例直接問。 |
| 161 | 思維鏈 | Chain of Thought | 要求模型先寫出推理步驟再給答案。 |
| 162 | 檢索增強生成 | Retrieval-Augmented Generation, RAG | 先用相似度找資料，貼進前文再回答。 |
| 163 | 工具使用 | Tool Use | 模型輸出特定格式請外部程式執行（計算、搜尋）。 |
| 164 | 函式呼叫 | Function Calling | 工具使用的一種實作方式。 |
| 165 | AI 代理 | AI Agent | 語言模型加工具加多步迴圈，自己決定下一步。 |
| 166 | 知識截止日 | Knowledge Cutoff | 訓練資料收集到哪一天，之後的事模型不知道。 |

## D.12　限制與安全（第 13 章）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 167 | 偏見 | Bias | 模型對某些群體或情境系統性地不公平或不準確。 |
| 168 | 公平性 | Fairness | 模型對不同群體是否一視同仁。 |
| 169 | 資料洩漏 | Data Leakage | 訓練資料被背出、使用者機密外洩、或測試資料混進訓練。 |
| 170 | 記憶化 | Memorization | 模型把訓練資料原封不動背下來。 |
| 171 | 隱私 | Privacy | 個人資料不被不當收集或揭露。 |
| 172 | 對抗樣本 | Adversarial Example | 刻意加微小雜訊讓模型認錯的輸入。 |
| 173 | 對抗訓練 | Adversarial Training | 把對抗樣本放進訓練資料提高抵抗力。 |
| 174 | 穩健性 | Robustness | 輸入有雜訊或變化時模型還能正確的程度。 |
| 175 | 可解釋性 | Interpretability | 能不能說出模型為什麼給這個答案。 |
| 176 | 黑箱 | Black Box | 看得到輸入輸出、看不懂中間過程的模型。 |
| 177 | 對齊 | Alignment | 模型實際追求的目標與人類想要的目標有多一致。 |
| 178 | 獎勵駭客 | Reward Hacking | 模型找到拿高分的捷徑而不是真的做好。 |
| 179 | 評估 | Evaluation | 有系統地測量模型多好、錯在哪。 |
| 180 | 基準測試 | Benchmark | 公開的固定題庫，用來比較不同模型。 |
| 181 | 分群體評估 | Subgroup Evaluation | 把資料分群各自算準確率，找偏見。 |
| 182 | 校準 | Calibration | 模型說 80% 信心時，是否真的有八成答對。 |
| 183 | 紅隊測試 | Red Teaming | 故意找方法讓模型出錯或做壞事，以便修補。 |
| 184 | 護欄 | Guardrail | 在模型外面加的檢查，擋住不該出現的輸入輸出。 |
| 185 | 負責任的 AI | Responsible AI | 在查證、隱私、公平、問責等方面謹慎使用與開發 AI。 |
| 186 | 問責 | Accountability | 出了錯有人負責，而不是推給「AI 決定的」。 |

## D.13　工具與程式（附錄 B）

| # | 中文 | 英文 | 一句話解釋 |
|---|---|---|---|
| 187 | Colab | Google Colaboratory | 瀏覽器裡的免費 Python 環境。 |
| 188 | 筆記本 | Notebook | Colab 的檔案，由儲存格組成。 |
| 189 | 儲存格 | Cell | 筆記本裡的一格程式或文字。 |
| 190 | 執行階段 | Runtime | Colab 分配給你的那台虛擬電腦。 |
| 191 | 套件 | Package / Library | 別人寫好、可以 import 進來用的程式。 |
| 192 | scikit-learn | scikit-learn, sklearn | 傳統機器學習的 Python 套件（KNN、決策樹、資料集）。 |
| 193 | Matplotlib | Matplotlib | 畫圖的 Python 套件。 |
| 194 | 隨機種子 | Random Seed | 固定它，隨機的結果每次都一樣，方便重現。 |
| 195 | 開源模型 | Open-source Model | 參數公開、任何人都能下載執行的模型。 |
| 196 | Hugging Face | Hugging Face | 存放與分享開源模型的平台。 |
