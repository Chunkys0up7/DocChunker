# Usage Examples

## CLI Example

```bash
python main.py --source input_files --output rag_documents --chunk-size 500 --chunk-method word
```

## UI Example

```bash
streamlit run app.py
```
- Upload files via the web interface
- Configure chunking and metadata options
- Preview and export output

## Sample Input
- PDF, DOCX, PPTX, MSG, or TXT files placed in the `input_files/` directory

## Sample Output
- Chunks saved in `rag_documents/` with rich metadata headers
- Output formats: TXT, JSON, or CSV 