**Project Title:** Flask‑MVC PDF Embed/Extract API

**Objective:**  
Define a Flask‑based web application (MVC pattern) that exposes two binary‑PDF endpoints and ships with interactive Swagger documentation. All PDF data must be handled in‑memory (no filesystem I/O).

---

## 1. High‑Level Description

You are building a microservice that allows clients to embed multiple PDF documents inside a host PDF, and to extract all embedded PDFs from such a document. The service must:

- Accept and return raw PDF bytes (binary streams).
- Never write intermediate files to disk.
- Provide a clean MVC architecture to separate concerns.
- Offer a live Swagger UI for easy testing and integration.

---

## 2. Functional Requirements

1. **Endpoint: `/api/pdf/create_embedded_pdf`**  
   - **Method:** POST  
   - **Inputs (multipart/form‑data):**  
     - `host_pdf` (binary): the “carrier” PDF  
     - `attachments[]` (binary array): one or more PDFs to embed  
   - **Output:**  
     - HTTP 200 with response body = merged PDF (binary)

2. **Endpoint: `/api/pdf/extract_embedded_pdf`**  
   - **Method:** POST  
   - **Input (multipart/form‑data):**  
     - `pdf` (binary): a PDF potentially containing embedded files  
   - **Output:**  
     - JSON object listing each extracted PDF as a base‑64 or hex string, plus a count  

---

## 3. Non‑Functional Requirements

- **In‑Memory Processing:** All PDF manipulation must use streams (e.g. `io.BytesIO`), no temp files.  
- **Modularity:** Follow MVC:  
  - **Models:** (if needed for future extension)  
  - **Views/Controllers:** define routes and request/response handling  
  - **Services:** implement PDF embed & extract logic  
  - **Config:** centralized settings (including Swagger)  
- **Documentation:** Swagger UI automatically generated from YAML or docstring annotations.  
- **Testing:** Unit tests to verify that embedding followed by extraction returns the original attachments.  

---

## 4. Technology Stack

- **Language & Framework:** Python 3.x, Flask  
- **PDF Library:** PyPDF2 (or equivalent with attachment support)  
- **API Docs:** Flasgger (Swagger‑UI)  
- **Validation (optional):** Marshmallow schemas  
- **Testing:** pytest  

---

## 5. Suggested Folder Structure

```

app/
├── config.py             # app & Swagger settings
├── controllers/          # Flask blueprints for PDF endpoints
├── services/             # PDF‑manipulation logic (embed/extract)
├── schemas/              # request/response definitions (optional)
├── models/               # domain models (empty placeholder)
└── **init**.py           # application factory
tests/                    # pytest units for services + endpoints
run.py                    # entry‑point script
requirements.txt          # dependencies

```

---

## 6. Deliverables for Code‑Gen AI

When you feed this prompt into your code generation tool, expect it to scaffold:

- `app/config.py` with Swagger configuration  
- A PDF service module with two functions: `embed_pdfs(bytes, List[bytes]) → bytes` and `extract_pdfs(bytes) → List[bytes]`  
- A Flask blueprint for the two endpoints, handling binary I/O and invoking the service  
- Auto‑wired Swagger definitions for each endpoint (inputs, outputs, examples)  
- A `run.py` to launch the app  
- A `requirements.txt` listing Flask, PyPDF2, flasgger, (and optionally marshmallow)  
- A basic pytest suite that asserts round‑trip embed→extract correctness  

---

## 7. Usage Example (for Swagger UI)

1. Open Swagger UI at `/apidocs`.  
2. Upload a host PDF and multiple attachments to **create_embedded_pdf**; download the result.  
3. Upload that result to **extract_embedded_pdf**; inspect returned embedded files.  
