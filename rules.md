# Development Rules & Conventions — AI Image Detector

## 1. Code Style Conventions
* **Python Backend:**
  * PEP 8 compliance with 4-space indentation and explicit type hinting (`Optional`, `Dict`, `List`, `Tuple`).
  * Functions must include clear docstrings explaining arguments, return values, and failure modes.
  * Logging must be handled via the standard `logging` module using structured formatters (`%(asctime)s [%(levelname)s] %(name)s: %(message)s`). Never use raw `print()` statements in API routes.
  * Exception handling must catch specific exceptions (e.g. `PIL.UnidentifiedImageError`, `ValueError`, `HTTPException`) and wrap unhandled runtime failures in generic HTTP 500 error responses to sanitize output.
* **TypeScript Frontend:**
  * Explicit React functional components with `React.FC<Props>` signature typing.
  * Strong typing on API payloads and props; avoid `any` wherever possible.
  * Async/await API calls inside `try/catch/finally` blocks with explicit UI loading/error state management.

---

## 2. Frontend Design System Rules
All new UI components must strictly adhere to the established cyberpunk terminal design system documented in `frontend/src/styles/theme.css`.

* **Design System Strict Policy:**
  > "All new UI must use these existing tokens. Never introduce new colors, fonts, or panel styles without updating theme.js / theme.css first."

* **Token & Style Mapping:**
  * **Color Palette Tokens:**
    * Base Void Background: `#0b0c10` (`var(--bg-color)`)
    * Primary Cyan Glow: `#66fcf1` (`var(--primary-cyan)`)
    * Secondary Dim Teal: `#45a29e` (`var(--secondary-cyan)`)
    * Success / Real Glow: `#2ecc40` / `#00ffcc` (`var(--accent-green)`)
    * Error / AI Generated Glow: `#ff4136` / `#ff3366` (`var(--accent-red)`)
    * Text Colors: Muted `#c5c6c7` (`var(--text-grey)`), Title `#ffffff` (`var(--text-white)`)
  * **Typography Rules:**
    * Headers (`h1`, `h2`, `h3`): Orbitron font (`var(--display-font)`), uppercase, letter-spaced.
    * Status Labels & Readouts: JetBrains Mono font (`var(--terminal-font)`), strictly formatted as `ALL_CAPS_WITH_UNDERSCORES` (e.g., `SYSTEM_READY`, `ANALYSIS_COMPLETE`).
    * Terminal Logs & Code: JetBrains Mono (`var(--terminal-font)`).
  * **Borders & Panels:**
    * 3D Glassmorphic Panels: `rgba(11, 12, 16, 0.7)` with `1px solid rgba(102, 252, 241, 0.2)` borders.
    * Sharp corners (`0px` border radius) for tactical sidebars, `8px` for main container panels.

---

## 3. Backend Rules
* **File Validation Pipeline:** Every endpoint receiving image files must execute the mandatory multi-stage validation sequence:
  1. `validate_file_metadata()`: Verify extension (`.jpg`, `.jpeg`, `.png`, `.webp`) and MIME content type.
  2. Size Limit Check: Enforce maximum payload size (10MB for single, 110MB for batch).
  3. `validate_image_magic_bytes()`: Verify binary signatures.
  4. `Image.open().verify()`: Confirm PIL decoding validity.
* **Rate Limiting:** Every endpoint accepting file payloads must apply the sliding-window rate limiter per client IP address.
* **Error Sanitization:** Never expose internal Python stack traces or low-level exception messages in API HTTP responses. Return concise JSON messages (e.g., `{"detail": "An error occurred while processing the image."}`).
* **Model State Safety:** Check `is_model_loaded()` before processing any inference request and return HTTP 503 if unavailable.

---

## 4. Model & ML Rules
* **Class Mapping Consistency:** The binary class mapping index **must remain strictly synchronized** across all training, dataset processing, and inference services:
  * `0`: `AI Generated` (`fake` / `ai_generated`)
  * `1`: `Real` (`real`)
* **Preprocessing Pipeline:** Inference code must use the exact transform pipeline used during validation:
  `Resize(256) -> CenterCrop(224) -> ToTensor() -> Normalize(IMAGENET_MEAN, IMAGENET_STD)`
* **Evaluation Requirement:** Any modification to dataset composition, unfreezing strategy, or hyperparameters requires running `backend/ml/evaluate.py` to regenerate `evaluation_results.json` before committing model updates.

---

## 5. Testing Requirements
* **Backend Integration Tests:** All new API endpoints or modified route handlers require corresponding test coverage in `backend/tests/test_api.py`.
* **Fixture Conventions:** Use established PyTest fixtures (`client`, `valid_jpeg_bytes`, `valid_png_bytes`, `invalid_txt_bytes`, `oversized_file_bytes`, `corrupted_image_bytes`) defined in `backend/tests/conftest.py`.
* **Execution Verification:** Run pytest before declaring task completion:
  ```bash
  pytest backend/tests/
  ```

---

## 6. Things To Never Do (Anti-Patterns)
* **Never assume high `num_workers` is safe without benchmarking:** Setting DataLoader `num_workers > 2` can cause PyTorch shared memory crashes or process deadlocks depending on the host OS. Always run `--benchmark_workers` if tuning.
* **Never bypass binary magic byte checks:** Relying solely on `UploadFile.content_type` or file extensions allows extension-spoofing security vulnerabilities.
* **Never write user uploads to persistent disk:** Image classification must occur entirely in-memory using `io.BytesIO` streams to maintain privacy and zero user data retention guarantees.
* **Never hardcode direct wildcard CORS origins (`*`) in production:** CORS origins must be configured through `ALLOWED_ORIGINS` environment variables.
