# IEEE ECICE Paper Outline & Framework Architecture

## Paper Title
**Edge-LLM: An On-Device Lightweight Large Language Model Framework for Real-Time Industrial IoT Sensor Anomaly Diagnosis**

---

## Core Innovations & Key Contributions
1. **Zero Cloud Dependency & Complete Air-Gapped Privacy**: All sensor telemetry and generative diagnostic inference execute entirely on-premise on edge nodes (NVIDIA Jetson / Raspberry Pi 5), preventing sensitive shop-floor data leakage.
2. **Temporal Feature Compression & Sliding-Window Encoding**: Converts high-frequency vibration, FBG optical strain, and thermal time series into compact semantic prompts, reducing token length and inference latency.
3. **Hardware-Efficient INT4 Quantization**:
   - 1.2B parameter model operates within **958 MB** total RAM (inclusive of 2048-token KV cache and CUDA runtime overhead).
   - Time to First Token (TTFT) is below **15 ms** on edge GPU, with end-to-end diagnostic response in **142 ms**.
4. **Actionable Explanatory Precision**: Across bearing spalls, stator winding breakdown, cavitation, and coupling misalignment, Edge-LLM achieves **94.2% to 95.9%** diagnostic F1-scores while generating structured JSON repair guidance.

---

## Section Structure Overview

`
I. INTRODUCTION
   ├── Industrial Condition-Based Maintenance (CBM) & Rotating Machinery Background
   ├── Limitations of Edge TinyML (Opaque Black-Box Classifiers, Numerical Labels Only)
   ├── Limitations of Cloud LLMs (Latency Spikes > 1.5s, WAN Disconnects, Data Exposure)
   └── Edge-LLM Framework Introduction & Summary of Four Core Contributions

II. RELATED WORK
   ├── Edge Intelligence & TinyML in Smart Manufacturing
   ├── Generative IoT (GIoT) & Industrial Language Models
   └── Post-Training Quantization & Runtime Acceleration (AWQ / GPTQ / GGUF / Speculative Decoding)

III. PROPOSED EDGE-LLM FRAMEWORK
   ├── 4-Stage End-to-End System Pipeline (Figure 1)
   ├── Sliding-Window Statistical Feature Encoding & Semantic Prompting
   ├── Quantized SLM Engine & Attention Memory Management
   └── Offline Retrieval-Augmented Generation (Local RAG)

IV. EXPERIMENTAL EVALUATION
   ├── Hardware Testbeds (NVIDIA Jetson Orin Nano vs. Raspberry Pi 5)
   ├── Token Generation Throughput & Time to First Token (Figure 2)
   ├── Memory Allocation & Quantization Scaling relative to 4 GB Limit (Figure 3)
   └── Multi-Fault Diagnostic Accuracy, Pareto Frontier & Case Study (Table 1)

V. DISCUSSION AND ENGINEERING CONSIDERATIONS
   ├── Long-Term Degradation Tracking via Daily Statistical Summaries
   └── Thermal Management & Event-Driven Activation in Fanless IP67 Enclosures

VI. CONCLUSION AND FUTURE WORK
   ├── Summary of Findings
   ├── Author Contributions, Funding, IRB, Consent, Data Availability, Conflicts of Interest
   └── Future Directions (On-Device QLoRA Calibration & Multi-Node Swarm Collaboration)
`
