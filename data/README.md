# Edge-LLM Open-Source Dataset & Hardware Benchmark Repository

This directory contains the complete public datasets, empirical hardware profiling logs, multi-modal sensor telemetry, offline RAG maintenance manuals, and diagnostic evaluation scenarios supporting the paper:

> **Edge-LLM: An On-Device Lightweight Large Language Model Framework for Real-Time Industrial IoT Sensor Anomaly Diagnosis**  
> *8th Eurasia Conference on IoT, Communication and Engineering (IEEE ECICE 2026)*  
> *Author: Yi-Chun Teng (National Dong Hwa University, Taiwan)*  
> *GitHub Repository: https://github.com/Victus0660/IEEE-ECICE*

---

## Directory Structure

- **enchmark_logs/**:
  - hardware_profiling_jetson_orin_nano.csv (10 trials per model: RAM, VRAM, TTFT, TPS, Power, Temp)
  - hardware_profiling_raspberry_pi_5.csv (10 trials per model: RAM, TTFT, TPS, CPU Util, Power)
- **sensor_telemetry/**:
  - case_00_normal_baseline.csv (ISO 10816 Class I/II baseline telemetry)
  - case_01_bearing_spall_bpfi.csv (Bearing inner-race fault: BPFI 148 Hz impact bursts)
  - case_02_stator_winding_insulation.csv (Stator inter-turn insulation breakdown: 14% unbalance)
  - case_03_pump_cavitation.csv (Pump cavitation broadband acoustic emission)
  - case_04_shaft_misalignment.csv (1X & 2X rotational harmonic coupling misalignment)
- **ag_knowledge_base/**:
  - maintenance_manuals.json (Offline maintenance SOPs & repair checklists)
  - ault_taxonomy_and_guidelines.json (ISO 10816 vibration severity zones & fault taxonomy)
- **diagnostic_eval_cases/**:
  - 100_industrial_scenarios_ground_truth.json (100 test cases with prompts and ground truth)
  - model_predictions_comparison.json (Detailed precision, recall, F1, latency breakdown)
