---
title: Testing Strategy
tags: [testing, pytest, fixtures, backend-tests, integration]
updated: 2026-07-23
---

# 🧪 Testing Strategy & Test Suite Guide

> [!INFO] Related Documents
> * Back to [[Index|Vault Home]]
> * [[Development Rules]]
> * [[API Specification]]
> * [[Security Guidelines]]

---

## 📋 Test Suite Overview

Backend integration and security unit tests are located in `backend/tests/` and powered by **PyTest** and **FastAPI TestClient**.

---

## 🧰 Reusable Test Fixtures (`backend/tests/conftest.py`)

| Fixture Name | Description | Used For |
| :--- | :--- | :--- |
| `client` | FastAPI TestClient initialized with application instance. | Making HTTP requests in test cases. |
| `valid_jpeg_bytes` | Real 100x100 RGB JPEG binary generated with PIL. | Valid single prediction tests. |
| `valid_png_bytes` | Real 100x100 RGB PNG binary generated with PIL. | Valid single/batch prediction tests. |
| `valid_webp_bytes` | Real 100x100 RGB WEBP binary generated with PIL. | Valid single/batch prediction tests. |
| `invalid_txt_bytes` | Plain text bytes (`b"Plain text payload"`). | Testing magic byte & extension rejection. |
| `oversized_file_bytes` | Dummy byte array exceeding 10MB (> 10,485,760 bytes). | Testing HTTP 413 Payload Too Large limits. |
| `corrupted_image_bytes` | Malformed image headers (`b"\xff\xd8\xff\x00corrupted"`). | Testing PIL decoding error handling. |

---

## 🧪 Comprehensive Test Cases (`backend/tests/test_api.py`)

```python
# Key Test Cases Implemented
1. test_health_endpoint(): Ensures GET /health returns HTTP 200 and operational status.
2. test_predict_valid_jpeg(): Ensures POST /api/v1/predict with JPEG returns 200 and prediction schema.
3. test_predict_valid_png(): Ensures POST /api/v1/predict with PNG returns 200.
4. test_predict_rejects_non_image(): Ensures text file disguised as .jpg triggers 415/422.
5. test_predict_rejects_oversized_file(): Ensures file > 10MB returns 413 Payload Too Large.
6. test_predict_rejects_corrupted_image(): Ensures corrupted bytes return 415/422.
7. test_magic_bytes_validation(): Unit test for validate_image_magic_bytes() across formats.
8. test_inference_service_output_shape(): Unit test verifying predict() return dict structure.
9. test_predict_batch_valid(): Tests batch upload of 3 images returns HTTP 200 array.
10. test_predict_batch_exceeds_max(): Tests batch upload of 11 images triggers HTTP 400.
11. test_predict_batch_partial_success(): Tests batch with 1 corrupted file returns itemized errors.
```

---

## 🏃 Running the PyTest Suite

```bash
# Run all tests with standard output
pytest backend/tests/

# Run with verbose test names and code coverage report
pytest backend/tests/ -v --cov=backend/app
```

> [!SUCCESS] Execution Standard
> All 11 test cases must pass cleanly without warnings before committing changes to main.
