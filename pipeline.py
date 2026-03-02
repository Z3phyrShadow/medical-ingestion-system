import google.generativeai as genai

from agents.document_understanding import DocumentUnderstandingAgent
from agents.layout_analysis import LayoutAnalysisAgent
from agents.entity_extraction import MedicalEntityExtractionAgent
from agents.normalization import NormalizationValidationAgent


def run_pipeline(file_path: str, model) -> dict:
    """
    Run the full 4-agent medical ingestion pipeline.

    Args:
        file_path: Path to the input file (PDF, image, or text).
        model: A configured google.generativeai GenerativeModel instance.

    Returns:
        A dict with keys:
          - document_understanding
          - layout_analysis
          - entity_extraction
          - normalization_validation
    """
    agent1 = DocumentUnderstandingAgent()
    agent2 = LayoutAnalysisAgent(model)
    agent3 = MedicalEntityExtractionAgent(model)
    agent4 = NormalizationValidationAgent(model)

    print("Running Agent 1: Document Understanding...")
    doc_output = agent1.process(file_path)

    print("Running Agent 2: Layout Analysis...")
    layout_output = agent2.analyze(doc_output)

    print("Running Agent 3: Medical Entity Extraction...")
    entity_output = agent3.extract(layout_output)

    print("Running Agent 4: Normalization & Validation...")
    normalized_output = agent4.normalize(entity_output)

    return {
        "document_understanding": doc_output,
        "layout_analysis": layout_output,
        "entity_extraction": entity_output,
        "normalization_validation": normalized_output,
    }
