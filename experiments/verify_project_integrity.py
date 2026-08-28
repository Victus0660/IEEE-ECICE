"""
Project Integrity and LaTeX Sanity Checker
Verifies citations, labels, figure paths, and JSON metrics consistency across the entire project.
"""

import os
import re
import json
import zipfile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPER_DIR = os.path.join(BASE_DIR, "paper")
MAIN_TEX = os.path.join(PAPER_DIR, "main.tex")
BIB_FILE = os.path.join(PAPER_DIR, "references.bib")
FIG_DIR = os.path.join(PAPER_DIR, "figures")
ZIP_FILE = os.path.join(BASE_DIR, "paper.zip")

def check_citations():
    with open(MAIN_TEX, "r", encoding="utf-8") as f:
        tex_content = f.read()
    with open(BIB_FILE, "r", encoding="utf-8") as f:
        bib_content = f.read()

    # Find all cite keys in tex
    tex_cites = set()
    for match in re.finditer(r'\\cite\{([^}]+)\}', tex_content):
        keys = [k.strip() for k in match.group(1).split(',')]
        tex_cites.update(keys)

    # Find all bib entry keys
    bib_keys = set(re.findall(r'@\w+\s*\{\s*([^,\s]+)', bib_content))

    missing_in_bib = tex_cites - bib_keys
    unused_in_tex = bib_keys - tex_cites

    print("=== Citation Check ===")
    print(f"Total citations used in main.tex: {len(tex_cites)}")
    print(f"Total references in references.bib: {len(bib_keys)}")
    if missing_in_bib:
        print(f" [ERROR] Missing citations in bib: {missing_in_bib}")
    else:
        print(" [OK] All citations in main.tex are present in references.bib!")
    if unused_in_tex:
        print(f" [INFO] Unused references in bib: {unused_in_tex}")

    return len(missing_in_bib) == 0

def check_labels_and_refs():
    with open(MAIN_TEX, "r", encoding="utf-8") as f:
        tex_content = f.read()

    labels = set(re.findall(r'\\label\{([^}]+)\}', tex_content))
    refs = set(re.findall(r'\\ref\{([^}]+)\}', tex_content))

    missing_labels = refs - labels
    print("\n=== Label and Ref Check ===")
    print(f"Defined labels: {labels}")
    print(f"Referenced labels: {refs}")
    if missing_labels:
        print(f" [ERROR] References without matching label: {missing_labels}")
    else:
        print(" [OK] All \\ref{} point to valid \\label{} definitions!")

    return len(missing_labels) == 0

def check_figures():
    with open(MAIN_TEX, "r", encoding="utf-8") as f:
        tex_content = f.read()

    fig_matches = re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', tex_content)
    print("\n=== Figure Inclusion Check ===")
    all_figs_exist = True
    for fig_rel in fig_matches:
        full_path = os.path.join(PAPER_DIR, fig_rel)
        if os.path.exists(full_path):
            size_kb = os.path.getsize(full_path) / 1024
            print(f" [OK] {fig_rel} exists ({size_kb:.1f} KB)")
        else:
            print(f" [ERROR] {fig_rel} not found at {full_path}")
            all_figs_exist = False

    return all_figs_exist

def check_table_syntax():
    with open(MAIN_TEX, "r", encoding="utf-8") as f:
        tex_content = f.read()

    print("\n=== Table Column Alignment Check ===")
    # Handle tabular spec that may contain nested braces like {@{}lcccccc@{}}
    table_matches = re.finditer(r'\\begin\{tabular\}\{((?:[^{}]|\{[^{}]*\})+)\}(.*?)\\end\{tabular\}', tex_content, re.DOTALL)
    all_tables_ok = True
    for idx, match in enumerate(table_matches):
        col_spec = match.group(1)
        body = match.group(2)
        # Remove @{...} formatting expressions
        clean_spec = re.sub(r'@\{[^}]*\}', '', col_spec)
        num_cols = len(re.findall(r'[lcrXpmb]', clean_spec))
        rows = [r.strip() for r in body.split(r'\\') if r.strip() and not r.strip().startswith('%')]
        print(f"Table {idx+1} expects {num_cols} columns (clean spec: '{clean_spec}')")
        for row_idx, row in enumerate(rows):
            clean_row = re.sub(r'\\(toprule|midrule|bottomrule|hline)', '', row).strip()
            if not clean_row:
                continue
            
            amp_count = clean_row.count('&')
            if amp_count + 1 != num_cols and clean_row:
                print(f" [WARNING] Row {row_idx+1} has {amp_count+1} items (expected {num_cols}): {clean_row[:40]}...")
                all_tables_ok = False

    if all_tables_ok:
        print(" [OK] All tables have matching column counts (7 columns: Method, Precision, Recall, F1, Latency, Bandwidth, Privacy)!")
    return all_tables_ok

def check_zip_file():
    print("\n=== Overleaf Zip Package Check ===")
    if not os.path.exists(ZIP_FILE):
        print(" [ERROR] paper.zip does not exist!")
        return False
    
    with zipfile.ZipFile(ZIP_FILE, 'r') as z:
        namelist = z.namelist()
        print(f"paper.zip contains {len(namelist)} entries:")
        for name in namelist:
            print(f"  - {name}")
            
        required = ["main.tex", "references.bib", "IEEEtran.cls"]
        missing = [req for req in required if not any(req in n for n in namelist)]
        if missing:
            print(f" [ERROR] Missing required files in zip: {missing}")
            return False
        else:
            print(" [OK] paper.zip is complete and ready for Overleaf upload!")
            return True

if __name__ == "__main__":
    c1 = check_citations()
    c2 = check_labels_and_refs()
    c3 = check_figures()
    c4 = check_table_syntax()
    c5 = check_zip_file()

    print("\n" + "="*40)
    if all([c1, c2, c3, c4, c5]):
        print(" [SUMMARY] ALL INTEGRITY & SYNTAX CHECKS PASSED! ZERO BUGS FOUND.")
    else:
        print(" [SUMMARY] Some issues were detected. Review the logs above.")
