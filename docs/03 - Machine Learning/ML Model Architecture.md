---
title: ML Model Architecture Overview
tags: [ml, pytorch, efficientnet, forensicnet, dual-model, architecture]
updated: 2026-08-09
---

# 🤖 ML Model Architecture Overview

> [!INFO] Related Documents
> * Parent Overview: [[Model Overview]]
> * Comparative Analysis: [[Model Comparison]]
> * Transfer Learning Model: [[EfficientNet-B0]]
> * Custom Forensic Model: [[ForensicNet]]
> * Training Pipeline: [[Training & Fine-Tuning Pipeline]]

---

## 📐 Dual Model Architecture Summary

The **AI Image Detector** system hosts two complementary machine learning model architectures:

1. **[[EfficientNet-B0]]:** Semantic Transfer Learning CNN pretrained on ImageNet-1K. Replaces standard head with dense `(1280 -> 512 -> 2)` classification layers. Achieves **97.82% Accuracy** and **3.78 ms GPU / 12.24 ms CPU** inference times.
2. **[[ForensicNet]]:** Custom tri-stream neural network combining Bayar constrained noise residual convolutions (Stream A), 2D Discrete Fast Fourier Transform log-magnitude spectrum (Stream B), and spatial RGB context (Stream C). Features **1.05M parameters** (4.4x smaller) and **1.78 ms GPU** inference latency.

---

## 🔗 Dedicated Architecture Notes

For full layer breakdowns, mathematical formulations, code implementations, and training histories, refer to:

* **[[Model Overview]]** — Dual-model serving strategy and lifespan initialization.
* **[[Model Comparison]]** — Side-by-side metric comparison table and hardware performance trade-offs.
* **[[EfficientNet-B0]]** — ImageNet backbone transfer learning and fine-tuning details.
* **[[ForensicNet]]** — Multi-stream design, Bayar weight constraint equations, 2D FFT pipeline, and the NaN bug fix.
