---
title: Inference Service
tags: [backend, service, pytorch, inference, singleton]
updated: 2026-07-23
---

# 🧠 Inference Service (`backend/app/services/inference.py`)

> [!INFO] Related Documents
> * Back to [[Index|Vault Home]]
> * [[Backend Architecture]]
> * [[ML Model Architecture]]
> * [[API Specification]]

---

## 📄 Service Overview

`inference.py` acts as the singleton manager for the PyTorch EfficientNet-B0 model. It keeps model weights resident in GPU/CPU memory across server lifetime and handles image preprocessing and forward pass timing.

---

## 🔑 Core Service Functions

### 1. `get_device() -> torch.device`
Auto-selects `cuda` if an NVIDIA GPU is present, otherwise falls back to `cpu`.

### 2. `initialize_model(model_path: Optional[str]) -> nn.Module`
Instantiates `models.efficientnet_b0`, replaces the classifier head with `nn.Sequential(Linear(1280, 512), ReLU(), Dropout(0.4), Linear(512, 2))`, loads weights from `best_efficientnet_b0.pth`, calls `.eval()`, and stores the instance in singleton variable `_model`.

### 3. `preprocess_image_bytes(image_bytes: bytes) -> torch.Tensor`
Decodes binary bytes using PIL (`Image.open().convert("RGB")`), applies standard ImageNet validation transforms (`Resize 256 -> CenterCrop 224 -> ToTensor -> Normalize`), and returns a batch tensor of shape `(1, 3, 224, 224)`.

### 4. `run_forward_pass(tensor: torch.Tensor, device: torch.device)`
Executes `_model(tensor)` under `torch.no_grad()`. Synchronizes CUDA clocks if GPU is active to return accurate wall-clock `inference_time_ms`.

### 5. `predict(image_bytes: bytes) -> Dict[str, Any]`
Orchestrates preprocessing, forward pass, Softmax probability calculation, and label resolution (`0 = AI Generated`, `1 = Real`).

---

## 🔗 Related Components
* Invoked by prediction endpoints in [[API Specification]].
* Architecture details defined in [[ML Model Architecture]].
