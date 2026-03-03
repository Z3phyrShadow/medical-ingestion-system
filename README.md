# Medical Ingestion System

An agentic pipeline that ingests medical documents (PDFs, scanned images, text files) and extracts structured, normalized data using OCR and LLMs.

## Architecture

```
Input File
    │
    ▼
Agent 1 — Document Understanding   (easyocr / pdfplumber)
    │
    ▼
Agent 2 — Layout Analysis          (Gemini — document type & section splitting)
    │
    ▼
Agent 3 — Medical Entity Extraction (Gemini — patient info, lab results, diagnosis)
    │
    ▼
Agent 4 — Normalization & Validation (Gemini — OCR fixes, unit normalization, flags)
    │
    ▼
Export (CSV / PDF)
```

## Setup

1. **Install dependencies** (using [uv](https://github.com/astral-sh/uv)):
   ```bash
   uv sync
   ```

2. **Set your API key** — copy `.env.example` to `.env` and fill in your key:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

3. **Install Poppler** (required by `pdf2image` for scanned PDF support):
   - **Windows**: Download from [oschwartz10612/poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases), extract, and add the `bin/` folder to your PATH.
   - **macOS**: `brew install poppler`
   - **Linux**: `sudo apt install poppler-utils`

## Usage

```bash
# Print normalized JSON output
python main.py test-samples/test4.pdf

# Export to CSV
python main.py test-samples/test4.pdf --export csv

# Export to PDF
python main.py test-samples/test4.pdf --export pdf

# Export both with a custom output name
python main.py test-samples/test4.pdf --export both --output my_report
```

## Sample Output

Running against a real blood test PDF (`test-samples/test4.pdf`):

```json
{
  "normalized_data": {
    "patient_info": {
      "patient_name": "Mr. DUMMY",
      "age": 25,
      "gender": "Male",
      "date_of_birth": null
    },
    "lab_results": [
      { "test_name": "Hemoglobin",    "value": 15.0,  "unit": "g/dL",   "reference_range": "13.00 - 17.00" },
      { "test_name": "HbA1c",         "value": 10.0,  "unit": "%",      "reference_range": "4.00 - 5.60" },
      { "test_name": "Glucose Fasting","value": 80.0,  "unit": "mg/dL",  "reference_range": "70 - 100" },
      { "test_name": "TSH",            "value": 3.0,   "unit": "µIU/mL", "reference_range": "0.550 - 4.780" },
      { "test_name": "HDL Cholesterol","value": 30.0,  "unit": "mg/dL",  "reference_range": ">40.00" }
    ]
  },
  "validation_flags": [
    "HbA1c value (10.0%) is significantly above reference range (4.00 - 5.60%).",
    "HDL Cholesterol value (30.0 mg/dL) is below reference range (>40.00 mg/dL)."
  ],
  "confidence": 1.0
}
```

## Project Structure

```
medical-ingestion-system/
├── agents/
│   ├── document_understanding.py   # Agent 1 — OCR & text extraction
│   ├── layout_analysis.py          # Agent 2 — document type & section detection
│   ├── entity_extraction.py        # Agent 3 — medical entity extraction
│   └── normalization.py            # Agent 4 — normalization & validation
├── exporters/
│   ├── csv_exporter.py
│   └── pdf_exporter.py
├── pipeline.py                     # Orchestrates all 4 agents
├── main.py                         # CLI entrypoint
├── prototype/                      # Original research notebooks
└── test-samples/                   # Sample input files
```

## Supported Input Formats

| Format | Extraction Method |
|--------|------------------|
| `.pdf` (digital) | pdfplumber |
| `.pdf` (scanned) | pdf2image + easyocr |
| `.png`, `.jpg`, `.jpeg` | easyocr |
| `.txt` | native read |
