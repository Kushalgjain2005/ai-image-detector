---
title: Dev Log — Debugging the NaN Crash
tags: [dev-log, bug-fix, nan-crash, forensicnet, amp, pytorch, gradient-explosion]
date: 2026-08-08
author: Engineering Team
---

# 📝 Dev Log: Debugging the ForensicNet NaN Gradient Explosion

> [!INFO] Session Context
> * **Objective:** Investigate, diagnose, and resolve the training crash during ForensicNet Run 1 where loss turned to `NaN` at Epoch 4.
> * **Related Notes:** [[ForensicNet]], [[Known Issues & Resolved Bugs]], [[Model Version History]], [[Development Rules]]

---

## 🛠️ What Was Done

1. **Root Cause Diagnosis & Audit:**
   - Evaluated training log `training_log_forensicnet.json` (Epochs 1–3 trained clean, Epoch 4 crashed with `NaN` loss).
   - Inspected autograd graph and forward pass calculations across `custom_model.py`.
   - Identified three compound triggers:
     1. **FP16 Underflow in FFT Spectrum Normalization:** Under Automatic Mixed Precision (`torch.cuda.amp.autocast`), `(shifted_spectrum - amin) / (amax - amin + 1e-6)` performed in FP16 caused division by near-zero numbers when `amax - amin` fell below half-precision limits.
     2. **In-Place Weight Mutation:** `BayarConv2d.constrain_weights()` mutated `self.conv.weight.data` in-place, corrupting PyTorch autograd graph tracking and `GradScaler` scaling.
     3. **Unclipped Multi-Stream Gradients:** Gradients accumulating across three parallel streams triggered gradient explosion.

2. **Implementation of Fixes:**
   - **FP32 Forced Execution Block:** Wrapped `compute_fft_spectrum()` in `with torch.autocast(device_type=device_type, enabled=False):` with float conversion and explicit clamping.
   - **Non-In-Place Weight Masking:** Rewrote `BayarConv2d.constrain_weights()` to construct a new functional weight tensor non-in-place.
   - **Gradient Norm Clipping:** Added `torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)`.
   - **Learning Rate Tuning & Rollback:** Reduced base LR from `1e-3` to `5e-4` (CosineAnnealingLR) and added automated `NaN` detection with state rollback.

3. **Verification & Re-Run:**
   - Ran a 3-epoch smoke test verifying stable, non-zero, non-NaN losses.
   - Launched full 40-epoch training run (`best_forensicnet.pth`), achieving **96.16% Peak Val Accuracy** (Epoch 33) and **94.83% Test Accuracy**.

---

## 💡 Decisions Made

- **Decision 1:** Force FP32 precision strictly for the FFT spectral calculation block while retaining AMP FP16 across convolutional layers for GPU speed.
- **Decision 2:** Implement non-in-place weight constraining for `BayarConv2d` to preserve PyTorch autograd computational graph integrity.
- **Decision 3:** Add rule to [[Development Rules]] mandating live model parameter counting and FP32 blocks for FFT transforms.

---

## ⚠️ Issues Encountered

- **Issue:** Initial attempts to clamp tensor outputs without disabling `autocast` still produced occasional `inf` values during FP16 backward passes.
- **Resolution:** Completely disabling `autocast` for `compute_fft_spectrum()` solved the numerical instability permanently.

---

## 🚀 Next Steps

- Proceed to build dual-model serving backend infrastructure (`inference.py`, `predict.py`).
