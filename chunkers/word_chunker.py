"""
word_chunker.py
--------------
Module for splitting text into chunks by word count.
"""
import re
from typing import List

def chunk_text_by_words(text: str, chunk_size: int) -> List[str]:
    """
    Splits text into chunks, each containing up to chunk_size words.

    Args:
        text (str): The input text to be chunked.
        chunk_size (int): Number of words per chunk.

    Returns:
        List[str]: List of text chunks.
    """
    # Use regex to split text into words, preserving whitespace
    words = re.findall(r'\S+\s*', text)
    # Create chunks by joining words
    chunks = [''.join(words[i:i+chunk_size]).strip()
              for i in range(0, len(words), chunk_size)]
    return chunks 