---
title: Background3D Component
tags: [frontend, component, threejs, 3d, animation, particle]
updated: 2026-07-23
---

# 🌌 Background3D Component (`frontend/src/components/Background3D.tsx`)

> [!INFO] Related Documents
> * Back to [[Index|Vault Home]]
> * [[Frontend Architecture]]
> * [[Design System & Theme]]

---

## 📄 Component Overview

`Background3D.tsx` renders an interactive 3D particle canvas using **Three.js**. The particle system creates an ambient deep-space particle mesh that dynamically tilts and shifts in response to user mouse movements.

---

## ⚙️ Technical Implementation Highlights

* **Canvas Lifecycle:** Uses `useRef<HTMLCanvasElement>` and `useEffect` to instantiate Three.js `PerspectiveCamera`, `Scene`, and `WebGLRenderer`.
* **Particle Geometry:** Generates a `BufferGeometry` containing thousands of cyan (`#66fcf1`) vertices.
* **Performance Optimization:**
  * Uses `requestAnimationFrame` loop.
  * Disposes of geometries and materials on unmount to prevent WebGL memory leaks.
  * Lazy-loaded in `Layout.tsx` to optimize initial load times.

---

## 🔗 Related Components
* Rendered at root of [[Frontend Architecture|Layout.tsx]].
