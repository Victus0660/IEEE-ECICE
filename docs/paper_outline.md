# IEEE ECICE 論文大綱與核心架構設計

## 題目 (Paper Title)
**Edge-LLM: An On-Device Lightweight Large Language Model Framework for Real-Time Industrial IoT Sensor Anomaly Diagnosis**
*(邊緣 LLM：應用於即時工業物聯網感測器異常診斷之裝置端輕量化大型語言模型架構)*

---

## 核心亮點與創新貢獻 (Key Innovations)
1. **零雲端依賴與 100% 隱私保護 (Air-Gapped Privacy)**：所有遙測資料與診斷推論皆在邊緣裝置（如 NVIDIA Jetson / 樹莓派）本地執行，徹底杜絕工廠敏感數據外洩。
2. **語意特徵壓縮與滑動窗口編碼 (Temporal Context Compression)**：將高頻連續震動與溫度數據轉換為高密度語意 Prompt，大幅降低 Token 長度並提升推論速度。
3. **極致量化與即時推論 (INT4 Post-Training Quantization)**：
   - 1.2B 參數模型量化後僅需 **672 MB** 記憶體（壓縮比達 3.57x）。
   - 首字延遲 (TTFT) 低至 **55 ms**，整體診斷輸出僅需 **142 ms**。
4. **高診斷準確率 (High Explainability & Accuracy)**：在軸承損傷、馬達過熱、泵浦氣蝕等典型工業異常案例中，診斷 F1-Score 達 **94.2% ~ 95.9%**，媲美雲端巨型模型（GPT-4o 97.1%），並能生成即時維修指引。

---

## 各章節結構設計 (Sections Overview)

```
I. INTRODUCTION
   ├── 工業 4.0 旋轉機械狀態監控 (CBM/PHM) 背景
   ├── 傳統 TinyML 缺點（缺乏可解釋性、僅有 0/1 標籤）
   ├── 雲端 LLM 缺點（網路延遲高、斷網風險、數據隱私外洩）
   └── Edge-LLM 提出與 4 大貢獻總結

II. RELATED WORK
   ├── Edge Intelligence & TinyML in IIoT
   ├── Generative AI & LLM in IoT (GIoT)
   └── Model Quantization & Edge Acceleration (AWQ / GGUF / Speculative Decoding)

III. PROPOSED EDGE-LLM FRAMEWORK
   ├── 系統整體架構 (System Architecture: 4-stage Pipeline)
   ├── 時序特徵提取與語意 Prompt 編碼器 (Feature Encoder)
   ├── 輕量化 SLM 引擎與 INT4/INT8 量化機制 (Quantized SLM Engine)
   └── 本地維修知識庫 RAG 檢索生成 (Offline RAG)

IV. EXPERIMENTAL EVALUATION
   ├── 實驗環境 (Jetson Orin Nano vs. Raspberry Pi 5)
   ├── 推論延遲與吞吐量評估 (Latency & Throughput: Tokens/sec & TTFT)
   ├── 記憶體佔用與量化效率 (RAM Footprint vs. 4GB Edge Limit)
   └── 診斷準確度與工業案例研究 (Accuracy, F1-score & Pareto Frontier)

V. DISCUSSION AND LIMITATIONS
   ├── 長週期退化趨勢分析之上下文窗口處理
   └── 無風扇邊緣閘道器之功耗與溫控策略 (Event-triggered activation)

VI. CONCLUSION AND FUTURE WORK
   ├── 全文成果總結
   └── 未來展望 (On-device LoRA Continual Learning & Multi-agent Edge Swarm)
```
