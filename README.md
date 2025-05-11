# RAG Document Preparation Toolkit

A Python toolkt for preparing, chunking, and annotating documents for ingestion into Retrieval-Augmented Generation (RAG) systems. Supports multiple file types, rich metadata, customizable chunking, and optional LLM-powered classification and metadata generation. Includes a user-friendly UI for configuration and preview.

## Featuresi
- Multi-format support: PDF, DOCX, PPTX, MSG, TXT
- Flexible chunking: By word, sentence, paragraph, page, or semantic boundary
- Rich metadata: Source info, file hash, chunk position, LLM-generated tags
- UI: Simple web interface for upload, config, and preview
- Extensible: Modular codebase for easy feature addition

## Installation
```bash
git clone <repo-url>
cd rag_document_prep
pip install -r requirements.txt
```

## Usage (CLI)
```bash
python main.py --source input_files --output rag_documents --chunk-size 500 --chunk-method word
```

## Usage (UI)
```bash
streamlit run app.py
```

## Configuration Options
- `--chunk-size`: Number of words/sentences/paragraphs per chunk
- `--chunk-method`: word | sentence | paragraph | page | semantic
- `--llm-metadata`: Enable LLM-based metadata generation
- `--output-format`: txt | json | csv

## Metadata Fields
- `source_path`
- `file_hash`
- `original_size`
- `created_date`
- `modified_date`
- `processing_time`
- `chunk_number`
- `total_chunks`
- `word_count`
- `document_type` (LLM)
- `summary` (LLM)
- `keywords` (LLM)
- `user_tags`

## Extending the Toolkit
- Add new file readers in `readers/`
- Add new chunking strategies in `chunkers/`
- Add new metadata enrichers in `metadata/`
- Add new UI features in `app.py`

## Contributing
- Please annotate all code with clear docstrings and comments.
- Add usage examples and tests for new features.
- See `CONTRIBUTING.md` for guidelines.

## License
MIT 