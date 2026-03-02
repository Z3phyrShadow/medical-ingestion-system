import numpy as np
import pdfplumber
from pdf2image import convert_from_path
import easyocr


class DocumentUnderstandingAgent:
    """Agent 1 — Raw text extraction from image, PDF, or text files."""

    def __init__(self):
        self.reader = easyocr.Reader(["en"], gpu=False)

    def detect_file_type(self, file_path: str) -> str:
        ext = file_path.lower().split(".")[-1]
        if ext in ["png", "jpg", "jpeg"]:
            return "image"
        elif ext == "pdf":
            return "pdf"
        elif ext == "txt":
            return "text"
        else:
            raise ValueError(f"Unsupported file type: .{ext}")

    def extract_from_image(self, file_path: str) -> dict:
        result = self.reader.readtext(file_path, detail=0)
        page_text = "\n".join(result)
        return {
            "full_text": page_text,
            "pages": [{"page_number": 1, "text": page_text}],
            "source_type": "image",
            "extraction_method": "easyocr",
        }

    def extract_from_pdf(self, file_path: str) -> dict:
        pages_data = []
        extraction_method = "pdfplumber"

        with pdfplumber.open(file_path) as pdf:
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    pages_data.append({"page_number": i + 1, "text": page_text})

        # Fallback to OCR for scanned PDFs
        if not pages_data:
            extraction_method = "pdf2image + easyocr"
            images = convert_from_path(file_path)
            for i, img in enumerate(images):
                img_np = np.array(img)
                result = self.reader.readtext(img_np, detail=0)
                page_text = "\n".join(result)
                pages_data.append({"page_number": i + 1, "text": page_text})

        full_text = "\n\n".join([p["text"] for p in pages_data])
        return {
            "full_text": full_text,
            "pages": pages_data,
            "source_type": "pdf",
            "extraction_method": extraction_method,
        }

    def extract_from_text(self, file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
        return {
            "full_text": text,
            "pages": [{"page_number": 1, "text": text}],
            "source_type": "text",
            "extraction_method": "native",
        }

    def process(self, file_path: str) -> dict:
        file_type = self.detect_file_type(file_path)
        if file_type == "image":
            return self.extract_from_image(file_path)
        elif file_type == "pdf":
            return self.extract_from_pdf(file_path)
        elif file_type == "text":
            return self.extract_from_text(file_path)
