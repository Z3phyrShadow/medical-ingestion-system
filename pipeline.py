import logging

from agents.document_understanding import DocumentUnderstandingAgent
from agents.layout_analysis import LayoutAnalysisAgent
from agents.entity_extraction import MedicalEntityExtractionAgent
from agents.normalization import NormalizationValidationAgent

logger = logging.getLogger(__name__)


def run_pipeline(file_path: str, client, model_name: str = "gemini-2.5-flash") -> dict:
    """
    Run the full 4-agent medical ingestion pipeline.

    Args:
        file_path:   Path to the input file (PDF, image, or text).
        client:      A configured google.genai.Client instance.
        model_name:  Gemini model to use for LLM agents.

    Returns:
        A dict with keys:
          - document_understanding
          - layout_analysis
          - entity_extraction
          - normalization_validation
    """
    agent1 = DocumentUnderstandingAgent()
    agent2 = LayoutAnalysisAgent(client, model_name)
    agent3 = MedicalEntityExtractionAgent(client, model_name)
    agent4 = NormalizationValidationAgent(client, model_name)

    try:
        logger.info("Agent 1: Document Understanding...")
        doc_output = agent1.process(file_path)
    except Exception as e:
        raise RuntimeError(f"Agent 1 (Document Understanding) failed: {e}") from e

    try:
        logger.info("Agent 2: Layout Analysis...")
        layout_output = agent2.analyze(doc_output)
    except Exception as e:
        raise RuntimeError(f"Agent 2 (Layout Analysis) failed: {e}") from e

    try:
        logger.info("Agent 3: Medical Entity Extraction...")
        entity_output = agent3.extract(layout_output)
    except Exception as e:
        raise RuntimeError(f"Agent 3 (Entity Extraction) failed: {e}") from e

    try:
        logger.info("Agent 4: Normalization & Validation...")
        normalized_output = agent4.normalize(entity_output)
    except Exception as e:
        raise RuntimeError(f"Agent 4 (Normalization) failed: {e}") from e

    return {
        "document_understanding": doc_output,
        "layout_analysis": layout_output,
        "entity_extraction": entity_output,
        "normalization_validation": normalized_output,
    }
