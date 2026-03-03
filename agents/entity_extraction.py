import json
import logging

logger = logging.getLogger(__name__)


class MedicalEntityExtractionAgent:
    """Agent 3 — Extracts structured medical entities from layout sections."""

    def __init__(self, client, model_name: str = "gemini-2.5-flash"):
        self.client = client
        self.model_name = model_name

    def extract(self, layout_output: dict) -> dict:
        document_type = layout_output["document_type"]
        sections = layout_output["sections"]

        sections_text = ""
        for section in sections:
            sections_text += f"\n\nSECTION: {section['section_name']}\n"
            sections_text += section["content"]

        prompt = f"""
You are a medical entity extraction system.

Document type: {document_type}

Below are structured sections of a medical document.

{sections_text}

Extract structured medical information in JSON format.

Rules:
- Do NOT hallucinate.
- If information is missing, use null or empty list.
- Keep lab_results as a list of objects with:
  test_name, value, unit, reference_range
- Keep diagnosis and medications as lists.
- Extract patient_info fields if available:
  patient_name, age, gender, date_of_birth

Return ONLY valid JSON:

{{
  "patient_info": {{
    "patient_name": null,
    "age": null,
    "gender": null,
    "date_of_birth": null
  }},
  "lab_results": [],
  "diagnosis": [],
  "medications": [],
  "confidence": 0.0
}}
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )

        try:
            return json.loads(response.text)
        except Exception:
            logger.error("Failed to parse Agent 3 response. Raw output:\n%s", response.text)
            raise
