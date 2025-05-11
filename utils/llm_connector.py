"""
llm_connector.py
---------------
Centralizes all LLM connection logic for metadata enrichment. Default implementation uses Perplexity API, but can be extended for other providers.
"""
import requests
import json
import re

class LLMConnector:
    def __init__(self, api_key, model="sonar", api_url="https://api.perplexity.ai/chat/completions"):
        self.api_key = api_key
        self.model = model
        self.api_url = api_url

    def truncate_text(self, text, max_chars=4000):
        """Truncate text to a maximum number of characters for LLM API limits."""
        return text[:max_chars]

    def clean_text(self, text):
        """Remove control characters (except newline and tab) from text for LLM API compatibility."""
        return re.sub(r'[^\x09\x0A\x0D\x20-\x7E]', '', text)

    def call_llm(self, prompt, max_tokens=256, system_prompt="Be precise and concise."):
        """
        Call the LLM API to get output for a given prompt.
        Default: Perplexity API with 'sonar' model.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.2
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        except requests.exceptions.HTTPError as http_err:
            return f"[LLM HTTP error: {http_err}\nStatus code: {getattr(http_err.response, 'status_code', 'N/A')}\nResponse: {getattr(http_err.response, 'text', 'N/A')}\nRequest: {json.dumps(data)}]"
        except Exception as e:
            return f"[LLM error: {e}\nRequest: {json.dumps(data)}]"

    def enrich_metadata(self, chunk, full_text=None):
        """
        Use LLM to generate summary, keywords, topics, and section/chapter info for the chunk.
        Cleans and truncates chunk to avoid API input size and character errors.
        Returns a dict with LLM metadata.
        """
        chunk_trunc = self.truncate_text(chunk)
        chunk_clean = self.clean_text(chunk_trunc)
        summary_prompt = f"Summarize the following document chunk in 1-2 sentences:\n\n{chunk_clean}"
        keywords_prompt = f"Extract 5-10 keywords or topics from the following document chunk:\n\n{chunk_clean}"
        section_prompt = f"If this chunk is part of a chapter or section, provide the likely section or chapter title. If not, say 'None'.\n\n{chunk_clean}"
        summary = self.call_llm(summary_prompt, max_tokens=128)
        keywords = self.call_llm(keywords_prompt, max_tokens=64)
        section = self.call_llm(section_prompt, max_tokens=32)
        return {
            "llm_summary": summary,
            "llm_keywords": keywords,
            "llm_section": section
        } 