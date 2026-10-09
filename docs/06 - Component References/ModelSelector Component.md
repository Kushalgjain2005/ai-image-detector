---
title: ModelSelector Component Reference
tags: [component, frontend, react, model-selector, ui]
updated: 2026-08-09
---

# 🎛️ ModelSelector Component Reference

> [!INFO] Related Documents
> * Back to [[Index|Vault Home]]
> * [[Frontend Architecture]]
> * [[Detector Page]]
> * [[Scanner Component]]
> * [[Model Overview]]

---

## 📐 Overview

The `ModelSelector` component (`frontend/src/components/ModelSelector.tsx`) provides an interactive pill-button selector for toggling between production models (**EfficientNet-B0** and **ForensicNet**) in the React frontend interface (`Detector.tsx`).

---

## 💻 Component Interface & Usage

```tsx
export interface ModelSelectorProps {
  selectedModel: string;
  onSelectModel: (modelId: string) => void;
  disabled?: boolean;
}
```

* **Props:**
  - `selectedModel`: Currently active model identifier (`"efficientnet"` or `"forensicnet"`).
  - `onSelectModel`: Callback handler triggered when the user switches model selection.
  - `disabled`: Optional boolean disabling interaction during active image upload / forward pass processing.

---

## 🔗 Key Dependencies & Styling

* Uses cyberpunk styling tokens from `frontend/src/styles/theme.css`.
* Communicates with `frontend/src/services/api.ts` to pass the `model` choice to `predictImage()` and `predictBatch()` endpoints.
