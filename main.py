"""
Medical Ingestion System — CLI entrypoint

Usage:
    python main.py <file_path> [--export csv|pdf|both] [--output <base_name>]

Examples:
    python main.py test-samples/test4.pdf
    python main.py test-samples/test4.pdf --export both --output my_report
    python main.py test-samples/test2.png --export csv
"""

import argparse
import json
import logging
import os
import sys

from dotenv import load_dotenv
from google import genai

from pipeline import run_pipeline
from exporters.csv_exporter import export_to_csv
from exporters.pdf_exporter import export_to_pdf

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    load_dotenv()

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        logger.error("GOOGLE_API_KEY not found. Add it to your .env file.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(
        description="Medical document ingestion pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("file_path", help="Path to the input file (PDF, PNG, JPG, or TXT)")
    parser.add_argument(
        "--export",
        choices=["csv", "pdf", "both"],
        default=None,
        help="Export format. Omit to only print the normalized output.",
    )
    parser.add_argument(
        "--output",
        default="medical_output",
        help="Base filename for exports (without extension). Default: medical_output",
    )
    args = parser.parse_args()

    if not os.path.exists(args.file_path):
        logger.error("Input file not found: %s", args.file_path)
        sys.exit(1)

    result = run_pipeline(args.file_path, client)
    normalized_output = result["normalization_validation"]

    logger.info("Pipeline complete.")

    if args.export in ("csv", "both"):
        export_to_csv(normalized_output, filename=f"{args.output}.csv")

    if args.export in ("pdf", "both"):
        export_to_pdf(normalized_output, filename=f"{args.output}.pdf")

    if args.export is None:
        print(json.dumps(normalized_output, indent=2))


if __name__ == "__main__":
    main()
