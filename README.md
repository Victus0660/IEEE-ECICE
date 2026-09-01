# Edge-LLM: On-Device Lightweight Large Language Model Framework for Industrial IoT Sensor Anomaly Diagnosis

[![Conference](https://img.shields.io/badge/IEEE-ECICE%202026-00629B?style=for-the-badge&logo=ieee&logoColor=white)](https://2026.ecice.org/)
[![Hardware](https://img.shields.io/badge/Platform-NVIDIA%20Jetson%20%7C%20Raspberry%20Pi-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://developer.nvidia.com/embedded/jetson-orin-nano-developer-kit)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Quantization](https://img.shields.io/badge/Precision-INT4%20%2F%20INT8%20%2F%20FP16-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://github.com/ggerganov/llama.cpp)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

An autonomous, 100% air-gapped on-device generative diagnostic engine delivering **94.2% F1-score** with **142 ms local response latency** on industrial edge compute nodes.

[Read Full Paper (PDF)](ECICE2026_FullPaper_YiChunTeng.pdf) | [Word Manuscript (DOCX)](ECICE2026_FullPaper_YiChunTeng.docx) | [Overleaf Package (ZIP)](paper.zip) | [Open Dataset (Data)](data/)

---

## Abstract & Overview

Unplanned machine breakdowns stall production lines and cost factories dearly. To catch faults before catastrophic failures occur, industrial plants monitor assets using vibration accelerometers, fiber Bragg grating (FBG) optical strain gauges, infrared thermal probes, and phase current sensors. Yet, conventional edge-deployed TinyML models merely flag anomalies with unhelpful numerical indices or binary alarms—failing to diagnose the underlying physics or instruct technicians on how to respond.

Offloading sensor data to cloud-based language models introduces unacceptable transmission delays (>1.5 s), high cloud API bills, and data confidentiality hazards. Here, we present **Edge-LLM**, an on-premise generative diagnostic framework running 4-bit quantized small language models locally on factory-floor compute nodes.

```
+------------------------+      +--------------------------+      +-------------------------+      +------------------------+
| 1. Industrial Sensors  | ---> | 2. Context Compression   | ---> | 3. Quantized SLM Engine | ---> | 4. Actionable JSON     |
| (12.8 kHz Vibration,   |      | (FFT Harmonics, RMS,     |      | (4-Bit Q4_K_M Kernels,  |      | (Root-Cause, Severity, |
|  FBG Strain, IR Temp)  |      |  ISO 10816 Thresholds)   |      |  Local Vector RAG)      |      |  Prescribed Steps)     |
+------------------------+      +--------------------------+      +-------------------------+      +------------------------+
```

---

## Key Highlights & Innovations

- **100% Air-Gapped Operational Security**: Operates completely on-device with zero external API calls or wide-area network dependency, eliminating proprietary telemetry leakage.
- **Ultra-Low Response Latency**: 4-bit quantized Llama-3.2-1B delivers **42.65 tokens/sec** with **13.75 ms TTFT** on NVIDIA Jetson Orin Nano (end-to-end diagnosis in **142 ms**).
- **Compact Memory Footprint**: Entire system operates within **958 MB RAM** (inclusive of weights, 2048-token KV cache, and CUDA runtime buffers), reserving ample headroom for OS and background tasks.
- **High Explanatory Accuracy**: Achieves **94.2% to 95.9% F1-score** across bearing inner-race spalling, stator winding breakdown, pump cavitation, and shaft coupling misalignment.

---

## Benchmark Results

### 1. Edge Hardware Throughput & Latency (NVIDIA Jetson Orin Nano vs. Raspberry Pi 5)

| Model Architecture | Params | Format | Total RAM (MB) | Jetson TPS (t/s) | Jetson TTFT (ms) | RPi 5 TPS (t/s) | RPi 5 TTFT (ms) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Qwen2.5-0.5B** | 0.5B | INT4 | **586 MB** | **62.74** | 8.92 ms | 23.45 | 38.20 ms |
| **TinyLlama-1.1B** | 1.1B | INT4 | **876 MB** | **44.28** | 12.85 ms | 13.84 | 68.50 ms |
| **Llama-3.2-1B (Recommended)** | 1.2B | INT4 | **958 MB** | **42.65** | **13.75 ms** | **12.65** | **76.40 ms** |
| **Qwen2.5-1.5B** | 1.5B | INT4 | **1216 MB** | **35.12** | 15.80 ms | 9.82 | 94.20 ms |
| **Llama-3.2-3B** | 3.2B | INT4 | **2275 MB** | **17.84** | 24.60 ms | 4.85 | 186.00 ms |
| **Phi-3.5-mini-3.8B** | 3.8B | INT4 | **2664 MB** | **15.22** | 29.80 ms | 3.90 | 235.00 ms |

### 2. Diagnostic Performance Comparison against Baselines

| Diagnostic Method | Precision (%) | Recall (%) | F1-Score (%) | Latency (ms) | Bandwidth (kbps) | Privacy (%)* | Explainability |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1D-CNN (TinyML Baseline)** | 91.2% | 88.5% | 89.8% | **8.5 ms** | 0.0 kbps | 100.0% | Opaque Code Only |
| **Cloud GPT-4o (WAN)** | **97.8%** | **96.5%** | **97.1%** | 1420.0 ms | 128.5 kbps | 35.0% | Full Natural Language |
| **Edge-LLM (Qwen-1.5B INT4)** | 93.8% | 92.4% | 93.1% | 185.0 ms | **0.0 kbps** | **100.0%** | Structured JSON |
| **Edge-LLM (Llama-1B INT4)** | 94.6% | 93.8% | **94.2%** | **142.0 ms** | **0.0 kbps** | **100.0%** | Structured JSON |
| **Edge-LLM (Llama-3B INT4)** | 96.2% | 95.7% | **95.9%** | 320.0 ms | **0.0 kbps** | **100.0%** | Structured JSON |

*\* Note: Privacy (%) measures the proportion of sensitive operational telemetry processed exclusively on-premise without external transmission (100% indicates complete air-gapped security).*

---

## Repository Structure

```
IEEE-ECICE/
├── ECICE2026_FullPaper_YiChunTeng.docx  # Official MDPI Word Paper (6 Pages)
├── ECICE2026_FullPaper_YiChunTeng.pdf   # Official PDF Paper (6 Pages)
├── paper.zip                            # Overleaf-ready LaTeX Bundle
├── README.md                            # Main Project Documentation
├── LICENSE                              # MIT Open-Source License
├── CITATION.cff                         # GitHub Native Citation Metadata
├── requirements.txt                     # Core Python Dependencies
├── data/                                # Open-Source Research Dataset & Logs
│   ├── benchmark_logs/                  # Raw Hardware Profiling Logs (CSV)
│   ├── sensor_telemetry/                # 12.8 kHz Multi-Modal Telemetry (CSV)
│   ├── rag_knowledge_base/              # Maintenance Manuals & Fault Taxonomy (JSON)
│   └── diagnostic_eval_cases/           # 100 Test Scenarios & Predictions (JSON)
├── experiments/                         # Python Experiment Suite & Compilers
│   ├── run_benchmark.py                 # Hardware Profiling & Benchmark Runner
│   ├── sensor_anomaly_eval.py           # Anomaly Diagnostic Metric Evaluator
│   ├── plot_results.py                  # IEEE Publication Chart Generator
│   ├── plot_architecture.py             # System Architecture Diagram Generator
│   ├── generate_official_word_paper.py  # Official MDPI DOCX Paper Compiler
│   └── verify_project_integrity.py      # Automated Syntax & Integrity Validator
└── paper/                               # LaTeX Source Files & Figures
    ├── main.tex                         # Full LaTeX Manuscript
    ├── references.bib                   # BibTeX Literature Database
    ├── IEEEtran.cls                     # IEEE LaTeX Class File
    └── figures/                         # High-Resolution Publication Figures (.pdf/.png)
```

---

## Quick Start & Reproducibility

### 1. Setup Environment
```bash
# Clone the repository
git clone https://github.com/Victus0660/IEEE-ECICE.git
cd IEEE-ECICE

# Install required dependencies
pip install -r requirements.txt
```

### 2. Run Benchmarks & Generate Figures
```bash
# 1. Run inference throughput and latency profiling
python experiments/run_benchmark.py

# 2. Run diagnostic evaluation across 100 test cases
python experiments/sensor_anomaly_eval.py

# 3. Generate high-resolution publication charts
python experiments/plot_architecture.py
python experiments/plot_results.py
```

### 3. Compile Word & PDF Manuscripts
```bash
# Generate official 6-page Word manuscript and verify integrity
python experiments/generate_official_word_paper.py
python experiments/verify_project_integrity.py
```

---

## Citation

```bibtex
@inproceedings{teng2026edgellm,
  author    = {Teng, Yi-Chun},
  title     = {Edge-{LLM}: An On-Device Lightweight Large Language Model Framework for Real-Time Industrial {IoT} Sensor Anomaly Diagnosis},
  booktitle = {Proceedings of the 8th Eurasia Conference on IoT, Communication and Engineering (IEEE ECICE 2026)},
  year      = {2026},
  pages     = {1--6},
  address   = {Yunlin, Taiwan},
  month     = {November}
}
```

---

## Author & Contact

- **Author**: Yi-Chun Teng
- **Affiliation**: Department of Opto-Electronic Engineering, National Dong Hwa University (NDHU), Hualien 97401, Taiwan
- **Email**: victus0110@gmail.com
- **Conference**: [IEEE ECICE 2026 (8th Eurasia Conference on IoT, Communication and Engineering)](https://2026.ecice.org/)
