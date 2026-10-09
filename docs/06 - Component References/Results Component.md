---
title: Results Component
tags: [frontend, component, results, verdict, confidence]
updated: 2026-07-23
---

# 📊 Results Component (`frontend/src/components/Results.tsx`)

> [!INFO] Related Documents
> * Back to [[Index|Vault Home]]
> * [[Frontend Architecture]]
> * [[Scanner Component]]
> * [[Design System & Theme]]

---

## 📄 Component Overview

`Results.tsx` renders the classification verdict, confidence percentage meter, and forward pass execution telemetry once inference completes.

---

## 🎨 Visual Verdict Rendering

* **AI Generated Verdict:**
  * Label: `AI GENERATED`
  * Primary Color: Neon Red (`#ff4136` / `#ff3366` glow)
  * Visual Alert: High warning glow
* **Real Photograph Verdict:**
  * Label: `AUTHENTIC PHOTOGRAPH`
  * Primary Color: Neon Green (`#2ecc40` / `#00ffcc` glow)
  * Visual Alert: Verified status check

---

## 🧩 Props & Interface Schema

```typescript
interface PredictionResult {
  label: 'AI Generated' | 'Real';
  confidence: number; // 0.0 to 1.0
  inference_time_ms: number;
}

interface ResultsProps {
  result: PredictionResult;
  imagePreviewUrl: string;
  onReset: () => void;
}
```

---

## 🔗 Related Components
* Connected with `predictSingleImage()` in `frontend/src/services/api.ts`.
* Styling tokens defined in [[Design System & Theme]].
