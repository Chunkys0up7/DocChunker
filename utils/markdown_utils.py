"""
markdown_utils.py
-----------------
Utility for formatting text chunks and metadata as Markdown with YAML frontmatter.
"""
from typing import Dict
import yaml

def format_chunk_as_markdown(chunk: str, metadata: Dict) -> str:
    """
    Formats a text chunk and its metadata as Markdown with YAML frontmatter.

    Args:
        chunk (str): The text content of the chunk.
        metadata (Dict): Metadata dictionary to include in the frontmatter.

    Returns:
        str: Markdown-formatted string with metadata and chunk content.
    """
    # Use YAML for metadata frontmatter
    yaml_frontmatter = yaml.dump(metadata, sort_keys=False, allow_unicode=True)
    return f"---\n{yaml_frontmatter}---\n\n{chunk}\n" 