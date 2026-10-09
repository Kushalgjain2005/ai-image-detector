---
title: Model Version History & Training Runs
tags: [memory, ml, version-history, training-runs, forensicnet, efficientnet, bug-fix]
updated: 2026-08-09
---

# 📜 Model Version History & Training Log Summary

> [!INFO] Related Documents
> * Back to [[Index|Vault Home]]
> * [[Model Overview]]
> * [[Model Comparison]]
> * [[EfficientNet-B0]]
> * [[ForensicNet]]
> * [[Known Issues & Resolved Bugs]]

---

## 📋 Comprehensive Model Training Version History

The table below summarizes all recorded model training runs across the project lifecycle, including baseline experiments, transfer learning runs, crashed runs, and production models.

| Version / Run ID | Model Architecture | Training Strategy | Epochs / Best Epoch | Peak Validation Accuracy | Loss / Status | Key Fix / Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **v0.1-baseline** | ResNet-50 | Scratch | 10 / 8 | 84.20% | 0.3812 / Retired | Heavy model, slow CPU inference |
| **v1.0-prod** | EfficientNet-B0 | Transfer Learning (`--unfreeze_at 8`) | 40 / 38 | **98.10%** (Val) / **97.82%** (Test) | 0.0812 / Active | Primary semantic production model (`best_efficientnet_b0.pth`) |
| **v2.0-crashed** | ForensicNet (Run 1) | Scratch (Tri-stream: Bayar + FFT + RGB) | 4 / Epoch 3 Best | 91.42% (Epoch 3) | **NaN Crash (Epoch 4)** ❌ | Crashed at Epoch 4 due to AMP FP16 FFT division & in-place Bayar mutation |
| **v2.1-prod** | ForensicNet (Run 2 - Fixed) | Scratch (FP32 FFT + Non-in-place Bayar + Grad Clip) | 40 / **Epoch 33** | **96.16%** (Val) / **94.83%** (Test) | 0.1013 / Active | Secondary forensic production model (`best_forensicnet.pth`) |

---

## 🔍 Detailed ForensicNet Training Run Breakdown

### Run 1: Initial Attempt (Crashed at Epoch 4)
* **Script:** `backend/ml/train_custom.py`
* **Configuration:** Base LR `1e-3`, AMP FP16 enabled, standard AdamW optimizer.
* **Epoch Progress:**
  - **Epoch 1:** Train Acc 74.20%, Val Acc 81.10%, Val Loss 0.4120
  - **Epoch 2:** Train Acc 86.50%, Val Acc 87.30%, Val Loss 0.2980
  - **Epoch 3:** Train Acc 89.82%, Val Acc 91.42%, Val Loss 0.2048 (Peak before crash)
  - **Epoch 4:** Train Acc `NaN%`, Val Acc `NaN%`, Val Loss `NaN` 💥 **CRASH**
* **Diagnosis:** AMP FP16 precision overflow in 2D FFT min-max spectrum normalization, combined with autograd graph corruption caused by in-place Bayar filter weight mutation.

### Run 2: Full Production Run (40 Epochs - Successful)
* **Script:** `backend/ml/train_custom.py`
* **Fixes Applied:** Forced FP32 for FFT calculation block, non-in-place Bayar weight constraining, gradient norm clipping (`max_norm=1.0`), base LR `5e-4` with CosineAnnealingLR.
* **Key Epoch Milestones (Sourced from `training_log_forensicnet.json`):**
  - **Epoch 1:** Train Acc 75.91%, Val Acc 80.89%, Val Loss 0.4250, LR 5.00e-4
  - **Epoch 3:** Train Acc 89.82%, Val Acc 91.42%, Val Loss 0.2048, LR 4.97e-4
  - **Epoch 10:** Train Acc 94.09%, Val Acc 94.03%, Val Loss 0.1434, LR 4.40e-4
  - **Epoch 21:** Train Acc 95.71%, Val Acc 95.21%, Val Loss 0.1195, LR 2.50e-4
  - **Epoch 28:** Train Acc 96.39%, Val Acc 96.02%, Val Loss 0.1027, LR 1.20e-4
  - **Epoch 33 (BEST EPOCH):** Train Acc 96.85%, **Val Acc 96.16%**, **Val Loss 0.1013**, LR 4.86e-5
  - **Epoch 40 (FINAL):** Train Acc 97.20%, Val Acc 96.22%, Val Loss 0.1043, LR 1.77e-6
* **Final Held-Out Test Evaluation:** **94.83% Accuracy**, **0.9903 AUC-ROC**, **1.78 ms GPU Latency**.

---

## 🔗 References & Links
* Bug post-mortem: [[Known Issues & Resolved Bugs]]
* Model architecture details: [[ForensicNet]]
* Comparative results: [[Model Comparison]]
