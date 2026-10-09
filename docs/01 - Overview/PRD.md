---
title: Product Requirements Document (PRD)
tags: [overview, prd, requirements, features, dual-model, forensicnet, efficientnet]
updated: 2026-08-09
---

# 📄 Product Requirements Document (PRD) — Neural Forensic Engine

> [!INFO] Related Documents
> * Back to [[Index|Vault Home]]
> * [[Product Vision & Goals]]
> * [[Success Metrics & Evaluation]]
> * [[System Architecture]]
> * [[Model Overview]]
> * [[Model Comparison]]

---

## 1. Product Summary
**Product Name:** Neural Forensic Engine (AI Image Detector)  
**Summary:** A full-stack, local-first web application designed to analyze uploaded images and classify them as authentic photographs or AI-generated synthetic media (Midjourney, DALL-E, Stable Diffusion) with high-confidence scoring and ultra-low latency inference. The system features a dual-model serving architecture allowing users to dynamically switch between **EfficientNet-B0** (semantic transfer learning) and **ForensicNet** (custom noise/frequency domain analysis).

---

## 2. Problem Statement
The proliferation of generative AI models has saturated online media channels with synthetic imagery. Distinguishing authentic visual media from synthetic or manipulated images is essential for:
* **Combatting Digital Misinformation:** Verifying journalistic assets and social media reports.
* **Content Moderation:** Detecting AI-generated spam or unauthorized image synthesis.
* **Digital Forensics:** Providing fast, reproducible visual verification for analysts using complementary detection paradigms (spatial semantics vs frequency/residual noise artifacts).

This project delivers a fast, secure, local-first solution for real-time neural classification.

---

## 3. Target User Personas
1. **Digital Forensics Analysts & Journalists:** Require fast, reliable preliminary verification of image provenance with multiple model perspectives.
2. **Platform Content Moderators:** Need bulk or single image validation APIs supporting dual model execution.
3. **General Public / Portfolio Audience:** Users exploring AI safety tools through an interactive cyberpunk terminal interface.

---

## 4. Implemented Features (Built & Active)

| Feature | Description | Implementation Link |
| :--- | :--- | :--- |
| **Model Selection** | Toggle between **EfficientNet-B0** (97.82% accuracy) and **ForensicNet** (1.05M params, 1.78ms GPU latency) via interactive selector UI or API parameter. | [[ModelSelector Component]] & `POST /api/v1/predict` in [[API Specification]] |
| **Model Metadata API** | Fetch dynamic model capabilities, accuracy, parameter count, and availability status. | `GET /api/v1/models` in [[API Specification]] |
| **Single Image Prediction** | Upload single image up to 10MB (`.jpg`, `.png`, `.webp`). Returns label, confidence, execution time, and model telemetry. | `POST /api/v1/predict` in [[API Specification]] |
| **Batch Image Prediction** | Upload up to 10 images concurrently (max 110MB total payload) with per-file status reports and selected model routing. | `POST /api/v1/predict/batch` in [[API Specification]] |
| **Terminal Log Simulator** | Interactive frontend visualizer simulating neural link telemetry, model weight loading, and forward pass steps. | [[Scanner Component]] |
| **Dynamic 3D Background** | Three.js particle canvas reacting to mouse movements. | [[Background3D Component]] |
| **Multi-Stage Security** | Magic byte binary validation, CORS lockdown, rate limiting, and size enforcement across all models. | [[Security Guidelines]] |
| **System Diagnostics** | Health check monitoring backend operational status, PyTorch model load state, and active GPU/CPU device. | `GET /health` in [[API Specification]] |

---

## 5. Model Evaluation & Success Metrics

The platform serves two production models with complementary strengths, evaluated on the held-out test split (15% of 48,000 image Kaggle dataset):

| Metric | EfficientNet-B0 (Transfer Learning) | ForensicNet (Custom Tri-Stream) | Target Threshold | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Architecture Type** | CNN (ImageNet Backbone) | Custom (Bayar Noise + 2D FFT + RGB) | N/A | Active |
| **Test Accuracy** | **97.82%** (`0.9782`) | **94.83%** (`0.9483`) | > 90.00% | ✅ PASS |
| **AUC-ROC Score** | **0.9979** | **0.9903** | > 0.9500 | ✅ PASS |
| **Macro F1-Score** | **97.82%** (`0.9782`) | **94.83%** (`0.9483`) | > 90.00% | ✅ PASS |
| **GPU Inference Speed** | **3.78 ms** | **1.78 ms** (2.1x faster) | < 10.00 ms | ✅ PASS |
| **CPU Inference Speed** | **12.24 ms** | **85.76 ms** (FFT overhead) | < 100.00 ms | ✅ PASS |
| **Trainable Parameters** | **4,664,446** (`4.66M`) | **1,048,942** (`1.05M`, 4.4x smaller) | < 10.0M | ✅ PASS |

---

## 6. Out of Scope Features
* ❌ **User Accounts / Auth:** Entirely session-based; zero user login or OAuth.
* ❌ **Persistent History:** Uploaded images and prediction history are processed strictly in RAM and never saved to disk.
* ❌ **Video / Audio Analysis:** Only static 2D image classification is supported.
* ❌ **Image Editing / Manipulation:** No cropping, filtering, or watermarking tools provided.

---

## 7. Known Product Constraints
> [!WARNING] Operational Limits
> * Maximum single file size: **10 MB**
> * Maximum batch size: **10 files / 110 MB**
> * Rate limits: **30 requests/min** for single predictions, **5 requests/min** for batch predictions.
> * Supported formats: Strictly `JPEG`, `PNG`, and `WEBP`.

---

## 8. Next Steps & References
* View detailed model comparison and trade-offs in [[Model Comparison]].
* Explore model architectures in [[EfficientNet-B0]] and [[ForensicNet]].
* View API request schemas in [[API Specification]].
