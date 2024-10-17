from loguru import logger
from pdfminer.high_level import extract_text


def load_pdf_to_text(pdf_path: str) -> str:
    """Extract all text from the PDF."""
    text = extract_text(pdf_path)
    if not text:
        raise ValueError(f"No text found in the PDF: {pdf_path}")
    logger.success(f"Loaded text from PDF: {pdf_path}...")
    return text
