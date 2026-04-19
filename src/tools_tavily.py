import os
import httpx

TOOL_NAME = "tavily_search"

def tavily_search(query: str) -> str:
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise RuntimeError("Set TAVILY_API_KEY in your environment.")

    payload = {
        "api_key": api_key,
        "query": query,
        "search_depth": "basic",
        "max_results": 5,
    }

    # Tavily検索APIを呼び出し
    with httpx.Client(timeout=30) as client:
        resp = client.post("https://api.tavily.com/search", json=payload)
        resp.raise_for_status()
        data = resp.json()

    # 検索結果を整形
    results = data.get("results", [])
    lines = []
    for item in results:
        title = item.get("title", "")
        url = item.get("url", "")
        content = item.get("content", "")
        lines.append(f"- {title}\n  {url}\n  {content}")

    # 結果を文字列として返す
    return "\n".join(lines).strip()
