---
title: AI Image Detector - Obsidian Knowledge Base Index
tags: [index, moc, overview, ai-image-detector, dual-model, efficientnet, forensicnet]
updated: 2026-08-09
---

# 🧠 AI Image Detector — Neural Forensic Engine Knowledge Base

Welcome to the central Map of Content (MOC) for the **AI Image Detector** (Neural Forensic Engine) project. This Obsidian vault contains the complete technical, architectural, machine learning, and operational documentation for the codebase.

> [!ABSTRACT] Executive Summary
> The **AI Image Detector** is a full-stack, local-first web application engineered to classify digital images as authentic photographs or AI-generated synthetic media (DALL-E, Midjourney, Stable Diffusion). Powered by a dual-model serving architecture, it hosts two production models in memory:
> * **[[EfficientNet-B0]]:** **97.82% Accuracy** | **0.9979 AUC-ROC** | **4.66M Parameters** | **3.78 ms GPU / 12.24 ms CPU Latency**
> * **[[ForensicNet]]:** **94.83% Accuracy** | **0.9903 AUC-ROC** | **1.05M Parameters** (4.4x smaller) | **1.78 ms GPU Latency** (2.1x faster)

---

## 🗺️ Knowledge Base Navigation (Map of Content)

### 📌 01 - Overview & Requirements
* [[PRD|Product Requirements Document (PRD)]] — Core problem statement, target personas, scope, and dual-model feature breakdown.
* [[Product Vision & Goals]] — High-level goals, local-first architecture philosophy, and aesthetic direction.
* [[Success Metrics & Evaluation]] — Detailed breakdown of side-by-side accuracy, AUC-ROC, macro metrics, and latency benchmarks.

### 🏗️ 02 - System Architecture
* [[System Architecture]] — High-level client-server diagram, data flow, and technology stack overview.
* [[Frontend Architecture]] — React 19, Vite, TypeScript, Tailwind CSS v4, and React Router v7 structure.
* [[Backend Architecture]] — FastAPI framework, Uvicorn, custom middleware, rate limiting, and dual-model lifespan serving.
* [[API Specification]] — Detailed REST API endpoints (`GET /health`, `GET /api/v1/models`, `POST /api/v1/predict`, `POST /api/v1/predict/batch`).
* [[Model Overview]] — Dual-model serving strategy, lifespan initialization, and error decorrelation philosophy.
* [[Model Comparison]] — Comprehensive side-by-side performance table, CPU vs GPU latency paradox analysis, and deployment recommendations.

### 🤖 03 - Machine Learning & Data Pipeline
* [[ML Model Architecture]] — Primary ML architecture entry point linking to model specs and comparative diagnostics.
* [[EfficientNet-B0]] — Semantic transfer learning model breakdown, ImageNet backbone, and classifier head `(1280 -> 512 -> 2)`.
* [[ForensicNet]] — Custom tri-stream architecture (Bayar noise + 2D FFT spectrum + RGB) and the NaN crash fix.
* [[Training & Fine-Tuning Pipeline]] — Transfer learning setup, unfreezing strategy (`--unfreeze_at 8`), AMP, and ReduceLROnPlateau.
* [[Dataset Management]] — Kaggle 48k dataset splits (70/15/15), PIL integrity checks, and `merge_datasets.py` utility.
* [[Evaluation & Benchmark Results]] — Confusion matrix, ROC curve analysis, and CPU/GPU speed benchmarks.

### 📐 04 - Guidelines & Development Rules
* [[Development Rules]] — Code style conventions, Multi-Model Consistency Rules, error handling protocols, and anti-patterns.
* [[Design System & Theme]] — Cyberpunk visual aesthetic, theme tokens (`theme.css`), Orbitron & JetBrains Mono typography.
* [[Security Guidelines]] — Magic byte binary validation (`validate_image_magic_bytes`), CORS lockdown, and payload limits.
* [[Testing Strategy]] — Pytest suite, fixtures (`conftest.py`), and test cases in `test_api.py`.

### 📜 05 - History, Memory & Dev Logs
* [[Project Memory & Decision History]] — Architecture Decision Records (ADR-001 through ADR-006).
* [[Decision Log]] — Quick alias link to all Architecture Decision Records.
* [[Model Version History]] — Version history tracking baseline, EfficientNet-B0, ForensicNet crashed run 1, and successful run 2.
* [[Known Issues & Resolved Bugs]] — ForensicNet NaN gradient explosion post-mortem, parameter count hardcoding fix, and open `[VERIFY]` items.
* [[Known Issues]] — Quick alias link to resolved technical bugs.
* **Dev Logs (`docs/05 - Dev Log/`):**
  - [[Building ForensicNet]] — Custom tri-stream architecture design session log.
  - [[Debugging the NaN Crash]] — Numerical instability investigation & FP32/autograd fix session log.
  - [[Dual-Model Serving]] — FastAPI backend & React ModelSelector integration session log.

### 🧩 06 - Component References
* [[Scanner Component]] — Drag-and-drop glassmorphic upload zone & terminal log simulation logic.
* [[Results Component]] — Prediction verdict rendering, confidence meter, and timing telemetry.
* [[ModelSelector Component]] — Interactive model switching control UI.
* [[Background3D Component]] — Interactive Three.js particle canvas background.
* [[Inference Service]] — Singleton PyTorch model manager (`backend/app/services/inference.py`).

---

## ⚡ Quick Start & Commands

> [!TIP] Local Development Launch
> ```bash
> # Start both Backend (FastAPI :8000) and Frontend (Vite :3000)
> python run.py
> 
> # Compare Models Side-by-Side Live
> backend/.venv/bin/python3 backend/ml/compare_models.py
> 
> # Execute Backend Pytest Suite
> pytest backend/tests/
> ```

---

## 🔗 Key Code References
* [[Backend Architecture|FastAPI Main Server Entry]]: `backend/app/main.py`
* [[Inference Service|PyTorch Model Manager]]: `backend/app/services/inference.py`
* [[API Specification|Prediction Route Handler]]: `backend/app/routes/predict.py`
* [[ForensicNet|Custom Model Definition]]: `backend/ml/custom_model.py`
* [[Model Comparison|Model Benchmark Script]]: `backend/ml/compare_models.py`
* [[Scanner Component|Upload Dropzone UI]]: `frontend/src/components/Scanner.tsx`
