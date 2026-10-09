# Technical Architecture — AI Image Detector

## 1. System Overview
The AI Image Detector (Neural Forensic Engine) operates as a decoupled, local-first client-server application. The frontend is built as a Single Page Application (SPA) using React 19, Vite, TypeScript, and Three.js for interactive rendering, styled according to the authoritative `DESIGN.md` visual specification (`theme.css` and `theme.js`). The backend is a lightweight FastAPI service running under Uvicorn, which handles request routing, binary image validation, rate limiting, and dual-engine model inference via PyTorch (**EfficientNet-B0** & **ForensicNet**).

```
+-----------------------------------------------------------------------------------+
|                                 FRONTEND (Vite / React 19)                         |
|  [Pages: Home, Detector, HowItWorks, About, FAQ, NotFound]                        |
|  [Components: Layout, Scanner, Results, ModelSelector, Background3D, Sidebars]     |
|  [Theme: DESIGN.md, theme.css, theme.js (Reconciled Cyberforensic Tokens)]        |
+---------------------------------------------------------+-------------------------+
                                                          |
                                         REST API (HTTP / JSON / Form-Data)
                                                          |
+---------------------------------------------------------v-------------------------+
|                                 BACKEND (FastAPI / Uvicorn)                       |
|  [Middleware: Security Headers, Request Size Enforcer, Logger]                    |
|  [Routes: GET /health, GET /api/v1/models, POST /api/v1/predict, POST batch]    |
+---------------------------------------------------------+-------------------------+
                                                          |
                                           In-Memory Tensor Pipeline
                                                          |
+---------------------------------------------------------v-------------------------+
|                              MODEL INFERENCE (PyTorch Service)                     |
|  [Preprocessing: Resize 256 -> CenterCrop 224 -> ToTensor -> Normalize]           |
|  [Model 1: EfficientNet-B0 Backbone + Custom Head (1280->512->2) | 97.82% Acc]    |
|  [Model 2: ForensicNet Tri-Stream (Spatial + Noise SRM + Frequency DCT) | 94.83%] |
|  [Weights: backend/ml/model_weights/best_efficientnet_b0.pth & forensicnet.pth]   |
+-----------------------------------------------------------------------------------+
```

---

## 2. Frontend Architecture
* **Framework & Build:** React 19, TypeScript, Vite 8, Tailwind CSS v4 (`@tailwindcss/vite`).
* **Routing Structure (`frontend/src/App.tsx`):**
  * `/` -> `HomePage` (`frontend/src/pages/Home.tsx`)
  * `/detector` -> `DetectorPage` (`frontend/src/pages/Detector.tsx`)
  * `/how-it-works` -> `HowItWorksPage` (`frontend/src/pages/HowItWorks.tsx`)
  * `/about` -> `AboutPage` (`frontend/src/pages/About.tsx`)
  * `/faq` -> `FAQPage` (`frontend/src/pages/FAQ.tsx`)
  * `*` -> `NotFoundPage` (`frontend/src/pages/NotFound.tsx`)
* **Component Structure (`frontend/src/components/`):**
  * `Layout.tsx`: Root wrapper rendering Navbar, Footer, and `Background3D`.
  * `Scanner.tsx`: Glassmorphic single & batch file upload dropzone and terminal scan animation trigger.
  * `Results.tsx`: Single and batch result views featuring signature readouts and confidence bars.
  * `ModelSelector.tsx`: Interactive model selection cards displaying accuracy, AUC-ROC, parameters, and live status.
  * `Background3D.tsx`: Three.js interactive particle background system.
  * `Sidebars.tsx`: Decorative tactical sidebars rendering live telemetry readouts.
  * `ErrorBoundary.tsx`: React error boundary for runtime UI resilience.
* **State Management:** Local React component state (`useState`, `useRef`) for file handles, model selection state, scanning logs, and prediction results.
* **Styling System:** Reconciled visual token specification defined in `DESIGN.md`, implemented via `frontend/src/styles/theme.css` and `frontend/src/styles/theme.js`. Enforces `ALL_CAPS_WITH_UNDERSCORES` terminal labeling and JetBrains Mono monospace readouts.

