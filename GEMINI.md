# AI Image Detector

## Project Overview
A full-stack, local-first web application to detect if an image is AI-generated (DALL-E, Midjourney, Stable Diffusion) or a real photograph. The detection is powered by a dual-engine PyTorch model system featuring fine-tuned **EfficientNet-B0** and custom **ForensicNet** trained on a balanced dataset of real and AI-generated images.

## Architecture

### Frontend
- **Framework:** React with TypeScript (Vite).
- **Styling:** Reconciled design system (`DESIGN.md`, `theme.css`, `theme.js`) tailored for a stark ink-and-canvas developer platform aesthetic with cyberforensic terminal overlays (neon cyan glows, glassmorphic layout, ALL_CAPS_WITH_UNDERSCORES labels, and 3D interactive elements).
- **Asset Loading:** Lazy-loaded dynamic 3D background wrapper (`Background3D.tsx`) to optimize initial load times.
- **State Management:** Local/session state (session-based, no persistent history, zero user data retention).

### Backend
- **Framework:** FastAPI (Python) serving with Uvicorn.
- **Model Serving:** PyTorch dual-engine inference service (EfficientNet-B0 & ForensicNet).
- **API Pattern:** RESTful endpoints for health status check (`/health`), available models metadata (`/api/v1/models`), single image classification (`/api/v1/predict`), and batch classification (`/api/v1/predict/batch`).
- **Database:** SQLite placeholder (`forensics.db`) for tracking overall application-level stats (e.g., total visits, total images scanned).

## Core Workflows

### User Experience
1. **Landing Page:** Immersive intro section featuring glowing display typography, dynamic 3D graphics, dual-engine credibility metrics, and an "INITIALIZE SCANNER" call-to-action.
2. **Scanner / Upload Page:** Glassmorphic drag-and-drop single & batch file upload dropzones with interactive `ModelSelector` cards. Initiates a realistic terminal logs simulator mapping active neural link status and forward pass events.
3. **Results:** Display of prediction labels ("AI Generated" in red or "Real" in green) with confidence scores, exact forward pass execution time, primary signature readouts, and raw logs summary.

### Development & Security Rules
- **No Authentication:** The app is entirely session-based. Do not implement login, signup, or database persistence for user credentials.
- **CORS Constraints:** CORS origins strictly locked down to authorized domains (configured via the `ALLOWED_ORIGINS` environment variable).
- **Payload Limitation:** Enforce a strict 10MB maximum payload limit per image directly at the middleware level.
- **Image Integrity checks:** Match uploaded file extensions/MIME types and run binary signature verification (magic bytes) to prevent extension spoofing.
- **Secure Headers:** HTTP response middleware appends security headers: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`.

## ML Strategy

- **Dual-Model System:**
  - **EfficientNet-B0**: Fine-tuned transfer learning CNN (1280 -> 512 -> 2 Linear head, Dropout 0.4). Backbone unfrozen at epoch 8 for deep fine-tuning. Optimized for highest classification accuracy.
  - **ForensicNet**: Custom tri-stream deep neural architecture combining spatial pixel analysis, noise residual extraction (SRM filters), and frequency domain (DCT) decomposition. Optimized for ultra-fast GPU inference speed.
- **Training Pipeline:** Training utilizes Mixed Precision (AMP) for reduced GPU memory footprint and is configured using optimal dataloader worker benchmarking.
- **Dataset:** Combined dataset of Kaggle "AI Generated Images vs Real Images" and deepfake/face-swap samples (~238,000 images total) balanced across classes (`real` and `fake`).
- **Preprocessing:** Resize to 256x256, center-crop to 224x224, and normalize with standard ImageNet statistics (`mean=[0.485, 0.456, 0.406]`, `std=[0.229, 0.224, 0.225]`).

### Evaluation Results
Current evaluation statistics across both served models (from `backend/ml/evaluation_results*.json`):

| Metric | EfficientNet-B0 | ForensicNet |
| :--- | :--- | :--- |
| **Accuracy** | 97.82% | 94.83% |
| **AUC-ROC** | 0.9979 | 0.9903 |
| **Precision (Macro)** | 97.82% | 94.84% |
| **Recall (Macro)** | 97.82% | 94.83% |
| **F1-Score (Macro)** | 97.82% | 94.83% |
| **Parameter Count** | 4.66M | 1.05M |
| **GPU Inference Speed** | ~3.78 ms / image | ~1.78 ms / image |
| **CPU Inference Speed** | ~12.24 ms / image | ~5.60 ms / image |


