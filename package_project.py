#!/usr/bin/env python3
"""
Project Packaging Script for AI Image Detector.
Creates a clean, production-ready ZIP archive of the project codebase and documentation,
excluding dataset files, virtual environments, node_modules, build artifacts, and cache directories.
Overwrites any pre-existing ZIP file of the same name.
"""

import os
import sys
import zipfile
from pathlib import Path

# Target output zip name
OUTPUT_ZIP_NAME = "ai-image-detector.zip"

# Project root directory
PROJECT_ROOT = Path(__file__).parent.resolve()
OUTPUT_ZIP_PATH = PROJECT_ROOT / OUTPUT_ZIP_NAME

# Directories to completely exclude
EXCLUDE_DIR_NAMES = {
    "node_modules",
    "venv",
    ".venv",
    "env",
    "dist",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".git",
    ".vscode",
    ".idea",
    "data",  # Large local datasets directory
    ".vite",
    ".gemini",
}

# Specific patterns / file extensions to exclude
EXCLUDE_EXTENSIONS = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".zip",
    ".tar",
    ".gz",
    ".7z",
    ".log",
    ".DS_Store",
}

# Exclude specific files by exact name
EXCLUDE_FILE_NAMES = {
    OUTPUT_ZIP_NAME,
    "Thumbs.db",
    ".DS_Store",
}


def should_exclude_path(path: Path) -> bool:
    """Check if a file or directory path should be excluded from the zip archive."""
    rel_path = path.relative_to(PROJECT_ROOT)
    parts = rel_path.parts

    # Check directory components
    for part in parts:
        if part in EXCLUDE_DIR_NAMES:
            return True

    # Check file name and extension
    if path.is_file():
        if path.name in EXCLUDE_FILE_NAMES:
            return True
        if path.suffix.lower() in EXCLUDE_EXTENSIONS:
            return True

    return False


def create_project_zip():
    print(f"📦 Starting packaging for AI Image Detector...")
    print(f"📍 Root Directory: {PROJECT_ROOT}")
    print(f"🎯 Output File:    {OUTPUT_ZIP_PATH}")

    # Remove existing zip if present
    if OUTPUT_ZIP_PATH.exists():
        print(f"🗑️  Existing archive found. Replacing {OUTPUT_ZIP_NAME}...")
        OUTPUT_ZIP_PATH.unlink()

    included_count = 0
    total_bytes = 0

    with zipfile.ZipFile(OUTPUT_ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Prune excluded directories in-place so os.walk does not recurse into them
            dirs[:] = [d for d in dirs if not should_exclude_path(Path(root) / d)]

            for file_name in files:
                file_path = Path(root) / file_name
                if should_exclude_path(file_path):
                    continue

                rel_archive_path = file_path.relative_to(PROJECT_ROOT)
                zipf.write(file_path, arcname=str(rel_archive_path))
                included_count += 1
                total_bytes += file_path.stat().st_size

    archive_size_mb = OUTPUT_ZIP_PATH.stat().st_size / (1024 * 1024)
    raw_size_mb = total_bytes / (1024 * 1024)

    print("\n✅ Packaging complete!")
    print(f"📄 Total Files Included: {included_count}")
    print(f"💾 Uncompressed Size:    {raw_size_mb:.2f} MB")
    print(f"🗜️  Compressed ZIP Size:  {archive_size_mb:.2f} MB")
    print(f"✨ Output generated at:   {OUTPUT_ZIP_PATH}")


if __name__ == "__main__":
    create_project_zip()
