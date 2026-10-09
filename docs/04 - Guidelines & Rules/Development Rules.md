---
title: Development Rules & Conventions
tags: [rules, conventions, coding-style, guidelines, multi-model, security]
updated: 2026-08-09
---

# 📜 Development Rules & Coding Conventions

> [!INFO] Related Documents
> * Back to [[Index|Vault Home]]
> * [[Design System & Theme]]
> * [[Security Guidelines]]
> * [[Known Issues & Resolved Bugs]]
> * [[Testing Strategy]]

---

## 🐍 Backend Rules & Conventions (Python / FastAPI)

1. **PEP 8 Compliance:** 4-space indentation, explicit type hints (`Optional`, `List`, `Dict`, `Tuple`), and module docstrings.
2. **Structured Logging:** All backend logs must use `logging.getLogger("app_logger")`. Never use raw `print()` statements in API routes.
3. **Mandatory File Validation:** Every endpoint handling image uploads must execute the full validation pipeline:
   * Extension check (`validate_file_metadata`)
   * Size limit check (10MB / 110MB)
   * Magic bytes verification (`validate_image_magic_bytes`)
   * PIL decoding verification (`Image.open().verify()`)
4. **Sanitized Error Responses:** Never return raw Python tracebacks to clients. Catch exceptions and return clean JSON errors:
   ```python
   raise HTTPException(
       status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
       detail="Unprocessable Entity. Invalid or corrupted image data."
   )
   ```
5. **Rate Limiting:** All user-facing prediction routes must enforce `InMemoryRateLimiter`.

---

## 🤖 Multi-Model Consistency Rules

1. **Dynamic Parameter & Metric Computation:** Parameter counts and performance metrics must ALWAYS be computed live from PyTorch model instances (`sum(p.numel() for p in model.parameters())`) or parsed directly from `evaluation_results.json` / `evaluation_results_forensicnet.json`. Hardcoding parameter strings across API endpoints, logs, or UI components is strictly prohibited — this caused a real bug resulting in parameter count mismatches between startup logs and API responses (see [[Known Issues & Resolved Bugs]]).
2. **Security Validation Pipeline Enforcement:** Any new model added to the system must implement the exact same security validation pipeline (`validate_file_metadata`, `validate_file_binary_integrity`, magic byte verification, payload limits) as existing models, with zero exceptions.
3. **Strict Class Label Parity:** Both models' class label index mappings must remain strictly synchronized:
   - Index `0` $\rightarrow$ `"AI Generated"` (`fake`)
   - Index `1` $\rightarrow$ `"Real"` (`real`)
4. **Non-In-Place Constraint Enforcement:** Any custom module enforcing filter constraints (such as `BayarConv2d`) must compute constrained weights non-in-place using functional operations during the forward pass. In-place parameter mutation (`param.data[...] = ...`) interferes with PyTorch autograd graph construction and Automatic Mixed Precision (`GradScaler`), causing `NaN` gradient explosions (see [[Known Issues & Resolved Bugs]]).
5. **Mixed Precision Execution Safeguards:** Mathematical operations prone to underflow/overflow in FP16 (such as 2D Discrete Fast Fourier Transforms or min-max tensor normalization) must be explicitly wrapped inside an FP32 execution block (`with torch.autocast(device_type=..., enabled=False):`) with explicit epsilon clamping.

---

## ⚛️ Frontend Rules & Conventions (React / TypeScript)

1. **Strict TypeScript Types:** Define explicit interfaces for component props, API responses, and page states. Avoid `any`.
2. **Design System Adherence:** Consume established tokens from `frontend/src/styles/theme.css`.
   > [!WARNING] Design System Rule
   > "All new UI must use existing tokens. Never introduce new colors, fonts, or panel styles without updating theme.js/theme.css first."
3. **Typography Standards:**
   * Headers (`h1`, `h2`, `h3`): Orbitron font, uppercase, letter-spaced.
   * Terminal Status Readouts: JetBrains Mono font, formatted as `ALL_CAPS_WITH_UNDERSCORES`.
4. **Async Lifecycle Safety:** Wrap API calls in `try/catch/finally` blocks with explicit loading indicator states.

---

## 🚫 Things To Never Do (Anti-Patterns)

* ❌ **Never set `num_workers` arbitrarily high:** Setting DataLoader workers without benchmarking can freeze PyTorch on Linux. Always test with `--benchmark_workers`.
* ❌ **Never rely solely on file extension checks:** Always verify magic bytes (`validate_image_magic_bytes`).
* ❌ **Never write upload binaries to disk:** Process image streams strictly in RAM (`io.BytesIO`).
* ❌ **Never hardcode wildcard CORS (`*`):** Maintain origin restrictions via `ALLOWED_ORIGINS`.
* ❌ **Never mutate weight parameters in-place during forward pass:** Always compute constrained weights non-in-place.
