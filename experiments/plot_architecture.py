"""
Generates IEEE Publication System Architecture Diagram for SensorLLM-Edge
Aligns Column 2 (Context Encoder) and Column 4 (Local RAG & Actionable Output)
"""

import os
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches

matplotlib.rcParams['font.family'] = 'serif'
matplotlib.rcParams['font.size'] = 8.5
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42

FIG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "paper", "figures")
os.makedirs(FIG_DIR, exist_ok=True)

def generate_architecture_diagram():
    fig, ax = plt.subplots(figsize=(7.1, 3.1), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 52)
    ax.axis('off')

    # Color Palette (Professional IEEE)
    c_iot = '#EBF5FB'      # Soft Blue
    c_edge = '#E8F8F5'     # Soft Green
    c_llm = '#FEF9E7'      # Soft Yellow
    c_out = '#F5EEF8'      # Soft Purple
    border_blue = '#2980B9'
    border_green = '#27AE60'
    border_yellow = '#D4AC0D'
    border_purple = '#8E44AD'

    # 1. Block: Industrial IoT Sensor Layer
    rect1 = patches.FancyBboxPatch((2, 4), 20, 43, boxstyle="round,pad=0.4", 
                                  fc=c_iot, ec=border_blue, lw=1.4)
    ax.add_patch(rect1)
    ax.text(12, 43, "1. Industrial IoT\nSensors & Telemetry", weight='bold', ha='center', va='center', color='#1B4F72', fontsize=8.5)
    sensor_items = [
        "• Tri-axial Accel (g)",
        "• FBG Optical Strain",
        "• IR Pyrometer (°C)",
        "• 3-Phase Current (A)",
        "• 12.8 kHz NI-9234 DAQ"
    ]
    for i, item in enumerate(sensor_items):
        ax.text(3.5, 33 - i * 6.2, item, fontsize=7.5, color='#2C3E50')

    # 2. Block: Edge Context Compression & Feature Encoder
    rect2 = patches.FancyBboxPatch((27, 4), 22, 43, boxstyle="round,pad=0.4", 
                                  fc=c_edge, ec=border_green, lw=1.4)
    ax.add_patch(rect2)
    ax.text(38, 43, "2. Edge Processing &\nContext Encoder", weight='bold', ha='center', va='center', color='#145A32', fontsize=8.5)
    
    # Removed Local Vector RAG from Column 2; added Feature Normalization
    edge_items = [
        "• Sliding-window FFT",
        "• Statistical Profiling",
        "• ISO Severity Filter",
        "• Semantic Prompt Gen",
        "• Feature Normalization",
        "• Token Budget Control"
    ]
    for i, item in enumerate(edge_items):
        ax.text(28.5, 34 - i * 5.2, item, fontsize=7.2, color='#1E8449')

    # 3. Block: Quantized On-Device SLM Engine
    rect3 = patches.FancyBboxPatch((54, 4), 23, 43, boxstyle="round,pad=0.4", 
                                  fc=c_llm, ec=border_yellow, lw=1.4)
    ax.add_patch(rect3)
    ax.text(65.5, 43, "3. Quantized On-Device\nSLM Engine", weight='bold', ha='center', va='center', color='#7D6608', fontsize=8.5)
    
    llm_items = [
        "• Llama-3.2 / Qwen2.5",
        "• 4-Bit GGUF (Q4_K_M)",
        "• AWQ / INT8 PTQ",
        "• Edge FlashAttention",
        "• KV-Cache Allocation",
        "• Direct HW Execution"
    ]
    for i, item in enumerate(llm_items):
        ax.text(55.5, 34 - i * 5.2, item, fontsize=7.2, color='#7D6608')

    # 4. Block: Intelligent Actionable Output (With Local RAG)
    rect4 = patches.FancyBboxPatch((82, 4), 16, 43, boxstyle="round,pad=0.4", 
                                  fc=c_out, ec=border_purple, lw=1.4)
    ax.add_patch(rect4)
    ax.text(90, 43, "4. Local RAG &\nDiagnostic Output", weight='bold', ha='center', va='center', color='#512E5F', fontsize=8.5)
    
    out_items = [
        "• Vector SOP Retrieval",
        "• Root-Cause Diagnosis",
        "• Severity (Crit/Warn)",
        "• Prescribed Actions",
        "• Air-Gapped JSON"
    ]
    for i, item in enumerate(out_items):
        ax.text(83.5, 33 - i * 6.2, item, fontsize=7.2, color='#512E5F')

    # Connecting Arrows
    arrow_props = dict(arrowstyle="->", lw=1.6, color="#34495E")
    ax.annotate("", xy=(27, 25), xytext=(22, 25), arrowprops=arrow_props)
    ax.annotate("", xy=(54, 25), xytext=(49, 25), arrowprops=arrow_props)
    ax.annotate("", xy=(82, 25), xytext=(77, 25), arrowprops=arrow_props)

    plt.tight_layout()
    fig.savefig(os.path.join(FIG_DIR, "fig_architecture.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(FIG_DIR, "fig_architecture.png"), bbox_inches='tight', dpi=300)
    plt.close(fig)
    print("Saved fig_architecture.pdf & .png with aligned Local RAG in Column 4")

if __name__ == "__main__":
    generate_architecture_diagram()
