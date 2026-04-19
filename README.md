# Simple AI Agent

## Setup

```bash
uv sync

mv .env.example .env
nano .env
## Add below API keys
# TAVILY_API_KEY=
# OPEN_AI_API_KEY=
```

## Run

```bash
# 計算させる
uv run python -m src.agent "フィボナッチ数の30番目の数字を計算して"

# 調べ物をさせる
uv run python -m src.agent "明日の天気を教えて"
```
