"""
pdf_reader.py
-------------
Module for extracting text from PDF files using pdfminer.six.
"""
from pathlib import Path
from typing import Optional
from pdfminer.high_level import extract_text

def extract_text_from_pdf(file_path: Path) -> Optional[str]:
    """
    Extracts text from a PDF file using pdfminer.six.

    Args:
        file_path (Path): Path to the PDF file.

    Returns:
        Optional[str]: Extracted text, or None if extraction fails.
    """
    try:
        return extract_text(str(file_path))
    except Exception as e:
        print(f"Error extracting text from PDF {file_path}: {e}")
        return None 