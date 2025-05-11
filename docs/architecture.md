# Architecture Overview

## Modular Structure

- **readers/**: Extract text from various file formats (PDF, DOCX, PPTX, MSG, TXT).
- **chunkers/**: Split extracted text into chunks (by word, sentence, paragraph, page, or semantic boundary).
- **metadata/**: Extract and enrich metadata for each chunk (file info, LLM-generated tags, user annotations).
- **output/**: Write processed chunks and metadata to output files (TXT, JSON, CSV).
- **utils/**: Utility functions for hashing, logging, etc.
- **app.py**: UI entry point (Streamlit/Gradio).
- **main.py**: CLI entry point.

## Data Flow
1. **File Ingestion**: User uploads or selects files.
2. **Text Extraction**: Appropriate reader extracts text.
3. **Chunking**: Text is split into chunks using selected strategy.
4. **Metadata Enrichment**: Metadata is attached to each chunk (optionally using LLMs).
5. **Output**: Chunks and metadata are written to output files for RAG ingestion. 