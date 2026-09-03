# SensorLLM-Edge: An On-Device Lightweight Large Language Model Framework for Real-Time Industrial IoT Sensor Anomaly Diagnosis

[![Conference](https://img.shields.io/badge/IEEE-ECICE%202026-00629B?style=for-the-badge&logo=ieee&logoColor=white)](https://2026.ecice.org/)
[![Hardware](https://img.shields.io/badge/Platform-NVIDIA%20Jetson%20%7C%20Raspberry%20Pi-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://developer.nvidia.com/embedded/jetson-orin-nano-developer-kit)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Quantization](https://img.shields.io/badge/Precision-INT4%20%2F%20INT8%20%2F%20FP16-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://github.com/ggerganov/llama.cpp)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

Official open-source research dataset, empirical hardware profiling logs, multi-modal telemetry waveforms, and reproducible edge benchmark scripts for the paper:
> **"SensorLLM-Edge: An On-Device Lightweight Large Language Model Framework for Real-Time Industrial IoT Sensor Anomaly Diagnosis"**  
> *Presented at the 8th Eurasia Conference on IoT, Communication and Engineering (IEEE ECICE 2026)*

[Explore Dataset (data/)](data/) | [Hardware Benchmark Suite](experiments/) | [Citation](#citation)

---

## Abstract & System Overview

Unexpected mechanical breakdowns halt manufacturing lines and increase operating costs. While plants deploy accelerometers, fiber Bragg grating (FBG) optical strain sensors, infrared probes, and current transformers for early fault detection, conventional microcontroller TinyML classifiers merely output discrete fault IDs or binary flags without root-cause explanations or repair guidance. Conversely, streaming raw sensor streams to cloud LLMs incurs network latency spikes (>1.4 s), recurring costs, and severe telemetry privacy risks.

To overcome these constraints, we propose **SensorLLM-Edge**, an air-gapped framework executing 4-bit quantized small language models (SLMs) on industrial edge gateways. The pipeline couples a sliding-window temporal encoder with an onboard vector repository, converting 12.8 kS/s telemetry into structured JSON repair guidance without external connectivity.

```
+--------------------------+      +--------------------------+      +-------------------------+      +------------------------+
| 1. Multi-Modal Sensors   | ---> | 2. Context Compression   | ---> | 3. Quantized SLM Engine | ---> | 4. Local RAG Output    |
| (12.8 kHz Accel, FBG     |      | (Sliding-window FFT,     |      | (4-Bit Q4_K_M Kernels,  |      | (Offline Vector SOPs,  |
|  Optical Strain, IR Py)  |      |  ISO 10816 Thresholds)   |      |  FlashAttention, Cache) |      |  Triage: 142 ms)       |
+--------------------------+      +--------------------------+      +-------------------------+      +------------------------+
```

---

## Key Highlights & Innovations

- **100% Air-Gapped Operational Security**: Operates completely on-device with zero external API calls or wide-area network dependency, eliminating proprietary telemetry leakage.
- **Two-Tier Low-Latency Diagnostics**: 4-bit quantized Llama-3.2-1B delivers **42.65 tokens/sec** with **13.75 ms TTFT** on NVIDIA Jetson Orin Nano—completing real-time triage diagnosis (fault identification & severity) in **142 ms**, followed by complete step-by-step repair guidance within **1.18 s**.
- **Compact Memory Footprint**: Entire system operates within **958 MB RAM** (inclusive of weights, 2048-token KV cache, and runtime context), reserving ample headroom for OS and concurrent industrial services.
- **High Explanatory Accuracy**: Achieves **94.2% to 95.9% macro-average F1-score** across bearing inner-race spalling (BPFI), stator winding breakdown, pump cavitation, and shaft coupling misalignment.

---

## Empirical Benchmark Results

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

| Diagnostic Method | Precision (%) | Recall (%) | F1-Score (%) | Latency (ms) | Bandwidth (kbps) | Privacy (%)* | Output Format |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **1D-CNN (TinyML Baseline)** | 91.2% | 88.5% | 89.8% | **8.5 ms** | 0.0 kbps | 100.0% | Opaque Code Only |
| **Cloud GPT-4o (WAN)** | **97.8%** | **96.5%** | **97.1%** | 1420.0 ms | 128.5 kbps | 35.0% | Full Natural Language |
| **SensorLLM-Edge (Qwen-1.5B INT4)** | 93.8% | 92.4% | 93.1% | 185.0 ms | **0.0 kbps** | **100.0%** | Structured JSON |
| **SensorLLM-Edge (Llama-1B INT4)** | 94.6% | 93.8% | **94.2%** | **142.0 ms** | **0.0 kbps** | **100.0%** | Structured JSON |
| **SensorLLM-Edge (Llama-3B INT4)** | 96.2% | 95.7% | **95.9%** | 320.0 ms | **0.0 kbps** | **100.0%** | Structured JSON |

*\* Note: Privacy (%) measures the proportion of sensitive operational telemetry processed exclusively on-premise without external transmission (100% indicates complete air-gapped security).*

---

## 📂 Open-Source Dataset Catalog (`data/`)

```
data/
├── benchmark_logs/
│   ├── hardware_profiling_jetson_orin_nano.csv  # 10 trials per model (RAM, VRAM, TTFT, TPS, Power, Temp)
│   └── hardware_profiling_raspberry_pi_5.csv    # 10 trials per model (RAM, TTFT, TPS, CPU Util, Power)
├── sensor_telemetry/
│   ├── case_00_normal_baseline.csv              # ISO 10816 Class I/II baseline telemetry (12.8 kHz NI-9234)
│   ├── case_01_bearing_spall_bpfi.csv           # Bearing inner-race fault (BPFI 148 Hz impact bursts)
│   ├── case_02_stator_winding_insulation.csv    # Stator inter-turn insulation breakdown (14% unbalance)
│   ├── case_03_pump_cavitation.csv              # Centrifugal pump cavitation broadband spectral spikes
│   └── case_04_shaft_misalignment.csv           # 1X & 2X rotational harmonic coupling misalignment
├── rag_knowledge_base/
│   ├── maintenance_manuals.json                 # Offline maintenance SOPs & repair checklists
│   └── fault_taxonomy_and_guidelines.json       # ISO 10816 vibration severity zones & fault taxonomy
└── diagnostic_eval_cases/
    ├── 100_industrial_scenarios_ground_truth.json # 100 test cases with prompts and ground truth
    └── model_predictions_comparison.json        # Detailed precision, recall, F1, latency breakdown
```

---

## 🚀 Quick Start & Reproducibility

### 1. Setup Environment
```bash
# Clone repository
git clone https://github.com/Victus0660/IEEE-ECICE.git
cd IEEE-ECICE

# Install lightweight dependencies
pip install -r requirements.txt
```

### 2. Run Benchmarks & Diagnostic Evaluation
```bash
# Run hardware inference profiler
python experiments/run_benchmark.py

# Run diagnostic accuracy evaluator across 100 test cases
python experiments/sensor_anomaly_eval.py
```

---

## Citation

```bibtex
@inproceedings{teng2026sensorllmedge,
  author    = {Teng, Yi-Chun},
  title     = {SensorLLM-Edge: An On-Device Lightweight Large Language Model Framework for Real-Time Industrial {IoT} Sensor Anomaly Diagnosis},
  booktitle = {Proceedings of the 8th Eurasia Conference on IoT, Communication and Engineering (IEEE ECICE 2026)},
  year      = {2026},
  pages     = {1--6},
  address   = {Yunlin, Taiwan},
  month     = {November}
}
```

---

## Author & Contact

- **Author**: Yi-Chun Teng (National Dong Hwa University, Hualien, Taiwan)
- **Email**: victus0110@gmail.com
- **Conference**: [IEEE ECICE 2026 (8th Eurasia Conference on IoT, Communication and Engineering)](https://2026.ecice.org/)
- **Repository**: [https://github.com/Victus0660/IEEE-ECICE](https://github.com/Victus0660/IEEE-ECICE)
