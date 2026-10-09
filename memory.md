# Project Decisions & History Log (Memory) — AI Image Detector

## 1. Key Technical Decisions

### Decision 1: Choice of EfficientNet-B0 over ResNet-50
* **Decision:** Adopted EfficientNet-B0 as the primary model architecture for production serving instead of ResNet-50.
* **Reasoning:** Evidenced by `backend/utils.py` (which contains legacy ResNet-50 utilities) vs `backend/app/services/inference.py` and `backend/ml/train.py` (which strictly implement EfficientNet-B0). EfficientNet-B0 provides significantly higher parameter efficiency, achieving **97.82% accuracy** while requiring only ~3.78 ms GPU / 12.24 ms CPU latency per forward pass.

### Decision 2: Multi-Stage Transfer Learning with Layer Unfreezing
* **Decision:** Implemented a two-stage training strategy: initial training with frozen backbone layers followed by unfreezing all parameters at epoch 8 (`--unfreeze_at 8`).
* **Reasoning:** Prevents destructive gradient updates to pretrained ImageNet features during early epochs, allowing the custom classifier head (1280 -> 512 -> 2) to converge before fine-tuning deeper spatial feature representations.

### Decision 3: Modular Dataset Merging Script (`merge_datasets.py`)
* **Decision:** Created an automated dataset merging tool to combine separate real and synthetic image datasets into a single unified directory structure (`backend/ml/data/merged_dataset/`).
* **Reasoning:** Facilitates dataset expansion (combining initial Kaggle sets with new deepfake corpora) while pre-validating file integrity with PIL and prefixing filenames to prevent directory collisions.

### Decision 4: In-Memory Only Image Processing (Zero Disk Persistence)
* **Decision:** Streams uploaded image bytes directly into `io.BytesIO` memory buffers for PIL decoding and PyTorch tensor transformation.
* **Reasoning:** Guarantees user privacy, eliminates server disk I/O bottlenecks, and prevents accumulation of temporary files.

### Decision 5: React Router SPA over Multi-Page Architecture
* **Decision:** Maintained a client-side Single Page Application using React Router v7 (`frontend/src/App.tsx`) backed by Vite.
* **Reasoning:** Enables smooth transitions between pages (`Home`, `Detector`, `HowItWorks`, `About`, `FAQ`) without destroying the persistent Three.js 3D background webgl context (`Background3D.tsx`).

---

## 2. Dataset History & Pipeline
* **Primary Dataset:** Kaggle "AI Generated Images vs Real Images" dataset containing ~48,000 balanced images (`real` vs `fake`).
* **Dataset Splitting:** 70% Train, 15% Validation, 15% Test configured in `backend/ml/dataset.py` using fixed random seeds (`seed=42`) for reproducibility.
* **Dataset Expansion:** Script `backend/ml/merge_datasets.py` provides dry-run capabilities and automatic disk space verification for merging secondary deepfake datasets.

---

## 3. Model Version History

| Version / Model | Weights File | Test Accuracy | AUC-ROC | Inference Speed (CPU / GPU) | Notes |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ResNet-50 Baseline** | `resnet50_finetuned.pth` | [VERIFY: Legacy baseline script exists in `utils.py`] | [VERIFY: Unrecorded] | ~25 ms / ~8 ms [VERIFY] | Initial baseline evaluation prior to EfficientNet adoption. |
| **EfficientNet-B0 (Final)** | `best_efficientnet_b0.pth` | **97.82%** | **0.9979** | **12.24 ms / 3.78 ms** | Current production model evaluated in `evaluation_results.json`. |

---

## 4. Known Issues & Resolved Bugs

* **DataLoader Subprocess Crash on Linux (`num_workers`):**
  * *Issue:* High `num_workers` values caused PyTorch DataLoader worker process failures and shared memory bottlenecks on certain host hardware.
  * *Resolution:* Added `benchmark_dataloader_workers()` utility in `train.py` to benchmark optimal worker counts (defaulting safely to `num_workers=2`).
* **Truncated / Corrupted File Crashes:**
  * *Issue:* Corrupted uploaded images or truncated JPEG buffers broke PIL image decoding during forward pass.
  * *Resolution:* Added PIL verification (`Image.open().verify()`) and binary signature magic byte checks (`validate_image_magic_bytes`) in request validation pipeline.
* **Extension & Content-Type Spoofing:**
  * *Issue:* Uploading non-image payloads (e.g. executable scripts or text files) disguised with `.jpg` extensions.
  * *Resolution:* Enforced strict magic byte signature checks at the API boundary before passing byte streams to PIL.

---

## 5. Open Questions & Future Considerations
* **[VERIFY: Database Purpose]** SQLite database module `backend/database.py` defines counters for `total_visits` and `total_scanned`, but is not actively imported in `main.py` or `predict.py`. Needs verification on whether global stats recording should be connected.
* **[VERIFY: Laser Line Animation]** Scanning cyan bar and terminal blinker CSS keyframes in `theme.css` [VERIFY: scanner keyframe animations defined in Scanner.tsx but not present in CSS file].
* **Support for AVIF / HEIC Formats:** Expanding supported input MIME types beyond JPEG, PNG, and WEBP.
