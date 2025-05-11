"""
Global configuration for the RAG Document Preparation Toolkit.
Edit this file to set default values for chunk size, output directory, etc.
These can be overridden by the UI or CLI arguments.
"""

# Example configuration variables
DEFAULT_CHUNK_SIZE = 500
DEFAULT_CHUNK_METHOD = 'word'  # Options: word, sentence, paragraph, page, semantic
DEFAULT_OUTPUT_FORMAT = 'txt'  # Options: txt, json, csv
DEFAULT_INPUT_DIR = 'input_files'  # Can be set by user via UI/CLI
DEFAULT_OUTPUT_DIR = 'rag_documents'  # Can be set by user via UI/CLI
# Perplexity API Key (set your key here or override via environment variable)
PPLX_API_KEY = "your-key-here" 