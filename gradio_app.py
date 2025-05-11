"""
gradio_app.py
-------------
Gradio UI for the RAG Document Preparation Toolkit.
Supports file upload (multiple files), folder upload (as ZIP), chunk size selection, and download of Markdown outputs.
Modern, guided, and user-friendly UI.
"""
import gradio as gr
from pathlib import Path
import tempfile
import zipfile
from readers.dispatcher import read_file_with_dispatcher
from chunkers.word_chunker import chunk_text_by_words
from utils.markdown_utils import format_chunk_as_markdown
from metadata.metadata_extractor import extract_rich_metadata
import shutil
import os
from utils.llm_connector import LLMConnector
from config import PPLX_API_KEY

# Helper to process files and return output files as (filename, content) tuples
def process_files(files, chunk_size, llm_enabled=False, llm_connector=None):
    output_files = []
    for file_path in files:
        text = read_file_with_dispatcher(Path(file_path))
        if not text:
            continue
        chunks = chunk_text_by_words(text, chunk_size)
        total_chunks = len(chunks)
        for idx, chunk in enumerate(chunks):
            metadata = extract_rich_metadata(Path(file_path), chunk, idx+1, total_chunks, text)
            if llm_enabled and llm_connector:
                llm_meta = llm_connector.enrich_metadata(chunk, text)
                metadata.update(llm_meta)
            md_content = format_chunk_as_markdown(chunk, metadata)
            out_name = f"{Path(file_path).stem}_chunk{idx+1}.txt"
            output_files.append((out_name, md_content))
    return output_files

# Main Gradio function
def rag_pipeline(upload_method, file_upload, folder_zip, chunk_size, llm_enabled):
    temp_dir = tempfile.mkdtemp(prefix="rag_gradio_")
    files_to_process = []
    # Handle file uploads (support both file-like and NamedString)
    if upload_method == "Files" and file_upload:
        for f in file_upload:
            if hasattr(f, 'read'):
                dest = Path(temp_dir) / Path(getattr(f, 'name', 'uploaded_file')).name
                with open(dest, "wb") as out_f:
                    out_f.write(f.read())
                files_to_process.append(str(dest))
            elif hasattr(f, 'name') and os.path.exists(f.name):
                # It's a NamedString or similar with a .name attribute
                dest = Path(temp_dir) / Path(f.name).name
                shutil.copy(f.name, dest)
                files_to_process.append(str(dest))
    # Handle folder upload as ZIP
    if upload_method == "Folder as ZIP" and folder_zip:
        if hasattr(folder_zip, 'read'):
            zip_path = Path(temp_dir) / "uploaded_folder.zip"
            with open(zip_path, "wb") as zf:
                zf.write(folder_zip.read())
        elif hasattr(folder_zip, 'name') and os.path.exists(folder_zip.name):
            zip_path = Path(temp_dir) / "uploaded_folder.zip"
            shutil.copy(folder_zip.name, zip_path)
        else:
            zip_path = None
        if zip_path and zip_path.exists():
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            for ext in [".txt", ".pdf", ".docx", ".pptx"]:
                files_to_process.extend([str(p) for p in Path(temp_dir).rglob(f"*{ext}")])
    # Process files
    llm_connector = LLMConnector(api_key=PPLX_API_KEY, model="sonar") if llm_enabled else None
    output_files = process_files(files_to_process, chunk_size, llm_enabled, llm_connector)
    # Prepare for download: create a ZIP of all outputs
    output_zip_path = Path(temp_dir) / "rag_outputs.zip"
    with zipfile.ZipFile(output_zip_path, 'w') as zipf:
        for fname, content in output_files:
            file_path = Path(temp_dir) / fname
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            zipf.write(file_path, arcname=fname)
    # Return download link for ZIP and individual files
    download_links = [(fname, content) for fname, content in output_files]
    return output_zip_path, download_links

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 📄 RAG Document Preparation Toolkit
    
    **Prepare, chunk, and annotate your documents for RAG databases.**
    
    ---
    
    **Step 1:** Choose your input method (upload files or a folder as ZIP)
    
    **Step 2:** Select or upload your documents
    
    **Step 3:** Set your chunk size (words per chunk)
    
    **Step 4:** Click **Process** to start
    
    **Step 5:** Download your processed Markdown files (as ZIP or individually)
    
    ---
    """)
    upload_method = gr.Radio(["Files", "Folder as ZIP"], value="Files", label="Select upload method")
    file_upload = gr.File(label="Upload one or more files (TXT, PDF, DOCX, PPTX)", file_count="multiple", file_types=[".txt", ".pdf", ".docx", ".pptx"])
    folder_zip = gr.File(label="Upload a folder as ZIP (all supported files inside)", file_types=[".zip"])
    chunk_size = gr.Number(label="Chunk size (words per chunk)", value=500, precision=0, info="How many words per chunk?")
    llm_enabled = gr.Checkbox(label="Enable LLM-powered metadata (if configured)", value=False)
    process_btn = gr.Button("🚀 Process Documents", elem_id="process-btn")
    output_zip = gr.File(label="⬇️ Download all as ZIP")
    output_files = gr.Files(label="⬇️ Download individual files")

    # Show/hide uploaders based on method
    def toggle_uploaders(method):
        return gr.update(visible=method=="Files"), gr.update(visible=method=="Folder as ZIP")
    upload_method.change(toggle_uploaders, inputs=upload_method, outputs=[file_upload, folder_zip])

    def on_process(upload_method, file_upload, folder_zip, chunk_size, llm_enabled):
        zip_path, download_links = rag_pipeline(upload_method, file_upload, folder_zip, int(chunk_size), llm_enabled)
        file_paths = []
        for fname, content in download_links:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=fname)
            temp_file.write(content.encode("utf-8"))
            temp_file.close()
            file_paths.append(temp_file.name)
        return zip_path, file_paths

    process_btn.click(on_process, inputs=[upload_method, file_upload, folder_zip, chunk_size, llm_enabled], outputs=[output_zip, output_files])

demo.launch() 