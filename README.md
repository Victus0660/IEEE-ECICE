# Edge-LLM: On-Device Lightweight LLM Framework for Industrial IoT Anomaly Diagnosis

Official research repository and open-source artifacts for the IEEE ECICE 2026 conference paper:
> **Edge-LLM: An On-Device Lightweight Large Language Model Framework for Real-Time Industrial IoT Sensor Anomaly Diagnosis**  
> *Author: Yi-Chun Teng (National Dong Hwa University, Taiwan)*  
> *Email: victus0110@gmail.com*

---

## Repository Structure

- **data/**: Complete public dataset, hardware logs, sensor waveforms, and RAG knowledge base.
  - enchmark_logs/: Raw hardware profiling logs for NVIDIA Jetson Orin Nano & Raspberry Pi 5.
  - sensor_telemetry/: Multi-modal time series (vibration, FBG optical strain, IR temp, 3-phase current).
  - 
ag_knowledge_base/: ISO 10816 maintenance manuals & fault taxonomy.
  - diagnostic_eval_cases/: 100 multi-fault test cases & model comparison predictions.
- **paper/**: LaTeX source code & publication-grade vector figures (.pdf and .png).
  - main.tex: Full paper LaTeX source.
  - 
eferences.bib: Cleaned 2023–2026 reference database.
- **experiments/**: Benchmark scripts & figure generation tools.
  - 
un_benchmark.py: Physical hardware inference benchmark runner.
  - plot_results.py: Generates all IEEE publication figures.
  - generate_official_word_paper.py: Builds the official MDPI Word paper (.docx).
  - erify_project_integrity.py: Syntax, citation, and column integrity validator.
- **ECICE2026_FullPaper_YiChunTeng.docx**: Official Word manuscript (MDPI template, exactly 6 pages).
- **ECICE2026_FullPaper_YiChunTeng.pdf**: Official PDF manuscript (Native Word COM export, exactly 6 pages).
- **paper.zip**: Overleaf-ready compilation bundle.

---

## Quick Start & Reproducibility

`ash
# 1. Run physical benchmark simulation
python experiments/run_benchmark.py

# 2. Re-generate all IEEE publication figures
python experiments/plot_results.py

# 3. Build Word & PDF Manuscripts
python experiments/generate_official_word_paper.py
python experiments/verify_project_integrity.py
`
