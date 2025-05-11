"""
dispatcher.py
-------------
Dispatches file reading to the appropriate reader based on file extension.
"""
from pathlib import Path
from typing import Optional
from readers.txt_reader import read_txt_file
from readers.pdf_reader import extract_text_from_pdf
from readers.docx_reader import extract_text_from_docx
from readers.pptx_reader import extract_text_from_pptx
# from readers.msg_reader import extract_text_from_msg  # Uncomment when implemented

def read_file_with_dispatcher(file_path: Path) -> Optional[str]:
    """
    Reads a file using the appropriate reader based on its extension.

    Args:
        file_path (Path): Path to the input file.

    Returns:
        Optional[str]: Extracted text, or None if unsupported or error.
    """
    ext = file_path.suffix.lower()
    if ext == '.txt':
        return read_txt_file(file_path)
    elif ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.pptx':
        return extract_text_from_pptx(file_path)
    # elif ext == '.msg':
    #     return extract_text_from_msg(file_path)
    else:
        print(f"Unsupported file type: {file_path}")
        return None 