---

## 3. Backend Architecture
* **Framework & Server:** FastAPI serving via Uvicorn on port 8000.
* **API Endpoints (`backend/app/main.py` & `backend/app/routes/predict.py`):**
  * `GET /health`: Returns operational status, model loaded flag, and hardware device (`cuda` / `cpu`).
  * `GET /api/v1/models`: Returns metadata, parameter counts, and accuracy benchmarks for all available models.
  * `POST /api/v1/predict`: Single image classification endpoint accepting `image` file and optional `model` parameter (`efficientnet` or `forensicnet`).
  * `POST /api/v1/predict/batch`: Batch image classification endpoint accepting up to 10 files and optional `model` choice.
  * `GET /{file_name:path}`: Serves frontend production build static assets from `frontend/dist` when available.
* **Implemented Middleware (`backend/app/main.py`):**
  * `CORSMiddleware`: Locked to explicit origins from `ALLOWED_ORIGINS` environment variable (defaults to `http://localhost:3000`).
  * `add_security_headers`: Sets `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, and `X-XSS-Protection: 1; mode=block`.
  * `enforce_max_request_size`: Rejects requests exceeding 10MB (single) or 110MB (batch) with HTTP 413.
  * `log_requests`: Timed HTTP logger recording client IP, method, status, and duration in `backend/logs/app.log`.
  * `InMemoryRateLimiter`: Enforces 30 req/min for single predict and 5 req/min for batch predict per IP.
* **Inference Service Pattern (`backend/app/services/inference.py`):**
  * Singleton module pattern managing resident PyTorch model instances (`EfficientNet-B0` & `ForensicNet`) in RAM/VRAM across requests.

---

## 4. Model Architecture & Training Pipeline
* **Model 1 — EfficientNet-B0:**
  * **Base Architecture:** `torchvision.models.efficientnet_b0`.
  * **Classifier Head:** `nn.Sequential(nn.Linear(1280, 512), nn.ReLU(), nn.Dropout(0.4), nn.Linear(512, 2))`
  * **Performance:** 97.82% Accuracy · 0.9979 AUC-ROC · 4.66M Parameters · 3.78ms GPU Latency.
* **Model 2 — ForensicNet:**
  * **Architecture:** Custom tri-stream deep neural network combining spatial RGB features, noise residual features (SRM filter bank), and frequency domain representations (2D DCT).
  * **Performance:** 94.83% Accuracy · 0.9903 AUC-ROC · 1.05M Parameters · 1.78ms GPU Latency.
* **Input Preprocessing Pipeline (`backend/app/services/inference.py` & `backend/ml/dataset.py`):**
  1. `transforms.Resize(256)`
  2. `transforms.CenterCrop(224)`
  3. `transforms.ToTensor()`
  4. `transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])`
* **Training Pipeline (`backend/ml/train.py` & `backend/ml/run_training_pipeline.py`):**
  * **Transfer Learning:** Initial training phase freezes backbone weights, training only the classifier head.
  * **Deep Fine-Tuning:** Unfreezes all backbone parameters starting at epoch 8 (`--unfreeze_at 8`) with learning rate decay.
  * **Optimization & Loss:** Adam optimizer (initial `lr=0.0005`, `weight_decay=1e-4`), `ReduceLROnPlateau` scheduler, and `CrossEntropyLoss`.
  * **Mixed Precision:** Automatic Mixed Precision (`torch.cuda.amp.autocast`) enabled on CUDA devices.
  * **Dataset Split:** 70% Train, 15% Validation, 15% Test (~238,000 images total).

---

## 5. Data Flow (Image Upload to Result Display)
1. User drops an image file into `Scanner.tsx` on the frontend (`DetectorPage`).
2. Frontend sends an HTTP POST request to `http://localhost:8000/api/v1/predict` via `frontend/src/services/api.ts` using `formData`.
3. Backend middleware (`main.py`) checks `Content-Length` header against 10MB limit.
4. `predict.py` endpoint checks in-memory rate limiter for client IP address.
5. Metadata validation (`validate_file_metadata`) checks extension (`.jpg`, `.jpeg`, `.png`, `.webp`) and MIME content type.
6. Binary integrity check (`validate_file_binary_integrity` in `security.py`) verifies magic bytes (`FF D8 FF` for JPEG, `\x89PNG` for PNG, `RIFF...WEBP` for WEBP) and attempts PIL verification.
7. Valid binary stream is passed to `inference.predict()` in `backend/app/services/inference.py`.
8. Image bytes are decoded into RGB PIL Image, transformed into normalized $(1, 3, 224, 224)$ PyTorch tensor, and evaluated under `torch.no_grad()`.
9. Softmax probabilities are mapped via `LABEL_MAPPING` (`0: "AI Generated"`, `1: "Real"`).
10. Response object containing `label`, `confidence`, and `inference_time_ms` is returned to frontend and displayed in `Results.tsx`.

