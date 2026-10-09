---
title: Dev Log — Dual-Model Serving
tags: [dev-log, dual-model, fastapi, react, model-selector, backend, frontend]
date: 2026-08-08
author: Engineering Team
---

# 📝 Dev Log: Dual-Model Serving & Model Selector Integration

> [!INFO] Session Context
> * **Objective:** Implement dual-model serving infrastructure in FastAPI backend and build an interactive model selector UI in React frontend.
> * **Related Notes:** [[Model Overview]], [[Model Comparison]], [[Backend Architecture]], [[API Specification]], [[Known Issues & Resolved Bugs]]

---

## 🛠️ What Was Done

1. **Backend Dual-Model Infrastructure (`backend/app/services/inference.py` & `predict.py`):**
   - Refactored `inference.py` to initialize both `EfficientNet-B0` and `ForensicNet` as singleton model instances on startup.
   - Built dynamic live parameter counter (`get_model_param_count()`) using `sum(p.numel() for p in model.parameters())` and string formatter `format_params_count()`.
   - Created `GET /api/v1/models` endpoint returning metadata, test accuracy, AUC-ROC, live parameters, and load status.
   - Updated `POST /api/v1/predict` and `POST /api/v1/predict/batch` to parse optional `model` parameter (`"efficientnet"` or `"forensicnet"`).

2. **Frontend Model Selector Component (`frontend/src/`):**
   - Created `ModelSelector.tsx` component providing interactive pill buttons for selecting between EfficientNet-B0 and ForensicNet.
   - Integrated `ModelSelector` into `Detector.tsx` page.
   - Updated `frontend/src/services/api.ts` to pass the selected model identifier to prediction API calls.

3. **Comparison Script & Benchmarking (`backend/ml/compare_models.py`):**
   - Created `compare_models.py` to load evaluation JSON files, compute parameters live, print side-by-side comparison tables, and determine metric winners.
   - Identified CPU latency bottleneck on ForensicNet (85.76 ms CPU vs 1.78 ms GPU due to FFT computation overhead).

---

## 💡 Decisions Made

- **Decision 1:** Retain both models in production serving rather than discarding ForensicNet (ADR-006: Dual-Model Serving & Error Decorrelation Strategy).
- **Decision 2:** Compute all parameter counts live from PyTorch model instances (`sum(p.numel() for p in model.parameters())`) to eliminate parameter mismatch bugs.
- **Decision 3:** Default predictions to EfficientNet-B0 while allowing seamless switching to ForensicNet via UI toggle or API parameter.

---

## ⚠️ Issues Encountered

- **Issue:** Parameter count discrepancy identified where startup logs reported `1.05M params` while API routes or docs returned static hardcoded strings.
- **Resolution:** Replaced all hardcoded parameter strings with `get_model_param_count()` and `format_params_count()` in `inference.py` and `compare_models.py` (see [[Known Issues & Resolved Bugs]]).

---

## 🚀 Next Steps

- Perform full audit of vault documentation and refresh all notes.
