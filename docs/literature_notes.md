# Literature Notes: Edge LLM for Industrial IoT Anomaly Diagnosis

## 1. On-Device & Edge LLM Deployment (2023–2026)
1. **Llama 3.2 Series (Meta, 2024)**:
   - Introduces lightweight 1B and 3B parameter models tailored for on-device deployment (mobile, edge ARM, edge GPU).
   - High instruction-following capability with minimal memory footprint (e.g. 1B model requires ~1.3 GB under 4-bit quantization).
2. **Qwen2.5 Series (Alibaba, 2024–2025)**:
   - Includes 0.5B, 1.5B, and 3B compact models with strong reasoning and structured output (JSON/Code) capabilities.
3. **Quantization & Edge Inference Runtimes**:
   - **GGUF / llama.cpp (Gerganov et al., 2023–2025)**: High-performance CPU/GPU inference with k-quants (Q4_K_M, Q5_K_M, Q8_0).
   - **AWQ (Lin et al., MLSys 2024)** & **GPTQ (Frantar et al., ICLR 2023)**: Activation-aware weight quantization preserving accuracy in edge settings.
   - **Speculative Decoding (Leviathan et al., ICML 2023 / Xu et al., IEEE TMC 2025)**: Accelerates small model inference on resource-constrained devices.

## 2. Industrial IoT Sensor Anomaly Detection & Reasoning
1. **Generative IoT (GIoT) (Firouzi et al., IEEE, 2026)**:
   - Explores convergence of Generative AI, LLMs, and IoT ecosystems for industrial intelligence and autonomous operations.
2. **LLM Edge-Intelligence Survey (Nam et al., 2026)**:
   - Reviews trade-offs among memory, compute bandwidth, latency, and reasoning capability across edge hardware platforms.
3. **Industrial Anomaly Diagnosis vs. Binary Detection**:
   - Traditional TinyML/ML (Autoencoders, Isolation Forest, 1D-CNN) detects *that* an anomaly occurred (binary 0/1 or anomaly score).
   - *Problem*: Machine operators need immediate root-cause explanation (e.g., "Vibration spectral peak at 120Hz suggests bearing outer race fault due to lubrication depletion") and step-by-step mitigation actions.
   - *Proposed Edge-LLM solution*: Converts continuous time-series feature summaries into semantic prompts, runs local quantized inference with zero cloud latency and complete data privacy.

## 3. Key Research Gap & Our Contributions
| Dimension | Traditional Cloud LLM | Traditional Edge TinyML | **Our Proposed Edge-LLM** |
| :--- | :--- | :--- | :--- |
| **Connectivity** | Requires stable high-bandwidth WAN | Offline local execution | **100% Offline, Zero Cloud Dependency** |
| **Privacy & Security** | Telemetry logs exposed to 3rd-party cloud | Data stays on-device | **Zero Data Leakage (Edge Air-Gapped)** |
| **Latency** | 800ms ~ 3000ms (Network + Queue) | < 10ms (Binary only) | **150ms ~ 450ms (Full Explanatory Diagnostic)** |
| **Output Richness** | Rich explanations & advice | Raw score / Class index | **Structured Root-Cause + Actionable Steps** |
| **Memory / HW Cost** | Huge GPU clusters (A100/H100) | Microcontrollers (KB/MB) | **Edge Devices (< 2GB RAM / Jetson / RPi / Mini-PC)** |
