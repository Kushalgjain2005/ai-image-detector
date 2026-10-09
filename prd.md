# Product Requirements Document (PRD) — AI Image Detector

## 1. Product Name & One-Line Summary
**Product Name:** Neural Forensic Engine (AI Image Detector)  
**Summary:** A full-stack, local-first web application designed to analyze uploaded images and accurately classify them as real photographs or AI-generated synthetic media (e.g., Midjourney, DALL-E, Stable Diffusion) with high-confidence scoring and low-latency inference.

---

## 2. Problem Statement
The exponential rise of generative AI models has flooded digital channels with hyper-realistic synthetic imagery. Distinguishing authentic visual media from AI-generated or manipulated images has become increasingly critical for combatting digital misinformation, verifying journalistic assets, and protecting brand integrity. This project solves the problem of automated image authenticity verification by providing a fast, secure, and accessible neural classification pipeline.

---

## 3. Target Users
* **Digital Forensics Analysts & Journalists:** Individuals needing rapid, reliable preliminary classification of image sources.
* **Platform Content Moderators:** Teams checking media authenticity against synthetic generation signatures.
* **General Public / Portfolio Audience:** Users exploring local-first AI safety tools through an intuitive, interactive cyberpunk web terminal interface.

---

## 4. Core Features (Implemented & Built)
* **Single Image Detection (`POST /api/v1/predict`):** Upload single images (JPEG, PNG, WEBP, up to 10MB) for instant inference. Returns predicted label (`AI Generated` or `Real`), confidence score (0.0 to 1.0), and forward pass execution time in milliseconds.
* **Batch Image Detection (`POST /api/v1/predict/batch`):** Upload up to 10 images concurrently in a single batch request (max total payload size 110MB). Processes items independently with itemized success/error responses.
* **Real-time Terminal Log Simulator:** Interactive visual feedback during image analysis, displaying forward pass execution events and neural link telemetry on the frontend.
* **Dynamic 3D Background Wrapper (`Background3D.tsx`):** Interactive Three.js particle canvas reacting to mouse movements with fallback rendering.
* **Cyberpunk Visual Interface:** High-contrast glassmorphic panels, neon cyan highlights (`#66fcf1`), scanline overlay, and animated result indicators.
* **Multi-Layer Security Validation:**
  * Strict MIME type and extension validation (`.jpg`, `.jpeg`, `.png`, `.webp`).
  * Binary signature (magic bytes) verification preventing file extension spoofing.
  * PIL image payload integrity decoding to reject corrupted file payloads.
  * In-memory sliding window rate limiting (30 requests/min for single, 5 requests/min for batch).
  * Payload size enforcement at HTTP middleware level (10MB single, 110MB batch).
  * HTTP security response headers (`X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`).
* **System Health Monitoring (`GET /health`):** Operational status reporting, ML model readiness indicator, and active compute device identifier (`cuda` or `cpu`).

---

## 5. Out of Scope
* **User Accounts & Authentication:** The application is entirely session-based with zero user login, registration, or OAuth flows.
* **User Data Persistence:** Uploaded image binary streams and individual user prediction histories are never written to disk or stored permanently.
* **Video / Audio Forensics:** Synthetic video or audio deepfake analysis is explicitly not supported.
* **Image Editing / Alteration Tools:** Features for modifying, cropping, or watermarking uploaded images within the UI.
* **Cloud Database User Metrics:** Persistent database user tracking [VERIFY: SQLite `forensics.db` contains basic global visit counters in backend code, but no user-level database tables exist].

---

## 6. Success Metrics (Real Evaluation Results)
Metrics extracted directly from `backend/ml/evaluation_results.json` evaluated on the test split:

| Metric | Measured Value |
| :--- | :--- |
| **Overall Accuracy** | 97.82% (0.9782) |
| **AUC-ROC Score** | 0.9979 |
| **Macro Precision** | 97.82% (0.9782) |
| **Macro Recall** | 97.82% (0.9782) |
| **Macro F1-Score** | 97.82% (0.9782) |
| **AI Generated Class F1** | 97.81% (Precision: 97.79%, Recall: 97.82%) |
| **Real Class F1** | 97.83% (Precision: 97.84%, Recall: 97.82%) |
| **GPU Inference Latency** | **3.78 ms** per image |
| **CPU Inference Latency** | **12.24 ms** per image |

---

## 7. Known Limitations
* **Maximum File Constraints:** Uploads strictly capped at 10MB per image and 10 images per batch request.
* **Supported File Formats:** Limited strictly to JPEG, PNG, and WEBP. Other image formats (e.g. AVIF, HEIC, TIFF) are rejected.
* **Domain Gap Sensitivity:** Heavily re-compressed images (e.g. from messaging apps) or unseen generative architectures outside training distributions may experience reduced confidence scores.
* **In-Memory Rate Limiting:** Sliding-window rate limit counters are stored in RAM and reset upon server restart.
