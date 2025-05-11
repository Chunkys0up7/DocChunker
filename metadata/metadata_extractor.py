"""
metadata_extractor.py
---------------------
Extracts rich metadata from files and text chunks, including file properties, headings, and topics.
"""
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime
import hashlib
import re

# For future: import and use LLMs for topic/summary/keywords

def extract_rich_metadata(file_path: Path, chunk: str, chunk_number: int, total_chunks: int, full_text: Optional[str] = None) -> Dict:
    """
    Extracts rich metadata for a text chunk, including file info, headings, and basic topic/section detection.

    Args:
        file_path (Path): Path to the source file.
        chunk (str): The text content of the chunk.
        chunk_number (int): The chunk's position in the document.
        total_chunks (int): Total number of chunks for the document.
        full_text (Optional[str]): The full text of the document (for context).

    Returns:
        Dict: Metadata dictionary.
    """
    stats = file_path.stat()
    metadata = {
        # 'source_path': str(file_path),  # Removed as per user request
        'file_hash': hashlib.md5(file_path.read_bytes()).hexdigest(),
        'original_size': stats.st_size,
        'created_date': datetime.fromtimestamp(stats.st_ctime).isoformat(),
        'modified_date': datetime.fromtimestamp(stats.st_mtime).isoformat(),
        'processing_time': datetime.now().isoformat(),
        'chunk_number': chunk_number,
        'total_chunks': total_chunks,
        'word_count': len(chunk.split()),
    }
    # Attempt to extract a heading/section from the chunk (simple heuristic)
    heading = extract_heading(chunk)
    if heading:
        metadata['section_heading'] = heading
    # Attempt to extract a topic/keywords (simple heuristic)
    keywords = extract_keywords(chunk)
    if keywords:
        metadata['keywords'] = keywords
    # Optionally, add first/last line as context
    lines = [line.strip() for line in chunk.splitlines() if line.strip()]
    if lines:
        metadata['first_line'] = lines[0]
        metadata['last_line'] = lines[-1]
    return metadata

def extract_heading(text: str) -> Optional[str]:
    """
    Attempts to extract a heading or section title from the start of the text chunk.
    """
    # Simple heuristic: first line in ALL CAPS or Title Case
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return None
    first_line = lines[0]
    if first_line.isupper() or re.match(r'^[A-Z][a-z]+( [A-Z][a-z]+)*$', first_line):
        return first_line
    return None

def extract_keywords(text: str, max_keywords: int = 5) -> Optional[str]:
    """
    Extracts keywords from the chunk using a simple frequency-based approach.
    """
    words = re.findall(r'\b\w{5,}\b', text.lower())  # words with 5+ letters
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    sorted_words = sorted(freq, key=freq.get, reverse=True)
    if sorted_words:
        return ', '.join(sorted_words[:max_keywords])
    return None 