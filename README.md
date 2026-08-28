# IEEE ECICE 論文發表專案：Edge-LLM

本專案包含投稿至 **IEEE ECICE (IEEE Eurasia Conference on IoT, Communication and Engineering)** 的完整論文源碼、實驗數據、圖表生成腳本與文獻資料庫。

---

## 📁 專案目錄結構

* **`paper/`**：LaTeX 論文源碼（符合 IEEE 官方雙欄格式）
  * `main.tex`：論文主文件（包含完整的 Introduction、Related Work、Methodology、Experiments、Conclusion）
  * `references.bib`：2023–2026 年最新 IEEE/ACM/arXiv BibTeX 文獻庫
  * `IEEEtran.cls`：IEEE 官方 LaTeX 格式類別檔
  * `figures/`：論文所需之所有出版級圖表（提供向量 `.pdf` 與高解析度 `.png`）
* **`experiments/`**：Python 實驗與基準測試程式
  * `run_benchmark.py`：邊緣 LLM 推論延遲、記憶體佔用與吞吐量評估腳本
  * `sensor_anomaly_eval.py`：工業物聯網感測器異常診斷評估測試
  * `plot_results.py`：繪製 IEEE 雙欄出版級實驗圖表
  * `plot_architecture.py`：繪製系統架構圖
* **`docs/`**：論文規劃與文獻筆記
  * `paper_outline.md`：論文架構大綱與核心創新亮點
  * `literature_notes.md`：最新文獻調研與技術比較

---

## 🚀 如何在 Overleaf 或本地編譯論文

### 方法 A：使用 Overleaf（推薦，最方便）
1. 將 `paper/` 資料夾打包壓縮成 `paper.zip`。
2. 開啟 [Overleaf](https://www.overleaf.com/)，點選 **New Project** $\rightarrow$ **Upload Project**，上傳該 zip 檔。
3. 點選 **Recompile** 即可直接預覽與下載 IEEE 雙欄格式 PDF！

### 方法 B：本地編譯（若有安裝 TeX Live / MiKTeX）
在 `paper/` 目錄下執行：
```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

---

## 📊 如何重新執行實驗並繪圖

在專案根目錄下使用 Python 執行：
```bash
# 1. 執行基準測試與診斷評估
python experiments/run_benchmark.py
python experiments/sensor_anomaly_eval.py

# 2. 重新產生出版級圖表
python experiments/plot_architecture.py
python experiments/plot_results.py
```
生成的圖表將自動更新至 `paper/figures/` 目錄。
