"""
Publication-Grade Chart Generator for IEEE Conference Papers
Generates IEEE standard 3.5-inch single-column / 7-inch double-column figures.
"""

import json
import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# Configure IEEE Publication Style
matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.size'] = 9
matplotlib.rcParams['axes.labelsize'] = 9
matplotlib.rcParams['axes.titlesize'] = 10
matplotlib.rcParams['xtick.labelsize'] = 8
matplotlib.rcParams['ytick.labelsize'] = 8
matplotlib.rcParams['legend.fontsize'] = 8
matplotlib.rcParams['figure.titlesize'] = 10
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(os.path.dirname(BASE_DIR), "paper", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def load_data():
    bench_file = os.path.join(BASE_DIR, "benchmark_results.json")
    acc_file = os.path.join(BASE_DIR, "accuracy_results.json")

    if not os.path.exists(bench_file):
        raise FileNotFoundError(
            f"benchmark_results.json not found. Run run_benchmark.py first.\n  Expected: {bench_file}"
        )
    if not os.path.exists(acc_file):
        raise FileNotFoundError(
            f"accuracy_results.json not found. Run sensor_anomaly_eval.py first.\n  Expected: {acc_file}"
        )

    with open(bench_file, "r", encoding="utf-8") as f:
        bench_data = json.load(f)
    with open(acc_file, "r", encoding="utf-8") as f:
        acc_data = json.load(f)

    return bench_data, acc_data

def plot_latency_throughput(bench_data):
    models = ["Qwen-0.5B", "Llama3.2-1B", "Qwen-1.5B", "Llama3.2-3B", "Phi-3.5-3.8B"]
    raw_models = ["Qwen2.5-0.5B", "Llama-3.2-1B", "Qwen2.5-1.5B", "Llama-3.2-3B", "Phi-3.5-mini-3.8B"]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.7), dpi=300)
    
    jetson_data = {entry["model"] + "_" + entry["quantization"]: entry for entry in bench_data["Jetson_Orin_Nano_8GB"]}
    rpi_data = {entry["model"] + "_" + entry["quantization"]: entry for entry in bench_data["Raspberry_Pi_5_8GB"]}
    
    x = np.arange(len(models))
    width = 0.25
    
    # Subplot 1: Throughput (Tokens/s) on Jetson Orin Nano
    t_fp16 = [jetson_data[m + "_FP16"]["tokens_per_sec"] for m in raw_models]
    t_int8 = [jetson_data[m + "_INT8"]["tokens_per_sec"] for m in raw_models]
    t_int4 = [jetson_data[m + "_INT4 (Q4_K_M)"]["tokens_per_sec"] for m in raw_models]
    
    ax1.bar(x - width, t_fp16, width, label='FP16 Baseline', color='#708090', edgecolor='black', linewidth=0.6)
    ax1.bar(x, t_int8, width, label='INT8 (AWQ)', color='#4682B4', edgecolor='black', linewidth=0.6)
    ax1.bar(x + width, t_int4, width, label='INT4 (Q4_K_M)', color='#2E8B57', edgecolor='black', linewidth=0.6)
    
    ax1.set_ylabel('Throughput (Tokens / sec)')
    ax1.set_title('(a) Inference Throughput (Jetson Orin Nano)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(models, rotation=18)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.legend(frameon=True, facecolor='white', framealpha=0.9)
    
    # Subplot 2: Time to First Token (TTFT) Comparison across Platforms (INT4)
    ttft_jetson = [jetson_data[m + "_INT4 (Q4_K_M)"]["ttft_ms"] for m in raw_models]
    ttft_rpi = [rpi_data[m + "_INT4 (Q4_K_M)"]["ttft_ms"] for m in raw_models]
    
    w2 = 0.35
    ax2.bar(x - w2/2, ttft_jetson, w2, label='Jetson Orin Nano (Edge GPU)', color='#2E8B57', edgecolor='black', linewidth=0.6)
    ax2.bar(x + w2/2, ttft_rpi, w2, label='Raspberry Pi 5 (Edge CPU)', color='#E06666', edgecolor='black', linewidth=0.6)
    
    ax2.set_ylabel('Time to First Token - TTFT (ms)')
    ax2.set_title('(b) Prompt Evaluation Latency (INT4)')
    ax2.set_xticks(x)
    ax2.set_xticklabels(models, rotation=18)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    ax2.legend(frameon=True, facecolor='white', framealpha=0.9)
    
    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_latency_throughput.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIG_DIR, "fig_latency_throughput.png"), bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Saved fig_latency_throughput.pdf & .png")

