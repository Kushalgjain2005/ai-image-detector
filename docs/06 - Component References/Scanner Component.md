---
title: Scanner Component
tags: [frontend, component, scanner, drag-and-drop, logs]
updated: 2026-07-23
---

# 🛸 Scanner Component (`frontend/src/components/Scanner.tsx`)

> [!INFO] Related Documents
> * Back to [[Index|Vault Home]]
> * [[Frontend Architecture]]
> * [[Results Component]]
> * [[Design System & Theme]]

---

## 📄 Component Overview

`Scanner.tsx` handles file upload selection, drag-and-drop interactions, and real-time terminal log simulation during image scanning.

---

## 🎨 Visual Design & UI Layout

* **Glassmorphic Dropzone:** High-contrast cyan dashed border (`#66fcf1`) with hover elevation.
* **Terminal Telemetry Panel:** Dark terminal block (`#000000`) displaying simulated scanning steps:
  * `[+] INITIALIZING NEURAL LINK...`
  * `[+] VERIFYING MAGIC BYTES...`
  * `[+] EXECUTING FORWARD PASS...`
  * `[+] COMPUTING SOFTMAX PROBABILITIES...`

---

## 🧩 Props & Interface Schema

```typescript
interface ScannerProps {
  onFileSelect: (file: File) => void;
  isScanning: boolean;
  scanProgress: number;
  currentLog: string;
}
```

---

## 🔗 Related Components
* Outputs uploaded files to [[Results Component]] via parent page state (`Detector.tsx`).
* Uses theme colors specified in [[Design System & Theme]].
