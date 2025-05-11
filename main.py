"""
main.py
-------
CLI entry point for the RAG Document Preparation Toolkit.
Processes any supported file type, chunks content, and outputs Markdown with metadata.
"""
import argparse
from pathlib import Path
from datetime import datetime
from readers.dispatcher import read_file_with_dispatcher
from chunkers.word_chunker import chunk_text_by_words
from utils.markdown_utils import format_chunk_as_markdown
import config
import hashlib


def generate_metadata(file_path: Path, chunk_number: int, total_chunks: int, chunk: str) -> dict:
    """
    Generate metadata for a chunk.
    """
    stats = file_path.stat()
    return {
        'source_path': str(file_path),
        'file_hash': hashlib.md5(file_path.read_bytes()).hexdigest(),
        'original_size': stats.st_size,
        'created_date': datetime.fromtimestamp(stats.st_ctime).isoformat(),
        'modified_date': datetime.fromtimestamp(stats.st_mtime).isoformat(),
        'processing_time': datetime.now().isoformat(),
        'chunk_number': chunk_number,
        'total_chunks': total_chunks,
        'word_count': len(chunk.split()),
    }

def main():
    """
    Main function to orchestrate reading, chunking, and Markdown output for any supported file type.
    """
    parser = argparse.ArgumentParser(description="RAG Document Preparation Toolkit")
    parser.add_argument('--input', type=str, default=config.DEFAULT_INPUT_DIR, help='Input folder containing files')
    parser.add_argument('--output', type=str, default=config.DEFAULT_OUTPUT_DIR, help='Output folder for processed chunks')
    parser.add_argument('--chunk-size', type=int, default=config.DEFAULT_CHUNK_SIZE, help='Number of words per chunk')
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)

    # Supported file extensions
    supported_exts = ['.txt', '.pdf', '.docx', '.pptx']  # Add '.msg' when implemented

    for file_path in input_dir.iterdir():
        if file_path.suffix.lower() not in supported_exts:
            continue
        print(f"Processing {file_path}...")
        text = read_file_with_dispatcher(file_path)
        if not text:
            print(f"Skipping {file_path} due to read error or unsupported type.")
            continue
        chunks = chunk_text_by_words(text, args.chunk_size)
        total_chunks = len(chunks)
        for idx, chunk in enumerate(chunks):
            metadata = generate_metadata(file_path, idx+1, total_chunks, chunk)
            md_content = format_chunk_as_markdown(chunk, metadata)
            out_file = output_dir / f"{file_path.stem}_chunk{idx+1}.txt"
            out_file.write_text(md_content, encoding='utf-8')
            print(f"  Wrote chunk {idx+1} to {out_file}")

if __name__ == "__main__":
    main() 