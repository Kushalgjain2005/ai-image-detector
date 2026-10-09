#!/usr/bin/env bash
# ==============================================================================
# Automated Mermaid Diagram Exporter Shell Script
# ==============================================================================
# Command to run from project root:
#   bash docs/export_diagrams.sh
#
# Requirements:
#   - Node.js / npm
#   - @mermaid-js/mermaid-cli installed in frontend (npm install --save-dev @mermaid-js/mermaid-cli)
#   - Google Chrome / Chromium installed at /usr/bin/google-chrome
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "=== Exporting Vault Mermaid Diagrams to PNG ==="
python3 "$SCRIPT_DIR/export_diagrams.py"
