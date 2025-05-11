# LLM Integration Guide

## Overview
The toolkit can use Large Language Models (LLMs) to:
- Classify documents (e.g., "invoice", "report")
- Generate metadata (summaries, keywords, topics)
- Suggest semantic chunk boundaries

## Enabling LLM Features
- Install the `openai` Python package (already in requirements.txt)
- Obtain an OpenAI API key (or configure for your preferred LLM provider)
- Set the API key as an environment variable:
  ```bash
  export OPENAI_API_KEY=your-key-here
  ```
- Use the `--llm-metadata` CLI flag or enable in the UI

## Usage Tips
- LLM features may incur API costs
- For local LLMs, see future docs for integration with Llama.cpp, Ollama, etc.
- LLM-generated metadata is added to each chunk's metadata fields

## Troubleshooting
- Ensure your API key is valid and has quota
- Check your internet connection
- Review logs for error messages 