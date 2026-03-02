import json


class LayoutAnalysisAgent:
    """Agent 2 — Identifies document type and splits into logical sections."""

    def __init__(self, model):
        self.model = model

    def analyze(self, doc_output: dict) -> dict:
        full_text = doc_output["full_text"]

        prompt = f"""
You are a medical document layout analyzer.

Given the raw medical document text below:

---
{full_text}
---

Your task:
1. Identify the document type (blood_test_report, prescription, discharge_summary, imaging_report, unknown).
2. Split the document into logical sections.
3. For each section return:
   - section_name (snake_case)
   - content (exact extracted text)
   - confidence (0 to 1)

Return ONLY valid JSON in this format:

{{
  "document_type": "...",
  "sections": [
    {{
      "section_name": "...",
      "content": "...",
      "confidence": 0.0
    }}
  ]
}}
"""

        response = self.model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"},
        )

        try:
            return json.loads(response.text)
        except Exception:
            print("Raw model output:")
            print(response.text)
            raise
