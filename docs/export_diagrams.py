#!/usr/bin/env python3
"""
Automated Mermaid Diagram Exporter for AI Image Detector Knowledge Base.

Usage:
  bash docs/export_diagrams.sh
  OR
  python3 docs/export_diagrams.py

Requirements:
  - Node.js & npm
  - @mermaid-js/mermaid-cli installed (npm install --save-dev @mermaid-js/mermaid-cli in frontend/)
  - Google Chrome / Chromium installed at /usr/bin/google-chrome
"""

import os
import re
import sys
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
ASSETS_DIR = os.path.join(DOCS_DIR, "assets", "diagrams")
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
MMDC_BIN = os.path.join(FRONTEND_DIR, "node_modules", ".bin", "mmdc")
PUPPETEER_CONFIG = os.path.join(DOCS_DIR, "puppeteerConfig.json")

os.makedirs(ASSETS_DIR, exist_ok=True)

# Ensure Puppeteer configuration uses system Google Chrome
with open(PUPPETEER_CONFIG, "w", encoding="utf-8") as f:
    f.write('{"executablePath": "/usr/bin/google-chrome", "args": ["--no-sandbox", "--disable-setuid-sandbox"]}\n')

# Target mappings: (relative_note_path, mermaid_block_index, output_png_name)
DIAGRAM_TARGETS = [
    ("02 - Architecture/System Architecture.md", 0, "01-system-architecture.png"),
    ("02 - Architecture/Backend Architecture.md", 0, "02-backend-dual-model-serving.png"),
    ("02 - Architecture/Frontend Architecture.md", 0, "03-frontend-sitemap.png"),
    ("02 - Architecture/API Specification.md", 0, "04-single-image-prediction-sequence.png"),
    ("02 - Architecture/API Specification.md", 1, "05-batch-prediction-sequence.png"),
    ("04 - Guidelines & Rules/Security Guidelines.md", 0, "06-file-validation-flow.png"),
    ("03 - Machine Learning/EfficientNet-B0.md", 0, "07-efficientnet-b0-architecture.png"),
    ("03 - Machine Learning/ForensicNet.md", 0, "08-forensicnet-architecture.png"),
    ("02 - Architecture/Model Overview.md", 0, "09-model-selection-decision-flow.png"),
    ("03 - Machine Learning/Training & Fine-Tuning Pipeline.md", 0, "10-training-pipeline.png"),
    ("05 - Decisions & Memory/Known Issues & Resolved Bugs.md", 0, "11-nan-detection-rollback-flow.png"),
]

mermaid_block_re = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)

print("Starting Mermaid Diagram Export...")
print(f"Target Directory: {ASSETS_DIR}\n")

exported_files = []

for note_rel, diagram_idx, out_name in DIAGRAM_TARGETS:
    note_path = os.path.join(DOCS_DIR, note_rel)
    out_png_path = os.path.join(ASSETS_DIR, out_name)

    if not os.path.exists(note_path):
        print(f"[ERROR] Note not found: {note_path}")
        continue

    with open(note_path, "r", encoding="utf-8") as f:
        content = f.read()

    matches = mermaid_block_re.findall(content)
    if diagram_idx >= len(matches):
        print(f"[ERROR] Diagram index {diagram_idx} out of range for {note_rel} (found {len(matches)})")
        continue

    diagram_code = matches[diagram_idx].strip()

    # Write temporary .mmd file
    temp_mmd = os.path.join(ASSETS_DIR, f"temp_{out_name}.mmd")
    with open(temp_mmd, "w", encoding="utf-8") as f:
        f.write(diagram_code + "\n")

    # Command: mmdc -p puppeteerConfig.json -i temp.mmd -o out.png -w 1600 -b white -t neutral
    cmd = [
        MMDC_BIN,
        "-p", PUPPETEER_CONFIG,
        "-i", temp_mmd,
        "-o", out_png_path,
        "-w", "1600",
        "-b", "white",
        "-t", "neutral"
    ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    if os.path.exists(temp_mmd):
        os.remove(temp_mmd)

    if res.returncode == 0 and os.path.exists(out_png_path) and os.path.getsize(out_png_path) > 0:
        size_bytes = os.path.getsize(out_png_path)
        print(f"  ✅ Rendered {out_name:<38} ({size_bytes / 1024.0:6.1f} KB)")
        exported_files.append((out_name, out_png_path, size_bytes))
    else:
        print(f"  ❌ Failed to render {out_name}: {res.stderr}")

print("\n" + "=" * 60)
print(f"Export Complete! Successfully rendered {len(exported_files)}/11 diagrams.")
print("=" * 60)
