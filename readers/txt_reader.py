"""
txt_reader.py
--------------
Module for reading plain text (.txt) files with robust encoding handling.
"""
from pathlib import Path
from typing import Optional


def read_txt_file(file_path: Path) -> Optional[str]:
    """
    Reads the contents of a .txt file, handling encoding issues with fallbacks.

    Args:
        file_path (Path): Path to the .txt file.

    Returns:
        Optional[str]: The file contents as a string, or None if reading fails.
    """
    try:
        # Try UTF-8 first
        return file_path.read_text(encoding='utf-8')
    except UnicodeDecodeError:
        try:
            # Fallback to latin-1
            return file_path.read_text(encoding='latin-1')
        except Exception as e:
            print(f"Encoding error in {file_path}: {str(e)}")
            return None 