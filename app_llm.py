"""
app_llm.py
----------
Streamlit UI for the RAG Document Preparation Toolkit with LLM-powered metadata enrichment (Perplexity API).
Features:
- File/folder upload, chunking, export
- LLM-powered: summary, keywords, topics, section/chapter detection
- Toggle to enable/disable LLM features

References:
- Perplexity API docs: https://docs.perplexity.ai/docs/api-reference
- Model cards: https://docs.perplexity.ai/docs/model-cards
"""
import streamlit as st
from pathlib import Path
import tempfile
from readers.dispatcher import read_file_with_dispatcher
from chunkers.word_chunker import chunk_text_by_words
from utils.markdown_utils import format_chunk_as_markdown
from metadata.metadata_extractor import extract_rich_metadata
import hashlib
from datetime import datetime
import os
import requests
import json
import re
from utils.llm_connector import LLMConnector

# Perplexity API key (user provided)
# PPLX_API_KEY = "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"
PPLX_API_KEY = os.environ.get("PPLX_API_KEY", "")  # Set your Perplexity API key in the environment
PPLX_API_URL = "https://api.perplexity.ai/chat/completions"
# Use the supported model 'sonar' as per latest docs
PPLX_MODEL = "sonar"

st.title("RAG Document Preparation Toolkit (LLM Edition)")

st.markdown("""
Upload your documents (TXT, PDF, DOCX, PPTX), select chunk size, choose import/export folders, and download processed Markdown files with rich, LLM-powered metadata.

**LLM features:** Summaries, topics, keywords, section/chapter detection (via Perplexity API)

*Model used: sonar. See [Perplexity Model Cards](https://docs.perplexity.ai/docs/model-cards) for more.*
""")

chunk_size = st.number_input("Chunk size (words per chunk)", min_value=50, max_value=2000, value=500, step=50)
llm_enabled = st.checkbox("Enable LLM-powered metadata (Perplexity)", value=True)

import_folder = st.text_input("Import folder (optional, for batch processing)", value="")
export_folder = st.text_input("Export folder (optional, for batch processing)", value="")

if 'upload_temp_dir' not in st.session_state:
    st.session_state['upload_temp_dir'] = tempfile.mkdtemp(prefix="rag_upload_")
upload_temp_dir = Path(st.session_state['upload_temp_dir'])

uploaded_files = st.file_uploader("Upload files", type=["txt", "pdf", "docx", "pptx"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = upload_temp_dir / uploaded_file.name
        file_path.write_bytes(uploaded_file.read())

files_to_process = []
if import_folder:
    import_path = Path(import_folder)
    if import_path.exists() and import_path.is_dir():
        files_to_process.extend(list(import_path.glob("*.txt")))
        files_to_process.extend(list(import_path.glob("*.pdf")))
        files_to_process.extend(list(import_path.glob("*.docx")))
        files_to_process.extend(list(import_path.glob("*.pptx")))
    else:
        st.warning("Import folder does not exist or is not a directory.")
files_to_process.extend(list(upload_temp_dir.glob("*.txt")))
files_to_process.extend(list(upload_temp_dir.glob("*.pdf")))
files_to_process.extend(list(upload_temp_dir.glob("*.docx")))
files_to_process.extend(list(upload_temp_dir.glob("*.pptx")))

llm_connector = LLMConnector(api_key=PPLX_API_KEY, model="sonar")

def enrich_metadata_with_llm(chunk, full_text):
    """
    Use LLMConnector to generate summary, keywords, topics, and section/chapter info for the chunk.
    """
    st.info(f"LLM prompt length: {len(chunk)} characters (pre-clean)")
    return llm_connector.enrich_metadata(chunk, full_text)

if st.button("Process"):
    if not files_to_process:
        st.warning("No files to process. Upload files or specify an import folder.")
    else:
        output_files = []
        for file_path in files_to_process:
            text = read_file_with_dispatcher(file_path)
            if not text:
                st.warning(f"Could not read {file_path.name}.")
                continue
            chunks = chunk_text_by_words(text, chunk_size)
            total_chunks = len(chunks)
            for idx, chunk in enumerate(chunks):
                metadata = extract_rich_metadata(file_path, chunk, idx+1, total_chunks, text)
                if llm_enabled:
                    llm_meta = enrich_metadata_with_llm(chunk, text)
                    metadata.update(llm_meta)
                md_content = format_chunk_as_markdown(chunk, metadata)
                out_name = f"{file_path.stem}_chunk{idx+1}.txt"
                output_files.append((out_name, md_content))
                if export_folder:
                    export_path = Path(export_folder)
                    export_path.mkdir(parents=True, exist_ok=True)
                    (export_path / out_name).write_text(md_content, encoding='utf-8')
        st.success(f"Processed {len(output_files)} chunks.")
        for out_name, md_content in output_files:
            st.download_button(
                label=f"Download {out_name}",
                data=md_content,
                file_name=out_name,
                mime="text/plain"
            ) 