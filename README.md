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

2. **Set your API key** — create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_key_here
   ```

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