---

## 6. Project Structure
```
ai-image-detector/
├── GEMINI.md
├── README.md
├── requirements.txt (root / backend reference)
├── run.py
├── start.sh / start.bat
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   ├── routes/
│   │   │   └── predict.py
│   │   ├── services/
│   │   │   └── inference.py
│   │   └── utils/
│   │       └── security.py
│   ├── database.py
│   ├── logs/
│   │   └── app.log
│   ├── ml/
│   │   ├── clean_dataset.py
│   │   ├── dataset.py
│   │   ├── evaluate.py
│   │   ├── evaluation_results.json
│   │   ├── merge_datasets.py
│   │   ├── plot_training.py
│   │   ├── run_training_pipeline.py
│   │   ├── train.py
│   │   ├── training_log.json
│   │   └── model_weights/
│   │       └── best_efficientnet_b0.pth
│   ├── requirements.txt
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_api.py
│   └── utils.py
└── frontend/
    ├── package.json
    ├── vite.config.ts
    ├── index.html
    └── src/
        ├── App.tsx
        ├── Background3D.tsx
        ├── main.tsx
        ├── components/
        │   ├── ErrorBoundary.tsx
        │   ├── Layout.tsx
        │   ├── Results.tsx
        │   ├── Scanner.tsx
        │   └── Sidebars.tsx
        ├── pages/
        │   ├── About.tsx
        │   ├── Detector.tsx
        │   ├── FAQ.tsx
        │   ├── Home.tsx
        │   ├── HowItWorks.tsx
        │   └── NotFound.tsx
        ├── services/
        │   └── api.ts
        └── styles/
            └── theme.css
```

---

## 7. Dependencies

### Backend (Python / ML)
* **ML & Compute:** `torch`, `torchvision`, `numpy`, `scikit-learn`, `pillow`
* **API Framework:** `fastapi`, `uvicorn`, `pydantic`, `python-multipart`
* **Utilities & Logging:** `python-dotenv`, `tqdm`, `matplotlib`, `seaborn`, `aiofiles`

### Frontend (Node / React)
* **Core Framework:** `react` (v19), `react-dom`, `typescript`
* **Routing & SEO:** `react-router-dom` (v7), `react-helmet-async`
* **Graphics & Animation:** `three`, `@types/three`, `framer-motion`
* **Build & Styling:** `vite`, `@vitejs/plugin-react`, `tailwindcss` (v4), `@tailwindcss/vite`

---

## 8. Security Measures
* **Binary Magic Byte Verification:** Verifies initial file bytes against known signatures (`validate_image_magic_bytes`).
* **Strict CORS Lockdown:** Restricts cross-origin requests to configured domains in `ALLOWED_ORIGINS`.
* **Payload Size Limits:** 10MB per single file / 110MB per batch enforced at FastAPI HTTP middleware layer.
* **In-Memory Rate Limiting:** Prevents Denial of Service via IP sliding-window limiting (30 single req/min, 5 batch req/min).
* **Sanitized Error Responses:** Generic HTTP 500 responses return uninformative error messages to clients while logging detailed stack traces to disk (`app.log`).
* **HTTP Security Headers:** `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `X-XSS-Protection: 1; mode=block`.
* **Path Traversal Protection:** Static file route explicitly blocks paths starting with `api/` or `health` and checks path boundaries.
