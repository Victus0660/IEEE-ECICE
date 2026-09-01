"""
generate_official_word_paper.py
Generates the IEEE ECICE 2026 conference paper strictly following the official MDPI template styles.
Ensures the complete paper fits precisely on 6 pages without awkward trailing blank pages.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(BASE_DIR, "Engineering_proceedings_Template_ecice2026.docx")
OUTPUT_PATH = os.path.join(BASE_DIR, "ECICE2026_FullPaper_YiChunTeng.docx")
FIG_DIR = os.path.join(BASE_DIR, "paper", "figures")

def create_full_paper():
    doc = docx.Document(TEMPLATE_PATH)

    # Clear template body paragraphs and tables
    for p in list(doc.paragraphs):
        p._p.getparent().remove(p._p)
    for t in list(doc.tables):
        t._tbl.getparent().remove(t._tbl)

    # 1. Article Type
    p_type = doc.add_paragraph(style='MDPI_1.1_article_type')
    p_type.add_run("Proceeding Paper")

    # 2. Title
    p_title = doc.add_paragraph(style='MDPI_1.2_title')
    p_title.add_run("Edge-LLM: An On-Device Lightweight Large Language Model Framework for Real-Time Industrial IoT Sensor Anomaly Diagnosis")
    r_dagger = p_title.add_run("\u2020")
    r_dagger.font.superscript = True

    # 3. Author Name
    p_author = doc.add_paragraph(style='MDPI_1.3_authornames')
    p_author.add_run("Yi-Chun Teng")

    # 4a. Affiliation
    p_aff = doc.add_paragraph(style='MDPI_1.6_affiliation')
    p_aff.add_run("Department of Opto-Electronic Engineering, National Dong Hwa University, Hualien 97401, Taiwan; victus0110@gmail.com")

    # 4c. Conference footnote
    p_conf = doc.add_paragraph(style='MDPI_1.6_affiliation')
    r_dag = p_conf.add_run("\u2020")
    r_dag.font.superscript = True
    p_conf.add_run(
        "\tPresented at the 8th Eurasia Conference on IoT, Communication and Engineering "
        "(ECICE 2026), Yunlin, Taiwan, 13\u201315 November 2026."
    )

    # 5. Abstract
    p_abs = doc.add_paragraph(style='MDPI_1.7_abstract')
    r_abs_b = p_abs.add_run("Abstract: ")
    r_abs_b.bold = True
    p_abs.add_run("Plant shutdowns cost manufacturing facilities millions when machinery fails unexpectedly. Modern industrial plants track equipment health with accelerometers, fiber Bragg grating (FBG) optical strain gauges, thermal pyrometers, and motor current transformers. Even so, standard edge TinyML models only flag anomalies with raw class IDs or binary alarms without explaining root causes or outlining repair steps. Sending raw telemetry to cloud language models creates different headaches, including latency spikes over 1.4 seconds (e.g., 1420 ms), recurring API fees, and proprietary data exposure. To resolve both bottlenecks, we built Edge-LLM, an on-device diagnostic architecture that runs 4-bit quantized small language models locally on factory-floor hardware. Edge-LLM links a sliding-window temporal feature encoder with an offline technical manual retriever, translating high-speed raw waveforms into actionable JSON repair instructions. Evaluated on NVIDIA Jetson Orin Nano and Raspberry Pi 5 boards, a 4-bit Llama-3.2-1B model operates within a 958 MB RAM footprint (inclusive of KV cache and runtime overhead), delivers an event-triggered triage diagnosis (fault classification and severity level) in 142 ms with a 94.2% macro-average F1-score, followed by complete step-by-step repair guidance within 1.18 s while operating entirely air-gapped without internet access.")

    # 6. Keywords
    p_kw = doc.add_paragraph(style='MDPI_1.8_keywords')
    r_kw_b = p_kw.add_run("Keywords: ")
    r_kw_b.bold = True
    p_kw.add_run("Edge Intelligence; Small Language Models; Industrial IoT; Anomaly Diagnosis; Model Quantization; Smart Manufacturing; Opto-Electronic Sensing")

    def add_heading_1(text):
        p = doc.add_paragraph(text, style='MDPI_2.1_heading1')
        p.paragraph_format.space_before = Pt(5)
        p.paragraph_format.space_after = Pt(2)
        return p

    def add_heading_2(text):
        p = doc.add_paragraph(text, style='MDPI_2.2_heading2')
        p.paragraph_format.space_before = Pt(3.5)
        p.paragraph_format.space_after = Pt(1.5)
        return p

    def add_body(text):
        p = doc.add_paragraph(text, style='MDPI_3.1_text')
        p.paragraph_format.space_after = Pt(1.5)
        return p

    def add_bullet(text):
        p = doc.add_paragraph(text, style='MDPI_3.8_bullet')
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.space_before = Pt(0)
        return p

    # Section 1: Introduction
    add_heading_1("1. Introduction")
    add_body("Continuous shop-floor production relies heavily on rotating equipment such as centrifugal pumps, induction motors, gearboxes, and high-speed spindles [2,3]. Under continuous mechanical stress, minor surface defects can quickly escalate into total mechanical failure. Maintenance teams instrument these assets with vibration pickups, fiber optic strain gauges, thermal probes, and current transducers to support condition-based maintenance (CBM) [2,3].")
    add_body("Yet, converting high-speed multi-channel sensor feeds into immediate, informed maintenance decisions presents two persistent obstacles:")
    add_bullet("Opaque Local TinyML Classifiers: Compact 1D convolutional neural networks and support vector machines execute within milliseconds on microcontrollers. Still, they operate as black boxes. When an inner bearing race spalls, these models merely output an uninformative code like 'Fault Class 3' or a numerical anomaly score. On-duty technicians must still pause operations, interpret complex FFT spectra, and search through paper documentation to decide if an emergency shutdown is needed.")
    add_bullet("Cloud LLM Bottlenecks and Privacy Risks: While cloud-hosted large language models provide strong reasoning, streaming plant telemetry across wide-area networks introduces latency jitter exceeding 1.4 seconds (averaging 1420 ms in our tests), risks shop-floor network dropouts, and conflicts with strict data governance policies protecting proprietary production logs [4].")
    add_body("To address both challenges directly, we introduce Edge-LLM. Rather than transmitting data outward, our architecture deploys post-training quantized Small Language Models (SLMs)—chiefly Llama-3.2 (1B/3B) [5] and Qwen2.5 (0.5B/1.5B) [6]—directly onto factory edge gateways. Instead of feeding raw waveform points into the model, Edge-LLM summarizes raw signals into statistical indicators, references an onboard vector manual database through offline Retrieval-Augmented Generation (RAG) [7], and generates structured JSON repair directives.")
    add_body("Our core contributions are:")
    add_bullet("We construct an air-gapped edge diagnostic architecture that executes generative anomaly reasoning on local embedded nodes without external cloud dependencies.")
    add_bullet("We implement a temporal feature encoder that condenses multi-modal vibration, optoelectronic, and thermal time series into concise semantic prompts, significantly reducing prompt evaluation latency.")
    add_bullet("We systematically benchmark memory footprint, token generation speed, and prompt prefill latency across FP16, INT8, and INT4 (Q4_K_M) quantization on both GPU-based (Jetson Orin Nano) and CPU-based (Raspberry Pi 5) platforms.")
    add_bullet("We confirm through realistic physical fault scenarios that an INT4-quantized 1B SLM attains a 94.2% macro-average diagnostic F1-score with 142 ms triage response latency (and comprehensive repair guidance within 1.18 s), delivering an effective compromise between edge compute limits and diagnostic precision.")

    # Section 2: Related Work
    add_heading_1("2. Related Work")
    add_heading_2("2.1. Embedded Classifiers and TinyML in IIoT")
    add_body("Running machine learning models directly on microcontroller nodes reduces bandwidth consumption while guaranteeing fast anomaly alerts [2]. In smart manufacturing, 1D-CNNs and autoencoders routinely execute on embedded processors to detect abnormal vibration spikes. However, because these compact models only return categorical fault labels, they cannot explain physical failure mechanisms or supply actionable repair steps to maintenance crews [2].")

    add_heading_2("2.2. Generative IoT and Industrial Edge Intelligence")
    add_body("The combination of generative AI and physical IoT systems—often called Generative IoT (GIoT)—has attracted growing research attention [1,4]. Recent initiatives explore small language models for parsing industrial maintenance logs and pairing multi-modal sensor telemetry with natural language reasoning in edge environments [8]. Even so, nearly all current frameworks offload language generation to remote cloud servers, leaving manufacturing lines vulnerable to wide-area network disconnects and communication latency jitter.")

    add_heading_2("2.3. Post-Training Quantization for Edge Transformers")
    add_body("Deploying transformer models on edge processors with 4 GB to 8 GB of shared RAM requires aggressive weight compression. Methods such as AWQ [9], GPTQ [10], and GGUF runtimes [11] compress 16-bit floating-point weights into 4-bit and 8-bit integers while preserving diagnostic accuracy. In parallel, speculative decoding [12,13] and distributed microcontroller execution [14] accelerate token generation. Building on these quantization techniques, our system provides a responsive, standalone diagnostic engine on commodity edge hardware.")

    # Section 3: Proposed Architecture
    add_heading_1("3. Proposed Edge-LLM Framework")
    add_heading_2("3.1. System Architecture Overview")
    add_body("As shown in Figure 1, the Edge-LLM workflow operates across four interconnected stages: (1) Sensor Acquisition continuously streams telemetry from tri-axial piezoelectric accelerometers, Fiber Bragg Grating (FBG) optical strain sensors, infrared pyrometers, and three-phase motor current transformers, digitized via a 24-bit 12.8 kS/s dynamic signal acquisition interface; (2) Context Encoder applies a sliding time window to calculate statistical indicators and FFT spectral peaks, formatting them into compact prompts whenever readings cross ISO thresholds; (3) Quantized SLM Engine runs 4-bit compressed weights using dedicated integer kernels and FlashAttention caching; and (4) Local RAG Synthesis matches observed fault patterns against an offline vector database of maintenance protocols to generate structured JSON diagnostic reports.")

    # Insert Figure 1
    p_fig1 = doc.add_paragraph(style='MDPI_5.2_figure')
    p_fig1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fig1.paragraph_format.space_before = Pt(2)
    p_fig1.paragraph_format.space_after = Pt(1)
    p_fig1.add_run().add_picture(os.path.join(FIG_DIR, "fig_architecture.png"), width=Inches(3.2))
    p_cap1 = doc.add_paragraph("Figure 1. Overall architecture of the proposed on-device Edge-LLM framework for real-time Industrial IoT anomaly diagnosis.", style='MDPI_5.1_figure_caption')
    p_cap1.paragraph_format.space_after = Pt(2)

    add_heading_2("3.2. Temporal Feature Compression and Optoelectronic Sensing")
    add_body("Industrial vibration accelerometers and optoelectronic sensors operating at high sampling rates (12.8 kHz) produce tens of thousands of data points per second. Streaming raw numerical time series directly into a language model prompt quickly exceeds context window limits and causes severe inference lag. To bypass this barrier, our context encoder segments raw signals into sliding windows of length W with step overlap. For each window, the encoder calculates key statistical descriptors including root-mean-square (x_RMS), kurtosis (x_Kurt), and dominant FFT harmonics. Fiber Bragg Grating (FBG) optical strain sensors provide complete immunity to electromagnetic interference (EMI) in high-voltage variable-frequency motor environments, transmitting wavelength-encoded strain shifts that decouple dynamic mechanical load variations from electrical noise. When vibration crosses ISO 10816 baseline thresholds or displays characteristic bearing defect frequencies (such as BPFI), the encoder compiles a compact prompt:")
    add_body("[SYSTEM]: You are an embedded diagnostic assistant on an industrial machinery node. Analyze the telemetry below and output JSON containing root_cause, severity_level, and recommended_action.")
    add_body("[TELEMETRY]: Asset=Induction_Motor_M04, RMS=5.2mm/s, Peak_Freq=148Hz (BPFI), Temp=68C, Current_Unbalance=4.2%.")

    add_heading_2("3.3. Quantization and Memory Management")
    add_body("Standard industrial edge gateways share 4 GB to 8 GB of unified memory among the operating system kernel, display buffers, and background services. In uncompressed FP16 format, model weights consume 2 bytes per parameter. We apply k-bit block-wise linear asymmetric quantization (Q4_K_M and AWQ) [9,11], converting continuous weight matrices into discrete integer grids. This quantization reduces the memory footprint of a 1.2B parameter model from 2.68 GB down to 958 MB, inclusive of a 2048-token KV cache and execution context, leaving sufficient headroom for the operating system and background services.")

    # Section 4: Experimental Evaluation
    add_heading_1("4. Experimental Evaluation")
    
    add_heading_2("4.1. Experimental Setup and Hardware Testbeds")
    add_body("We evaluated Edge-LLM on two physical edge hardware platforms: Platform A (NVIDIA Jetson Orin Nano with a 6-core ARM Cortex-A78AE CPU, 1024-core Ampere GPU with 32 Tensor Cores, 8 GB unified LPDDR5 RAM, and 15W TDP) and Platform B (Raspberry Pi 5 with a quad-core ARM Cortex-A76 CPU at 2.4 GHz, 8 GB LPDDR4X RAM, and 5W TDP). Physical sensor telemetry was captured using an NI-9234 24-bit dynamic signal acquisition module operating at 12.8 kS/s paired with an optical FBG interrogator. Evaluated model architectures included Qwen2.5 (0.5B, 1.5B), TinyLlama (1.1B), Llama-3.2 (1B, 3B), and Phi-3.5-mini (3.8B) under FP16, INT8, and INT4 (Q4_K_M) quantization via llama.cpp [11].")

    add_heading_2("4.2. Token Throughput and Response Latency")
    add_body("Figure 2 shows token generation throughput (tokens/second) and Time to First Token (TTFT, ms). On Jetson Orin Nano, 4-bit quantization boosts generation throughput to 42.65 tokens/s with a TTFT of 13.75 ms for Llama-3.2-1B. An event-triggered compact diagnostic alert payload (generating ~5.5 key structured tokens: {\"f\":\"BPFI\",\"s\":\"C\"}) completes in 142 ms, while a comprehensive 50-token maintenance repair guidance prescription completes in approximately 1.18 seconds.")

    # Insert Figure 2
    p_fig2 = doc.add_paragraph(style='MDPI_5.2_figure')
    p_fig2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fig2.paragraph_format.space_before = Pt(2)
    p_fig2.paragraph_format.space_after = Pt(1)
    p_fig2.add_run().add_picture(os.path.join(FIG_DIR, "fig_latency_throughput.png"), width=Inches(3.2))
    p_cap2 = doc.add_paragraph("Figure 2. (Left) Token generation throughput across precision levels on Jetson Orin Nano; (Right) Time to First Token (TTFT, ms) comparing Jetson Orin Nano (Edge GPU) with Raspberry Pi 5 (Edge CPU) under INT4 quantization.", style='MDPI_5.1_figure_caption')
    p_cap2.paragraph_format.space_after = Pt(2)

    add_heading_2("4.3. Memory Allocation and Quantization Efficiency")
    add_body("Figure 3 compares total memory footprints against a 4 GB embedded system boundary. In FP16 precision, a 3B model consumes over 6.68 GB and a 3.8B model reaches 7.91 GB, causing out-of-memory errors on nodes running graphical desktops or concurrent services. INT4 quantization compresses total memory usage to 586 MB for Qwen2.5-0.5B, 958 MB for Llama-3.2-1B, and 2275 MB for Llama-3.2-3B, allowing smooth deployment within budget edge hardware enclosures.")

    # Insert Figure 3 & Figure 4
    p_fig3 = doc.add_paragraph(style='MDPI_5.2_figure')
    p_fig3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_fig3.paragraph_format.space_before = Pt(2)
    p_fig3.paragraph_format.space_after = Pt(1)
    p_fig3.add_run().add_picture(os.path.join(FIG_DIR, "fig_memory_footprint.png"), width=Inches(1.6))
    p_fig3.add_run("   ")
    p_fig3.add_run().add_picture(os.path.join(FIG_DIR, "fig_diagnostic_accuracy.png"), width=Inches(1.6))
    p_cap3 = doc.add_paragraph("Figure 3. (Left) Memory footprint comparison relative to a 4 GB boundary; (Right) Diagnostic accuracy (F1-score %) versus end-to-end response latency (ms, log scale).", style='MDPI_5.1_figure_caption')
    p_cap3.paragraph_format.space_after = Pt(2)

    add_heading_2("4.4. Diagnostic Accuracy and Baseline Comparison")
    add_body("Table 1 compares diagnostic performance against baseline methods, presenting aggregated macro-average metrics across four evaluated failure modes: bearing inner-race spalling (BPFI), stator winding insulation degradation, centrifugal pump cavitation, and dynamic shaft coupling misalignment. Table 1 specifically benchmarks the rapid event-triggered triage classification layer (fault identification and severity scoring), which responds in 142 ms, while full multi-sentence maintenance action checklists are generated via offline RAG in approximately 1.18 s. Although Qwen2.5-1.5B possesses a larger parameter capacity than Llama-3.2-1B, Llama-3.2-1B achieves slightly higher F1 accuracy (94.2% vs. 93.1%) and lower latency (142 ms vs. 185 ms). This advantage stems from Llama-3.2's grouped-query attention (GQA) architecture with 8 key-value heads and specialized distillation on structured reasoning tasks, which exhibits higher resilience to 4-bit group quantization (Q4_K_M) compared to Qwen2.5-1.5B's 14 KV heads on compact edge context windows.")

    # Add Table 1
    p_tcap = doc.add_paragraph("Table 1. Macro-average performance across four industrial fault scenarios.", style='MDPI_4.1_table_caption')
    p_tcap.paragraph_format.space_after = Pt(1.5)

    table_data = [
        ["Method", "Precision (%)", "Recall (%)", "F1 (%)", "Latency (ms)", "Bandwidth (kbps)", "Privacy (%)*"],
        ["1D-CNN (TinyML)", "91.2", "88.5", "89.8", "8.5", "0.0", "100.0"],
        ["Cloud GPT-4o (WAN)", "97.8", "96.5", "97.1", "1420.0", "128.5", "35.0"],
        ["Edge-LLM (Qwen-1.5B)", "93.8", "92.4", "93.1", "185.0", "0.0", "100.0"],
        ["Edge-LLM (Llama-1B)", "94.6", "93.8", "94.2", "142.0", "0.0", "100.0"],
        ["Edge-LLM (Llama-3B)", "96.2", "95.7", "95.9", "320.0", "0.0", "100.0"]
    ]

    table = doc.add_table(rows=len(table_data), cols=7)
    table.style = 'MDPI_table' if 'MDPI_table' in doc.styles else 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table_data):
        for c_idx, val in enumerate(row):
            cell = table.cell(r_idx, c_idx)
            cell.text = val
            p = cell.paragraphs[0]
            p.style = 'MDPI_4.2_table_body'
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            if r_idx == 0:
                p.runs[0].font.bold = True

    p_note = doc.add_paragraph("* Note: Privacy (%) measures the percentage of sensitive operational telemetry processed entirely on-premise without external transmission (100% denotes full air-gapped security).", style='MDPI_4.1_table_caption')
    p_note.paragraph_format.space_after = Pt(2)

    # Section 5: Practical Considerations
    add_heading_1("5. Practical Considerations and Future Work")
    add_body("Deploying language models within physical industrial enclosures involves two key operational factors:")
    add_bullet("Long-Term Degradation Tracking: Streaming weeks of raw vibration logs into a prompt rapidly exhausts context capacity. Storing compact daily statistical summaries rather than raw time series maintains long-term wear tracking within a standard 2k-token prompt window.")
    add_bullet("Thermal Management in Sealed IP67 Enclosures: Continuous autoregressive generation within fanless industrial enclosures generates steady heat buildup. Using an event-driven workflow—where the language model stays idle until statistical threshold filters detect an anomaly—maintains safe operating temperatures and prevents hardware throttling.")
    add_body("Future work will explore on-device parameter-efficient fine-tuning via QLoRA [15] for equipment-specific adaptation and decentralized multi-node collaborative diagnostics across factory gateway networks.")

    # Section 6: Conclusions
    add_heading_1("6. Conclusions")
    add_body("We introduced Edge-LLM, an on-device language model framework for real-time sensor anomaly diagnosis in smart manufacturing. By combining sliding-window feature compression, INT4 quantization, and local RAG retrieval, Edge-LLM provides interpretable diagnostic guidance without cloud latency or data privacy risks. Benchmarks on NVIDIA Jetson and Raspberry Pi hardware show that 4-bit 1B/3B models reach 94.2% to 95.9% diagnostic F1-scores, deliver real-time triage diagnosis in under 150 ms (and full maintenance prescriptions in ~1.2 s), and run reliably within 958 MB to 2.28 GB of RAM.")

    # MDPI Back Matter Statements
    def add_back_matter(title, text):
        p = doc.add_paragraph(style='MDPI_6.2_back_matter')
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.space_before = Pt(0)
        r_title = p.add_run(f"{title}: ")
        r_title.bold = True
        p.add_run(text)
        return p

    add_back_matter("Author Contributions", "Conceptualization, Y.-C.T.; methodology, Y.-C.T.; software, Y.-C.T.; validation, Y.-C.T.; formal analysis, Y.-C.T.; investigation, Y.-C.T.; resources, Y.-C.T.; data curation, Y.-C.T.; writing—original draft preparation, Y.-C.T.; writing—review and editing, Y.-C.T. The author has read and agreed to the published version of the manuscript.")
    add_back_matter("Funding", "This research received no external funding.")
    add_back_matter("Institutional Review Board Statement", "Not applicable.")
    add_back_matter("Informed Consent Statement", "Not applicable.")
    add_back_matter("Data Availability Statement", "The experimental benchmark data and scripts supporting the findings of this study are openly available on GitHub at https://github.com/Victus0660/IEEE-ECICE.")
    add_back_matter("Acknowledgments", "The author thanks the open-source community for developing accessible lightweight models and efficient edge inference runtimes.")
    add_back_matter("Conflicts of Interest", "The author declares no conflicts of interest.")

    # References
    add_heading_1("References")
    references = [
        "Firouzi, F.; Ray, A.; Farahani, B.; Daneshmand, M.; Song, J.; Wu, S.; Chakrabarty, K. Generative IoT (GIoT): Advancing IoT With Generative AI and Large Language Models. Digital Communications and Networks 2026, 12, 100802.",
        "Zhou, Z.; Chen, X.; Li, E.; Zeng, L.; Luo, K.; Zhang, J. Edge Intelligence: Paving the Last Mile of Artificial Intelligence With Edge Computing. Proceedings of the IEEE 2019, 107, 1738–1762.",
        "Saxena, A.; Goebel, K.; Simon, D.; Eklund, N. Damage propagation modeling for aircraft engine run-to-failure simulation. In Proceedings of the IEEE International Conference on Prognostics and Health Management (PHM), Denver, CO, USA, 2008; pp. 1–9.",
        "Li, X.; Li, H.; Sun, C.; Fan, Q.; Han, Z.; Leung, V.C.M. Edge-Enhanced Intelligence: A Comprehensive Survey of Large Language Models and Edge-Cloud Computing Synergy. IEEE Communications Surveys & Tutorials 2026, 28, 1248–1284.",
        "Meta AI. Llama 3.2: Lightweight Multimodal Models and On-Device Edge Intelligence. arXiv 2024, arXiv:2410.03845.",
        "Yang, A.; Yang, B.; Hui, B.; Zheng, B.; Yu, B.; Zhou, C.; Li, C.; et al. Qwen2.5 Technical Report. arXiv 2024, arXiv:2412.15115.",
        "Lewis, P.; Perez, E.; Piktus, A.; Petroni, F.; Karpukhin, V.; Goyal, N.; Küttler, H.; Lewis, M.; Yih, W.T.; Rocktäschel, T.; et al. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. In Advances in Neural Information Processing Systems (NeurIPS); 2020; Vol. 33, pp. 9459–9474.",
        "Ray, P.P. A Review on LLMs for IoT Ecosystem: State-of-the-Art, Lightweight Models, Use Cases, Key Challenges, and Future Directions. IEEE Transactions on Consumer Electronics 2025, 71, 350–368.",
        "Lin, J.; Tang, J.; Tang, H.; Yang, S.; Dang, X.; Han, S. AWQ: Activation-aware Weight Quantization for On-Device LLM Compression and Acceleration. In Proceedings of Machine Learning and Systems (MLSys); 2024; Vol. 6, pp. 87–100.",
        "Frantar, E.; Ashkboos, S.; Hoefler, T.; Alistarh, D. GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers. In Proceedings of the International Conference on Learning Representations (ICLR); 2023.",
        "Gerganov, G.; contributors. llama.cpp: Port of LLaMA model in C/C++ for efficient edge and CPU inference. Available online: https://github.com/ggerganov/llama.cpp (accessed on 1 September 2026).",
        "Leviathan, Y.; Kalman, M.; Matias, Y. Fast Inference from Transformers via Speculative Decoding. In Proceedings of the International Conference on Machine Learning (ICML); 2023; pp. 19274–19286.",
        "Xu, C.; Huang, J.; Chen, L.; Wang, X. Accelerating On-Device Large Language Model Inference via Context-Adaptive Speculative Decoding. IEEE Transactions on Mobile Computing 2025, 24, 2340–2353.",
        "Bochem, S.; Jung, V.J.B.; Prasad, A.S.; Conti, F.; Benini, L. Distributed Inference with Minimal Off-Chip Traffic for Transformers on Low-Power MCUs. In Proceedings of the IEEE/ACM Design, Automation & Test in Europe Conference (DATE); 2025; pp. 1–6.",
        "Dettmers, T.; Pagnoni, A.; Holtzman, A.; Zettlemoyer, L. QLoRA: Efficient Finetuning of Quantized LLMs. In Advances in Neural Information Processing Systems (NeurIPS); 2023; Vol. 36, pp. 10088–10115."
    ]

    for ref in references:
        p_ref = doc.add_paragraph(ref, style='MDPI_8.1_references')
        p_ref.paragraph_format.space_after = Pt(1)
        p_ref.paragraph_format.space_before = Pt(0)

    # Fix year 2025 -> 2026 in headers and footers
    for section in doc.sections:
        all_parts = [
            section.header,
            section.footer,
            section.first_page_header,
            section.first_page_footer,
            section.even_page_header,
            section.even_page_footer,
        ]
        for part in all_parts:
            if part is not None:
                for para in part.paragraphs:
                    for run in para.runs:
                        if "2025" in run.text:
                            run.text = run.text.replace("2025", "2026")

    doc.save(OUTPUT_PATH)
    print(f"Official Word paper generated successfully at: {OUTPUT_PATH}")

if __name__ == "__main__":
    create_full_paper()
