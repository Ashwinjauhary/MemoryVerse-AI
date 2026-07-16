"""
Groq LLM wrapper — provides a single function for structured JSON extraction.
Uses Groq's ultra-fast inference with llama-3.3-70b-versatile.
"""

import json
import re
from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.3-70b-versatile"


def _strip_fences(text: str) -> str:
    """Remove markdown code fences that LLMs sometimes wrap around JSON."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def call_llm_json(system_prompt: str, user_prompt: str, retries: int = 2) -> dict:
    """
    Call Groq and parse the response as JSON.
    Retries once with a stricter reminder if parsing fails.
    """
    for attempt in range(retries):
        prompt = user_prompt
        if attempt > 0:
            prompt += "\n\nIMPORTANT: Your previous response was not valid JSON. Reply ONLY with a raw JSON object. No markdown, no explanation."

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=1024,
        )

        raw = _strip_fences(response.choices[0].message.content)

        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            if attempt == retries - 1:
                raise ValueError(f"Groq returned non-JSON after {retries} attempts: {raw[:300]}")

    return {}
