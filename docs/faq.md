# FAQ

## How do I install the required dependencies?
Run `pip install -r requirements.txt` in the project root.

## What file types are supported?
PDF, DOCX, PPTX, MSG, and TXT.

## How do I change the chunking method?
Use the `--chunk-method` CLI argument or select it in the UI.

## How do I enable LLM-based metadata?
Use the `--llm-metadata` CLI argument or enable it in the UI (requires OpenAI API key).

## Where are the output files saved?
In the directory specified by the `--output` argument (default: `rag_documents/`).

## I get an ImportError for a package. What should I do?
Install the missing package with `pip install <package-name>`.

## How do I contribute?
See `CONTRIBUTING.md` for guidelines. 