def plot_memory_footprint(bench_data):
    raw_models = ["Qwen2.5-0.5B", "TinyLlama-1.1B", "Llama-3.2-1B", "Qwen2.5-1.5B", "Llama-3.2-3B", "Phi-3.5-mini-3.8B"]
    models = ["Qwen-0.5B", "TinyLlama-1.1B", "Llama3.2-1B", "Qwen-1.5B", "Llama3.2-3B", "Phi-3.5-3.8B"]
    
    jetson_data = {entry["model"] + "_" + entry["quantization"]: entry for entry in bench_data["Jetson_Orin_Nano_8GB"]}
    
    fp16_mem = [jetson_data[m + "_FP16"]["ram_footprint_mb"] for m in raw_models]
    int8_mem = [jetson_data[m + "_INT8"]["ram_footprint_mb"] for m in raw_models]
    int4_mem = [jetson_data[m + "_INT4 (Q4_K_M)"]["ram_footprint_mb"] for m in raw_models]
    
    fig, ax = plt.subplots(figsize=(3.5, 2.7), dpi=300)
    x = np.arange(len(models))
    width = 0.25
    
    ax.bar(x - width, fp16_mem, width, label='FP16 (Uncompressed)', color='#A9A9A9', edgecolor='black', linewidth=0.6)
    ax.bar(x, int8_mem, width, label='INT8 Quantized', color='#4682B4', edgecolor='black', linewidth=0.6)
    ax.bar(x + width, int4_mem, width, label='INT4 Quantized', color='#3CB371', edgecolor='black', linewidth=0.6)
    
    ax.axhline(y=4096, color='red', linestyle=':', label='4GB RAM Edge Limit', linewidth=1.0)
    
    ax.set_ylabel('Memory Footprint (MB)')
    ax.set_title('Edge Memory Allocation (RAM / VRAM)')
    ax.set_xticks(x)
    ax.set_xticklabels(models, rotation=35, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    ax.legend(loc='upper left', frameon=True, facecolor='white', framealpha=0.9, fontsize=7)
    
    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_memory_footprint.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIG_DIR, "fig_memory_footprint.png"), bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Saved fig_memory_footprint.pdf & .png")

def plot_pareto_frontier(acc_data):
    fig, ax = plt.subplots(figsize=(3.5, 2.7), dpi=300)
    
    methods = acc_data["comparison"]
    
    markers = {'Traditional_TinyML (1D-CNN)': 's', 
               'Cloud_LLM (GPT-4o via WAN)': '^', 
               'Edge_LLM_Qwen2.5_1.5B (INT4)': 'o', 
               'Proposed_Edge_LLM_Llama3.2_1B (INT4)': 'D', 
               'Proposed_Edge_LLM_Llama3.2_3B (INT4)': '*'}
               
    colors = {'Traditional_TinyML (1D-CNN)': '#E74C3C', 
              'Cloud_LLM (GPT-4o via WAN)': '#3498DB', 
              'Edge_LLM_Qwen2.5_1.5B (INT4)': '#F39C12', 
              'Proposed_Edge_LLM_Llama3.2_1B (INT4)': '#27AE60', 
              'Proposed_Edge_LLM_Llama3.2_3B (INT4)': '#2ECC71'}
              
    labels = {
        'Traditional_TinyML (1D-CNN)': 'TinyML 1D-CNN (Binary only)',
        'Cloud_LLM (GPT-4o via WAN)': 'Cloud LLM (GPT-4o + WAN)',
        'Edge_LLM_Qwen2.5_1.5B (INT4)': 'Edge Qwen2.5-1.5B (INT4)',
        'Proposed_Edge_LLM_Llama3.2_1B (INT4)': 'Ours: Llama-3.2-1B (INT4)',
        'Proposed_Edge_LLM_Llama3.2_3B (INT4)': 'Ours: Llama-3.2-3B (INT4)'
    }
    
    for key, val in methods.items():
        lat = val["response_latency_ms"]
        f1 = val["f1_score"]
        ax.scatter(lat, f1, s=70 if '3B' not in key else 110, color=colors[key], marker=markers[key], 
                   label=labels[key], edgecolors='black', linewidth=0.7, zorder=5)
        
    ax.set_xscale('log')
    ax.set_xlabel('Response Latency (ms, Log Scale)')
    ax.set_ylabel('Diagnostic F1-Score (%)')
    ax.set_title('Accuracy vs. Latency Trade-Off')
    ax.grid(True, which="both", ls="--", alpha=0.4)
    ax.set_ylim(85, 100)
    ax.legend(loc='lower right', frameon=True, facecolor='white', framealpha=0.9, fontsize=6.5)
    
    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_diagnostic_accuracy.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIG_DIR, "fig_diagnostic_accuracy.png"), bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Saved fig_diagnostic_accuracy.pdf & .png")

if __name__ == "__main__":
    bench_data, acc_data = load_data()
    plot_latency_throughput(bench_data)
    plot_memory_footprint(bench_data)
    plot_pareto_frontier(acc_data)
    print("All IEEE figures updated successfully!")
