"""
app.py
------
Streamlit UI for the RAG Document Preparation Toolkit.
Allows users to upload files, select chunk size, choose import/export folders, and download Markdown outputs.
Files are only processed when the user clicks the 'Process' button. Uploaded files are stored in a persistent temp directory for the session.
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
from utils.llm_connector import LLMConnector

st.title("RAG Document Preparation Toolkit")

st.markdown("""
Upload your documents (TXT, PDF, DOCX, PPTX), select chunk size, choose import/export folders, and download processed Markdown files with metadata.

**Tip:** For batch processing, paste the full path to your import/export folders below. For uploads, files are stored in a temporary directory until you click 'Process'.
""")

chunk_size = st.number_input("Chunk size (words per chunk)", min_value=50, max_value=2000, value=500, step=50)

# Folder selection (user can type or paste path)
import_folder = st.text_input("Import folder (optional, for batch processing)", value="")
export_folder = st.text_input("Export folder (optional, for batch processing)", value="")

# Persistent temp directory for the session
if 'upload_temp_dir' not in st.session_state:
    st.session_state['upload_temp_dir'] = tempfile.mkdtemp(prefix="rag_upload_")
upload_temp_dir = Path(st.session_state['upload_temp_dir'])

uploaded_files = st.file_uploader("Upload files", type=["txt", "pdf", "docx", "pptx"], accept_multiple_files=True)

# Save uploaded files to persistent temp dir
if uploaded_files:
    for uploaded_file in uploaded_files:
        file_path = upload_temp_dir / uploaded_file.name
        file_path.write_bytes(uploaded_file.read())

# Gather files to process
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
# Add uploaded files from temp dir
files_to_process.extend(list(upload_temp_dir.glob("*.txt")))
files_to_process.extend(list(upload_temp_dir.glob("*.pdf")))
files_to_process.extend(list(upload_temp_dir.glob("*.docx")))
files_to_process.extend(list(upload_temp_dir.glob("*.pptx")))

llm_enabled = st.checkbox("Enable LLM-powered metadata (if configured)", value=False)
PPLX_API_KEY = "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"  # Or load from config/env
llm_connector = LLMConnector(api_key=PPLX_API_KEY, model="sonar")

# Add a 'Process' button
if st.button("Process"):
    if not files_to_process:
        st.warning("No files to process. Upload files or specify an import folder.")
    else:
        output_files = []
        for file_path in files_to_process:
            try:
                text = read_file_with_dispatcher(file_path)
                if not text:
                    st.error(f"Could not read {file_path.name}. Unsupported format or extraction error.")
                    continue
                try:
                    chunks = chunk_text_by_words(text, chunk_size)
                except Exception as e:
                    st.error(f"Chunking failed for {file_path.name}: {e}")
                    continue
                total_chunks = len(chunks)
                for idx, chunk in enumerate(chunks):
                    try:
                        metadata = extract_rich_metadata(file_path, chunk, idx+1, total_chunks, text)
                        if llm_enabled:
                            st.info(f"LLM prompt length: {len(chunk)} characters (pre-clean)")
                            llm_meta = llm_connector.enrich_metadata(chunk, text)
                            metadata.update(llm_meta)
                        md_content = format_chunk_as_markdown(chunk, metadata)
                        out_name = f"{file_path.stem}_chunk{idx+1}.txt"
                        output_files.append((out_name, md_content))
                        if export_folder:
                            export_path = Path(export_folder)
                            export_path.mkdir(parents=True, exist_ok=True)
                            (export_path / out_name).write_text(md_content, encoding='utf-8')
                    except Exception as e:
                        st.error(f"Metadata or output failed for {file_path.name} chunk {idx+1}: {e}")
            except Exception as e:
                st.error(f"Failed to process {file_path.name}: {e}")
        if output_files:
            st.success(f"Processed {len(output_files)} chunks.")
            for out_name, md_content in output_files:
                st.download_button(
                    label=f"Download {out_name}",
                    data=md_content,
                    file_name=out_name,
                    mime="text/plain"
                )
        else:
            st.warning("No files were successfully processed.") 