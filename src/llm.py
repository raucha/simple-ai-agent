import os
import httpx


def call_llm(prompt: str) -> str:
    """
    Stateless LLM call: input string -> output string.
    Uses an OpenAI-compatible endpoint for simplicity.
    """
    api_key = os.getenv("LLM_API_KEY")
    base_url = "https://api.openai.com"
    model = "gpt-4.1"

    if not api_key:
        raise RuntimeError("Set LLM_API_KEY in your environment.")

    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
    }

    headers = {"Authorization": f"Bearer {api_key}"}
    url = base_url.rstrip("/") + "/v1/chat/completions"

    with httpx.Client(timeout=60) as client:
        resp = client.post(url, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

    return data["choices"][0]["message"]["content"]
