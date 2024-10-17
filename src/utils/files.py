import os

from loguru import logger


def get_docs(path: str) -> list:
    pdf_files = [f for f in os.listdir(path) if f.endswith(".pdf")]
    logger.info(f"Found {len(pdf_files)} PDF files for cold start.")
    return pdf_files
