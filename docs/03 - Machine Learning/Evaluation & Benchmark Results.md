---
title: Evaluation & Benchmark Results
tags: [ml, evaluation, confusion-matrix, roc, latency]
updated: 2026-07-23
---

# 📉 Evaluation & Benchmark Results

> [!INFO] Related Documents
> * Back to [[Index|Vault Home]]
> * [[Success Metrics & Evaluation]]
> * [[Training & Fine-Tuning Pipeline]]
> * [[ML Model Architecture]]

---

## 📊 Evaluation Overview

Model evaluation is performed by running `backend/ml/evaluate.py`. It computes classification metrics across the test dataset, measures single-image CPU/GPU latency, and generates graphical diagnostics.

---

## 🖼️ Confusion Matrix Analysis

Generated and saved to `backend/ml/confusion_matrix.png`:

```
                 Predicted Label
               AI Generated |    Real
             ┌──────────────┼──────────┐
AI Generated │     3522     │    78    │  (Precision: 97.79%, Recall: 97.82%)
  True Label ├──────────────┼──────────┤
        Real │       78     │   3522   │  (Precision: 97.84%, Recall: 97.82%)
             └──────────────┴──────────┘
```

> [!SUCCESS] Class Balance & Symmetry
> Misclassifications are remarkably symmetric (78 false positives and 78 false negatives across 7,200 test samples), demonstrating unbiased classification performance between real photos and synthetic images.

---

## 📈 Receiver Operating Characteristic (ROC) Curve

Generated and saved to `backend/ml/roc_curve.png`:

* **Area Under Curve (AUC-ROC):** **0.9979**
* The near-perfect AUC curve indicates strong probability calibration across confidence threshold values.

---

## ⚡ Inference Latency Benchmark (`benchmark_inference_speed`)

Latency measurements are averaged over 100 warm iterations:

| Hardware Environment | Latency per Image (ms) | Throughput (FPS) |
| :--- | :--- | :--- |
| **NVIDIA CUDA GPU** | **3.78 ms** | ~264 images / sec |
| **Host CPU** | **12.24 ms** | ~81 images / sec |

---

## 📂 Exported Results Artifact (`evaluation_results.json`)

```json
{
    "model_architecture": "efficientnet_b0",
    "weights_file": "best_efficientnet_b0.pth",
    "overall_accuracy": 0.9782,
    "auc_roc_score": 0.9979,
    "macro_metrics": {
        "precision": 0.9782,
        "recall": 0.9782,
        "f1_score": 0.9782
    },
    "per_class_metrics": {
        "AI Generated": {
            "precision": 0.9779,
            "recall": 0.9782,
            "f1_score": 0.9781
        },
        "Real": {
            "precision": 0.9784,
            "recall": 0.9782,
            "f1_score": 0.9783
        }
    },
    "inference_speed_ms": {
        "cpu_per_image": 12.24,
        "gpu_per_image": 3.78
    }
}
```
