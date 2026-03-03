import json
import logging

logger = logging.getLogger(__name__)


class NormalizationValidationAgent:
    """Agent 4 — Normalizes and validates extracted medical data."""

    def __init__(self, client, model_name: str = "gemini-2.5-flash"):
        self.client = client
        self.model_name = model_name

    def normalize(self, entity_output: dict) -> dict:
        prompt = f"""
You are a medical data normalization and validation system.

Below is extracted medical data that may contain OCR errors,
formatting inconsistencies, and malformed numeric values.

Your job:
1. Fix OCR mistakes (O→0, l→1, etc.) where obvious.
2. Convert numeric fields to proper numbers.
3. Normalize units (e.g., mg/dl → mg/dL, mmol/l → mmol/L).
4. Fix malformed reference ranges.
5. If data is suspicious or unclear, add a validation flag.
6. Identify fields with low confidence due to ambiguity.

Return ONLY valid JSON in this format:

{{
  "normalized_data": {{
    "patient_info": {{
      "patient_name": null,
      "age": null,
      "gender": null,
      "date_of_birth": null
    }},
    "lab_results": [
      {{
        "test_name": "",
        "value": null,
        "unit": "",
        "reference_range": ""
      }}
    ],
    "diagnosis": [],
    "medications": []
  }},
  "validation_flags": [],
  "low_confidence_fields": [],
  "confidence": 0.0
}}

Here is the data to normalize:

{json.dumps(entity_output, indent=2)}
"""

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config={"response_mime_type": "application/json"},
        )

        try:
            return json.loads(response.text)
        except Exception:
            logger.error("Failed to parse Agent 4 response. Raw output:\n%s", response.text)
            raise
