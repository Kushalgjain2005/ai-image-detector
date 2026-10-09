---
title: Dataset Management
tags: [ml, dataset, dataloader, pil, data-prep]
updated: 2026-07-23
---

# 📁 Dataset Management & Preparation

> [!INFO] Related Documents
> * Back to [[Index|Vault Home]]
> * [[Training & Fine-Tuning Pipeline]]
> * [[ML Model Architecture]]
> * [[Evaluation & Benchmark Results]]

---

## 📊 Dataset Description & Composition

* **Primary Corpus:** Kaggle "AI Generated Images vs Real Images" dataset containing **~48,000 images**.
* **Class Balance:** Balanced 1:1 distribution between `real` photographs and `fake` AI-generated images.
* **Splitting Ratio:** Configured in `backend/ml/dataset.py`:
  * **Train Split:** 70% (~33,600 images)
  * **Validation Split:** 15% (~7,200 images)
  * **Test Split:** 15% (~7,200 images)

---

## 🧹 Dataset Resolution & Validation

Dataset path resolving is handled automatically by `resolve_dataset_dir()` in `dataset.py`, detecting nested subfolders like `archive/train/` or `data/`:

```python
# Image Loading Defensive Guards
ImageFile.LOAD_TRUNCATED_IMAGES = False
Image.MAX_IMAGE_PIXELS = None
warnings.filterwarnings("ignore", category=Image.DecompressionBombWarning)
```

---

## 🔄 Augmentation Pipelines (`dataset.py`)

### Training Augmentations
Applies spatial and color jittering to increase generalization:
```python
train_transform = transforms.Compose([
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(10),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.RandomResizedCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
```

### Validation & Test Pipeline
Deterministic center cropping:
```python
val_transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
```

---

## 🔀 Dataset Merging Utility (`backend/ml/merge_datasets.py`)

To combine multiple dataset sources safely, `merge_datasets.py` scans directories, validates PIL readability, checks available disk space, and prefixes filenames to prevent overwrites:

```bash
# Example Usage of Merge Script
python backend/ml/merge_datasets.py \
  --dataset_a_path ./data/dataset_a \
  --dataset_b_path ./data/dataset_b \
  --dry_run
```

> [!IMPORTANT] Disk Space Check
> The script automatically calculates required target disk space and aborts if free disk space is insufficient prior to copying images.
