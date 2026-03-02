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
import os

import google.generativeai as genai
from dotenv import load_dotenv

from pipeline import run_pipeline
from exporters.csv_exporter import export_to_csv
from exporters.pdf_exporter import export_to_pdf


def main():
    load_dotenv()

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY not found. Add it to your .env file.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")

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
        raise FileNotFoundError(f"Input file not found: {args.file_path}")

    result = run_pipeline(args.file_path, model)
    normalized_output = result["normalization_validation"]

    print("\n--- PIPELINE COMPLETE ---")

    if args.export in ("csv", "both"):
        export_to_csv(normalized_output, filename=f"{args.output}.csv")

    if args.export in ("pdf", "both"):
        export_to_pdf(normalized_output, filename=f"{args.output}.pdf")

    if args.export is None:
        import json
        print(json.dumps(normalized_output, indent=2))


if __name__ == "__main__":
    main()
